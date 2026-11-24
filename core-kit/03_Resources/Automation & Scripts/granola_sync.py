#!/usr/bin/env python3
r"""
granola_sync.py - Cross-Platform Granola Meeting Sync (Windows, Linux, Android Termux)
======================================================================================

Syncs Granola AI meeting notes directly into 00_Inbox/Granola/ via Granola's official
cloud MCP endpoint (https://mcp.granola.ai/mcp) using OAuth 2.0 (works on Free tier
for the rolling 30-day window, or paid tiers with unlimited history).

Features:
  - Runs natively on Android Termux (tablet/phone) and Windows without Desktop Obsidian.
  - Scans existing 00_Inbox/Granola/*.md files for granola_id to prevent duplicates.
  - Formats notes matching 06_Metadata/Templates/Granola Template.md.
  - Enforces the OneDrive & Cross-Platform File Naming Standard.
  - Supports --list (dry run), --date YYYY-MM-DD, --link-daily (links synced meetings
    into today's Daily Note with a pre-edit backup), and --auth (fresh PKCE OAuth login).
"""

import argparse
import base64
import datetime
import hashlib
import html
import http.server
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
import xml.etree.ElementTree as ET
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

MCP_URL = "https://mcp.granola.ai/mcp"
AUTH_ISSUER = "https://mcp-auth.granola.ai"
PROTOCOL_VERSION = "2025-03-26"


def resolve_vault_root() -> Path:
    script_vault = Path(__file__).resolve().parents[2]
    if (script_vault / "06_Metadata" / "Gemini").exists():
        return script_vault
    home_vault = Path.home() / "vault"
    if (home_vault / "06_Metadata" / "Gemini").exists():
        return home_vault.resolve()
    env_vault = os.environ.get("WAYPOST_VAULT") or os.environ.get("VAULT_DIR")
    if env_vault and (Path(env_vault) / "06_Metadata" / "Gemini").exists():
        return Path(env_vault).resolve()
    return script_vault


VAULT_ROOT = resolve_vault_root()
GRANOLA_DIR = VAULT_ROOT / "00_Inbox" / "Granola"
DAILY_DIR = VAULT_ROOT / "00_Inbox" / "Daily Notes"
BACKUP_DIR = VAULT_ROOT / "06_Metadata" / "Gemini" / "Backups"
PLUGIN_DATA_PATH = VAULT_ROOT / ".obsidian" / "plugins" / "granola-meetings-simple-sync" / "data.json"
LOCAL_AUTH_PATH = Path.home() / ".gemini" / "tools" / "granola" / "auth.json"
VAULT_AUTH_DIR = VAULT_ROOT / "06_Metadata" / "Gemini" / "GranolaAuth"


def sanitize_filename(name: str, max_len: int = 100) -> str:
    """Enforces OneDrive & Cross-Platform File Naming Standard."""
    name = html.unescape(name or "")
    name = re.sub(r'[\\/:*?"<>|]+', "-", name)
    name = re.sub(r"[\r\n\t]+", " ", name)
    name = re.sub(r"\s+", " ", name).strip()
    while name.startswith(".."):
        name = name[2:].lstrip()
    name = name.rstrip(". ").strip()
    if len(name) > max_len:
        name = name[:max_len].rstrip(". ").strip()
    return name or "Untitled Meeting"


def backup_file(filepath: Path) -> Path:
    today_str = datetime.date.today().isoformat()
    ts_str = datetime.datetime.now().strftime("%H%M%S")
    dest_dir = BACKUP_DIR / today_str
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{ts_str}_{filepath.stem}.bak.md"
    shutil.copy2(filepath, dest)
    return dest


def http_json(url: str, data: bytes | None = None, headers: dict | None = None, method: str = "GET") -> tuple[int, dict, bytes]:
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, dict(resp.headers.items()), resp.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers.items()), e.read()


def discover_oauth_metadata(issuer: str = AUTH_ISSUER) -> dict:
    for suffix in ("/.well-known/oauth-authorization-server", "/.well-known/openid-configuration"):
        status, _, body = http_json(issuer.rstrip("/") + suffix, headers={"Accept": "application/json"})
        if status == 200:
            return json.loads(body.decode("utf-8"))
    return {
        "issuer": issuer,
        "authorization_endpoint": f"{issuer}/oauth2/authorize",
        "token_endpoint": f"{issuer}/oauth2/token",
        "registration_endpoint": f"{issuer}/oauth2/register",
    }


def decode_jwt_exp(token: str) -> int:
    try:
        parts = token.split(".")
        if len(parts) < 2:
            return 0
        payload = parts[1] + "=" * (-len(parts[1]) % 4)
        data = json.loads(base64.urlsafe_b64decode(payload).decode("utf-8"))
        return int(data.get("exp", 0))
    except Exception:
        return 0


def load_auth_state() -> dict | None:
    if LOCAL_AUTH_PATH.exists():
        try:
            return json.loads(LOCAL_AUTH_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass

    # Bootstrap from existing Obsidian plugin data.json if available
    if PLUGIN_DATA_PATH.exists():
        try:
            pdata = json.loads(PLUGIN_DATA_PATH.read_text(encoding="utf-8"))
            accounts = pdata.get("accounts") or []
            if accounts:
                acc = accounts[0]
                tokens = acc.get("oauthTokens") or {}
                client_info = acc.get("oauthClientInfo") or {}
                if tokens.get("refresh_token") or tokens.get("access_token"):
                    state = {
                        "source": "plugin_bootstrap",
                        "email": acc.get("email", ""),
                        "issuer": client_info.get("issuer") or tokens.get("issuer") or AUTH_ISSUER,
                        "client_id": client_info.get("client_id", ""),
                        "access_token": tokens.get("access_token", ""),
                        "refresh_token": tokens.get("refresh_token", ""),
                        "scope": tokens.get("scope") or client_info.get("scope") or "mcp",
                    }
                    save_auth_state(state)
                    return state
        except Exception:
            pass
    return None


def save_auth_state(state: dict) -> None:
    LOCAL_AUTH_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOCAL_AUTH_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")
    try:
        os.chmod(LOCAL_AUTH_PATH, 0o600)
    except OSError:
        pass


def refresh_access_token(state: dict) -> dict:
    issuer = state.get("issuer") or AUTH_ISSUER
    meta = discover_oauth_metadata(issuer)
    token_endpoint = meta.get("token_endpoint")
    if not token_endpoint:
        raise RuntimeError("OAuth metadata missing token_endpoint.")

    form = {
        "grant_type": "refresh_token",
        "refresh_token": state["refresh_token"],
        "client_id": state["client_id"],
    }
    encoded = urllib.parse.urlencode(form).encode("utf-8")
    status, _, body = http_json(
        token_endpoint,
        data=encoded,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        method="POST",
    )
    if status != 200:
        raise RuntimeError(
            f"OAuth token refresh failed (HTTP {status}): {body.decode('utf-8', errors='replace')}\n"
            "Run `granola_sync.py --auth` to re-authenticate."
        )

    tok = json.loads(body.decode("utf-8"))
    state["access_token"] = tok["access_token"]
    if tok.get("refresh_token"):
        state["refresh_token"] = tok["refresh_token"]
    state["refreshed_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save_auth_state(state)
    return state


def run_interactive_pkce_auth(port: int = 8765) -> dict:
    meta = discover_oauth_metadata(AUTH_ISSUER)
    reg_endpoint = meta.get("registration_endpoint")
    auth_endpoint = meta.get("authorization_endpoint")
    token_endpoint = meta.get("token_endpoint")
    redirect_uri = f"http://127.0.0.1:{port}/callback"

    if not reg_endpoint or not auth_endpoint or not token_endpoint:
        raise RuntimeError("Unable to discover Granola OAuth endpoints.")

    reg_payload = json.dumps(
        {
            "client_name": "Antigravity Termux Granola Sync",
            "redirect_uris": [redirect_uri],
            "grant_types": ["authorization_code", "refresh_token"],
            "response_types": ["code"],
            "token_endpoint_auth_method": "none",
            "scope": "mcp",
        }
    ).encode("utf-8")
    status, _, body = http_json(
        reg_endpoint,
        data=reg_payload,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    if status not in (200, 201):
        raise RuntimeError(f"Dynamic client registration failed (HTTP {status}): {body.decode('utf-8', errors='replace')}")
    client_info = json.loads(body.decode("utf-8"))
    client_id = client_info["client_id"]

    code_verifier = secrets.token_urlsafe(48)
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("ascii")).digest()).rstrip(b"=").decode("ascii")
    oauth_state = secrets.token_urlsafe(24)

    auth_params = urllib.parse.urlencode(
        {
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": "mcp",
            "state": oauth_state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }
    )
    auth_url = f"{auth_endpoint}?{auth_params}"

    result_box = {"code": None, "error": None}
    done_event = threading.Event()

    class CallbackHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            qs = urllib.parse.parse_qs(parsed.query)
            if qs.get("state", [""])[0] != oauth_state:
                result_box["error"] = "OAuth state mismatch"
            elif "error" in qs:
                result_box["error"] = qs["error"][0]
            else:
                result_box["code"] = qs.get("code", [None])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h2>Granola Sync Authenticated</h2><p>You can close this tab and return to Termux.</p></body></html>")
            done_event.set()

        def log_message(self, format, *args):
            pass

    server = http.server.HTTPServer(("127.0.0.1", port), CallbackHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()

    print("\n=== Granola OAuth Sign-In ===")
    print("Opening browser to authorize Granola Sync (or copy/paste this URL):\n")
    print(auth_url)
    try:
        if shutil.which("termux-open-url"):
            subprocess.Popen(["termux-open-url", auth_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            webbrowser.open(auth_url)
    except Exception:
        pass
    print("\nWaiting for callback on 127.0.0.1...")
    done_event.wait(timeout=300)
    server.shutdown()

    if result_box["error"] or not result_box["code"]:
        raise RuntimeError(f"Granola OAuth failed: {result_box['error'] or 'Timed out'}")

    tok_form = urllib.parse.urlencode(
        {
            "grant_type": "authorization_code",
            "code": result_box["code"],
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "code_verifier": code_verifier,
        }
    ).encode("utf-8")
    status, _, body = http_json(
        token_endpoint,
        data=tok_form,
        headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
        method="POST",
    )
    if status != 200:
        raise RuntimeError(f"Token exchange failed (HTTP {status}): {body.decode('utf-8', errors='replace')}")
    tok = json.loads(body.decode("utf-8"))
    state = {
        "source": "dedicated_pkce",
        "issuer": AUTH_ISSUER,
        "client_id": client_id,
        "access_token": tok["access_token"],
        "refresh_token": tok.get("refresh_token", ""),
        "scope": tok.get("scope", "mcp"),
        "refreshed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    save_auth_state(state)
    print(f"[+] Granola OAuth saved to {LOCAL_AUTH_PATH}")
    return state


def get_valid_access_token() -> str:
    state = load_auth_state()
    if not state:
        raise RuntimeError(
            "No Granola OAuth token found. Run `granola_sync.py --auth` to sign in."
        )
    exp = decode_jwt_exp(state.get("access_token", ""))
    if not state.get("access_token") or exp <= int(time.time()) + 120:
        state = refresh_access_token(state)
    return state["access_token"]


class GranolaMCPClient:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.session_id: str | None = None
        self._req_id = 0

    def _parse_mcp_response(self, headers: dict, body: bytes) -> dict:
        ctype = ""
        for k, v in headers.items():
            if k.lower() == "content-type":
                ctype = v.lower()
            if k.lower() == "mcp-session-id":
                self.session_id = v.strip()

        text = body.decode("utf-8", errors="replace").strip()
        if not text:
            return {}
        if "text/event-stream" in ctype or text.startswith("event:") or text.startswith("data:"):
            last_json = {}
            for line in text.splitlines():
                if line.startswith("data:"):
                    payload = line[5:].strip()
                    if payload and payload != "[DONE]":
                        try:
                            obj = json.loads(payload)
                            if "result" in obj or "error" in obj:
                                last_json = obj
                        except json.JSONDecodeError:
                            pass
            return last_json
        return json.loads(text)

    def _post(self, payload: dict) -> dict:
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": PROTOCOL_VERSION,
        }
        if self.session_id:
            headers["mcp-session-id"] = self.session_id

        status, resp_headers, body = http_json(
            MCP_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        if status == 401:
            # Force refresh once
            state = load_auth_state()
            if state and state.get("refresh_token"):
                state = refresh_access_token(state)
                self.access_token = state["access_token"]
                headers["Authorization"] = f"Bearer {self.access_token}"
                status, resp_headers, body = http_json(
                    MCP_URL,
                    data=json.dumps(payload).encode("utf-8"),
                    headers=headers,
                    method="POST",
                )
        if status not in (200, 202):
            raise RuntimeError(f"Granola MCP HTTP {status}: {body.decode('utf-8', errors='replace')[:400]}")
        return self._parse_mcp_response(resp_headers, body)

    def initialize(self) -> None:
        self._req_id += 1
        self._post(
            {
                "jsonrpc": "2.0",
                "id": self._req_id,
                "method": "initialize",
                "params": {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": {},
                    "clientInfo": {"name": "antigravity-granola-sync", "version": "1.0.0"},
                },
            }
        )
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})

    def call_tool_text(self, tool_name: str, arguments: dict) -> str:
        self._req_id += 1
        resp = self._post(
            {
                "jsonrpc": "2.0",
                "id": self._req_id,
                "method": "tools/call",
                "params": {"name": tool_name, "arguments": arguments},
            }
        )
        if "error" in resp:
            raise RuntimeError(f"Granola MCP tool '{tool_name}' error: {resp['error']}")
        content = resp.get("result", {}).get("content", [])
        parts = [c.get("text", "") for c in content if c.get("type") == "text" and isinstance(c.get("text"), str)]
        return "\n".join(parts)


def parse_xml_or_json_meetings_list(raw_text: str) -> list[dict]:
    """Parses Granola list_meetings response (XML <meeting ...> or JSON)."""
    raw = raw_text.strip()
    if not raw:
        return []
    if raw.startswith("{") or raw.startswith("["):
        try:
            data = json.loads(raw)
            items = data if isinstance(data, list) else data.get("meetings", [])
            return [
                {
                    "id": str(m.get("id", "")),
                    "title": str(m.get("title", "Untitled Meeting")).strip(),
                    "date": str(m.get("date") or m.get("created_at") or ""),
                }
                for m in items
                if m.get("id")
            ]
        except Exception:
            pass

    meetings = []
    # Match <meeting id="..." title="..." date="...">
    for m in re.finditer(r"<meeting\b([^>]*)>(.*?)</meeting>", raw, re.DOTALL | re.IGNORECASE):
        attrs_str, inner = m.group(1), m.group(2)
        attrs = dict(re.findall(r'(\w+)\s*=\s*"([^"]*)"', attrs_str))
        mid = attrs.get("id", "").strip()
        if not mid:
            continue
        title = html.unescape(attrs.get("title", "")).strip() or "Untitled Meeting"
        date_raw = html.unescape(attrs.get("meeting_at") or attrs.get("date") or attrs.get("created_at") or "").strip()
        participants = []
        pm = re.search(r"<known_participants>(.*?)</known_participants>", inner, re.DOTALL | re.IGNORECASE)
        if pm:
            participants = [p.strip() for p in re.split(r"[\n,]+", html.unescape(pm.group(1))) if p.strip()]
        meetings.append({"id": mid, "title": title, "date_raw": date_raw, "participants": participants})

    if not meetings:
        # Fallback for self-closing tags
        for m in re.finditer(r"<meeting\b([^/>]*)/?>", raw, re.IGNORECASE):
            attrs = dict(re.findall(r'(\w+)\s*=\s*"([^"]*)"', m.group(1)))
            mid = attrs.get("id", "").strip()
            if mid:
                meetings.append(
                    {
                        "id": mid,
                        "title": html.unescape(attrs.get("title", "")).strip() or "Untitled Meeting",
                        "date_raw": html.unescape(attrs.get("meeting_at") or attrs.get("date") or attrs.get("created_at") or "").strip(),
                        "participants": [],
                    }
                )
    return meetings


def parse_meeting_details(raw_text: str) -> list[dict]:
    """Parses Granola get_meetings response."""
    raw = raw_text.strip()
    if not raw:
        return []
    if raw.startswith("{") or raw.startswith("["):
        try:
            data = json.loads(raw)
            items = data if isinstance(data, list) else data.get("meetings", [data])
            results = []
            for m in items:
                if not isinstance(m, dict) or not m.get("id"):
                    continue
                results.append(
                    {
                        "id": str(m["id"]),
                        "title": str(m.get("title", "Untitled Meeting")).strip(),
                        "date_raw": str(m.get("date") or m.get("created_at") or ""),
                        "participants": m.get("participants") or m.get("attendees") or [],
                        "private_notes": str(m.get("private_notes") or m.get("notes") or "").strip(),
                        "summary": str(m.get("summary") or m.get("enhanced_notes") or "").strip(),
                    }
                )
            return results
        except Exception:
            pass

    results = []
    for m in re.finditer(r"<meeting\b([^>]*)>(.*?)</meeting>", raw, re.DOTALL | re.IGNORECASE):
        attrs = dict(re.findall(r'(\w+)\s*=\s*"([^"]*)"', m.group(1)))
        inner = m.group(2)
        mid = attrs.get("id", "").strip()
        if not mid:
            continue

        def tag_text(tag_name: str) -> str:
            tm = re.search(rf"<{tag_name}\b[^>]*>(.*?)</{tag_name}>", inner, re.DOTALL | re.IGNORECASE)
            return html.unescape(tm.group(1)).strip() if tm else ""

        participants_raw = tag_text("known_participants")
        participants = [p.strip() for p in re.split(r"[\n,]+", participants_raw) if p.strip()]
        private_notes = tag_text("private_notes")
        summary = tag_text("summary") or tag_text("enhanced_notes")

        results.append(
            {
                "id": mid,
                "title": html.unescape(attrs.get("title", "")).strip() or "Untitled Meeting",
                "date_raw": html.unescape(attrs.get("meeting_at") or attrs.get("date") or attrs.get("created_at") or "").strip(),
                "participants": participants,
                "private_notes": private_notes,
                "summary": summary,
            }
        )
    return results


def parse_iso_date(date_raw: str) -> str:
    """Converts Granola date strings (e.g. 'Nov 24, 2026 10:30 AM' or ISO) to YYYY-MM-DD."""
    if not date_raw:
        return datetime.date.today().isoformat()
    m = re.search(r"(\d{4}-\d{2}-\d{2})", date_raw)
    if m:
        return m.group(1)
    for fmt in (
        "%b %d, %Y %I:%M %p",
        "%B %d, %Y %I:%M %p",
        "%b %d, %Y",
        "%B %d, %Y",
        "%a, %b %d, %Y %I:%M %p",
        "%a, %d %b %Y %H:%M:%S %Z",
    ):
        try:
            return datetime.datetime.strptime(date_raw.strip(), fmt).date().isoformat()
        except ValueError:
            continue
    # Fallback loose month-day-year match
    m2 = re.search(r"([A-Za-z]{3,9})\s+(\d{1,2}),?\s+(\d{4})", date_raw)
    if m2:
        for fmt in ("%b %d %Y", "%B %d %Y"):
            try:
                return datetime.datetime.strptime(f"{m2.group(1)} {m2.group(2)} {m2.group(3)}", fmt).date().isoformat()
            except ValueError:
                continue
    return datetime.date.today().isoformat()


def scan_existing_granola_ids() -> dict[str, Path]:
    existing = {}
    if not GRANOLA_DIR.exists():
        return existing
    for md in GRANOLA_DIR.glob("*.md"):
        try:
            head = md.read_text(encoding="utf-8", errors="ignore")[:1000]
            m = re.search(r"^granola_id:\s*([a-zA-Z0-9_-]+)\s*$", head, re.MULTILINE)
            if m:
                existing[m.group(1).strip()] = md
        except Exception:
            continue
    return existing


def format_granola_note(meeting: dict) -> tuple[str, str]:
    mid = meeting["id"]
    title = meeting["title"]
    date_iso = parse_iso_date(meeting.get("date_raw", ""))
    granola_url = f"https://notes.granola.ai/d/{mid}"

    # Exclude self from attendees cleanly
    attendee_lines = []
    for p in meeting.get("participants", []):
        p_clean = str(p).strip()
        if not p_clean:
            continue
        lower = p_clean.lower()
        self_ids = [s.strip().lower() for s in os.environ.get("GRANOLA_SELF_IDENTIFIERS", "").split(",") if s.strip()]
        if self_ids and any(me in lower for me in self_ids):
            continue
        # Strip email angle brackets for cleaner display
        display = re.sub(r"\s*<[^>]+>", "", p_clean).strip() or p_clean
        safe_display = display.replace('"', "'")
        attendee_lines.append(f'  - "{safe_display}"')

    attendees_block = "\n".join(attendee_lines)
    safe_title = title.replace('"', "'")

    sections = []
    private_notes = (meeting.get("private_notes") or "").strip()
    summary = (meeting.get("summary") or "").strip()
    if private_notes:
        sections.append(f"## Notes\n\n{private_notes}")
    if summary:
        sections.append(f"## Summary\n\n{summary}")
    if not sections:
        sections.append("## Summary\n\n*(No summary generated yet in Granola.)*")

    body = "\n\n".join(sections)
    frontmatter = [
        "---",
        f"granola_id: {mid}",
        f"granola_url: {granola_url}",
        f'title: "{safe_title}"',
        f"date: {date_iso}",
        "attendees:",
    ]
    if attendees_block:
        frontmatter.append(attendees_block)
    frontmatter.extend(
        [
            "categories:",
            '  - "[[Meetings]]"',
            '  - "[[Granola]]"',
            "type: []",
            "org:",
            "loc:",
            "people: []",
            "topics: []",
            f"Created: {date_iso}",
            f"Updated: {datetime.date.today().isoformat()}",
            "---",
        ]
    )

    filename = f"{date_iso} {sanitize_filename(title)}.md"
    return filename, "\n".join(frontmatter) + "\n\n" + body + "\n"


def link_meetings_in_daily_note(target_date: str, note_stems: list[str]) -> bool:
    daily_path = DAILY_DIR / f"{target_date}.md"
    if not daily_path.exists() or not note_stems:
        return False

    content = daily_path.read_text(encoding="utf-8", errors="replace")
    to_add = [stem for stem in note_stems if f"[[{stem}]]" not in content]
    if not to_add:
        return False

    heading = "## 🎙️ Today's Meetings & Granola Notes"
    idx = content.find(heading)
    if idx == -1:
        return False

    backup_file(daily_path)
    next_sep = content.find("\n---", idx + len(heading))
    insert_pos = next_sep if next_sep != -1 else len(content)
    block = content[idx:insert_pos].rstrip()
    # Remove empty placeholder bullet "* " if present alone
    block = re.sub(r"\n\*\s*$", "", block)
    additions = "\n".join(f"* [[{stem}]]" for stem in to_add)
    new_content = content[:idx] + block + "\n" + additions + "\n" + content[insert_pos:]
    daily_path.write_text(new_content, encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Cross-platform Granola MCP meeting sync for Obsidian")
    parser.add_argument("--auth", action="store_true", help="Run fresh OAuth 2.0 PKCE sign-in")
    parser.add_argument(
        "--time-range",
        default="last_30_days",
        choices=["this_week", "last_week", "last_30_days"],
        help="Granola MCP time range to query",
    )
    parser.add_argument("--date", help="Only sync meetings on this date (YYYY-MM-DD)")
    parser.add_argument("--meeting-id", help="Sync a specific Granola meeting ID")
    parser.add_argument("--list", action="store_true", help="List available meetings without writing files")
    parser.add_argument("--force", action="store_true", help="Overwrite existing note if granola_id already exists")
    parser.add_argument("--link-daily", action="store_true", help="Link synced meetings into corresponding Daily Note")
    parser.add_argument("--raw-debug", action="store_true", help="Print raw MCP tool text for troubleshooting")
    args = parser.parse_args()

    if args.auth:
        run_interactive_pkce_auth()
        return

    token = get_valid_access_token()
    client = GranolaMCPClient(token)
    client.initialize()

    if args.meeting_id:
        candidate_ids = [args.meeting_id]
        meetings_meta = [{"id": args.meeting_id, "title": args.meeting_id, "date_raw": ""}]
    else:
        raw_list = client.call_tool_text("list_meetings", {"time_range": args.time_range})
        if args.raw_debug:
            print("=== RAW list_meetings ===")
            print(raw_list[:3000])
        meetings_meta = parse_xml_or_json_meetings_list(raw_list)
        if args.date:
            meetings_meta = [m for m in meetings_meta if parse_iso_date(m.get("date_raw", "")) == args.date]
        candidate_ids = [m["id"] for m in meetings_meta]

    existing = scan_existing_granola_ids()

    if args.list:
        if not meetings_meta:
            print("[=] No Granola meetings found for the requested window.")
            return
        print(f"Found {len(meetings_meta)} meeting(s) in Granola ({args.time_range}):")
        for m in meetings_meta:
            d_iso = parse_iso_date(m.get("date_raw", ""))
            status = "SYNCED" if m["id"] in existing else "NEW"
            print(f"  [{status}] {d_iso} | {m['title']} ({m.get('date_raw', '')}) | id={m['id']}")
        return

    to_fetch = [mid for mid in candidate_ids if args.force or mid not in existing]
    if not to_fetch:
        print(f"[=] All {len(candidate_ids)} Granola meeting(s) are already synced in 00_Inbox/Granola/.")
        if args.link_daily and args.date:
            stems = [existing[mid].stem for mid in candidate_ids if mid in existing]
            if link_meetings_in_daily_note(args.date, stems):
                print(f"[+] Linked {len(stems)} meeting(s) in Daily Note {args.date}.md")
        return

    GRANOLA_DIR.mkdir(parents=True, exist_ok=True)
    synced_by_date: dict[str, list[str]] = {}
    synced_count = 0

    # Fetch in batches of 5 to keep payloads fast
    for i in range(0, len(to_fetch), 5):
        batch = to_fetch[i : i + 5]
        raw_details = client.call_tool_text("get_meetings", {"meeting_ids": batch})
        if args.raw_debug:
            print("=== RAW get_meetings ===")
            print(raw_details[:3000])
        details = parse_meeting_details(raw_details)
        for mtg in details:
            filename, md_content = format_granola_note(mtg)
            target_path = GRANOLA_DIR / filename
            if target_path.exists() and mtg["id"] in existing and not args.force:
                continue
            if target_path.exists():
                backup_file(target_path)
            target_path.write_text(md_content, encoding="utf-8")
            date_iso = parse_iso_date(mtg.get("date_raw", ""))
            synced_by_date.setdefault(date_iso, []).append(target_path.stem)
            synced_count += 1
            print(f"[+] Synced: 00_Inbox/Granola/{target_path.name}")

    if args.link_daily:
        for d_iso, stems in synced_by_date.items():
            if link_meetings_in_daily_note(d_iso, stems):
                print(f"[+] Linked {len(stems)} meeting(s) in Daily Note {d_iso}.md")

    print(f"[+] Granola sync complete: {synced_count} new/updated meeting(s).")


if __name__ == "__main__":
    main()
