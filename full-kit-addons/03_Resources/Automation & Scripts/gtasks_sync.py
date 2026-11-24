"""
gtasks_sync.py - Two-Way Synchronization Engine between Google Tasks and Obsidian Vault
========================================================================================

Architecture:
- Inbound: Pulls reminders/tasks created in Google Tasks on mobile/desktop into Obsidian Daily Notes.
- Outbound (Option B): Pushes tasks scheduled in Obsidian Daily Notes to Google Tasks for mobile reminders.
- Reconcile & Prune: Syncs completed status both ways and automatically completes stale/rolled-over/superseded
  Obsidian tasks from prior days in Google Tasks so mobile task counts match today's active Daily Note.
- Cross-Workstation Continuity: Dynamically resolves Path.home() across workstations and mirrors token.json
  and gtasks_state.json into 06_Metadata/Gemini/GoogleTasks/.
- Safety: Enforces pre-edit snapshot backups in 06_Metadata/Gemini/Backups/ before modifying any vault markdown file.
"""

import os
import sys
import re
import json
import shutil
import argparse
from datetime import datetime, timezone
from pathlib import Path

# Force UTF-8 and line-buffered stdout/stderr on Windows so background tasks stream immediately
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)

# Google API libraries
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("ERROR: Google API dependencies not found in current Python environment.", file=sys.stderr)
    print(f"Run using the dedicated venv at {Path.home() / '.gemini' / 'tools' / 'google-tasks' / '.venv' / 'Scripts' / 'python.exe'}", file=sys.stderr)
    sys.exit(1)

# Scopes required
SCOPES = ['https://www.googleapis.com/auth/tasks']

# File system paths (cross-platform: Windows, Linux, Android Termux)
def _resolve_vault_dir() -> Path:
    # 1. Resolve relative to this script inside the vault
    script_vault = Path(__file__).resolve().parents[2]
    if (script_vault / "06_Metadata" / "Gemini").exists():
        return script_vault
    # 2. Termux / Linux vault symlink
    home_vault = Path.home() / "vault"
    if (home_vault / "06_Metadata" / "Gemini").exists():
        return home_vault.resolve()
    # 3. Windows OneDrive / Google Drive fallbacks
    env_vault = os.environ.get("CALM_SLATE_VAULT") or os.environ.get("VAULT_DIR")
    if env_vault and (Path(env_vault) / "06_Metadata" / "Gemini").exists():
        return Path(env_vault).resolve()
    return default_od

VAULT_DIR = _resolve_vault_dir()
VAULT_GTASKS_DIR = VAULT_DIR / "06_Metadata" / "Gemini" / "GoogleTasks"
LOCAL_DIR = Path.home() / ".gemini" / "tools" / "google-tasks"
CREDENTIALS_PATH = LOCAL_DIR / "credentials.json"
TOKEN_PATH = LOCAL_DIR / "token.json"
STATE_PATH = LOCAL_DIR / "gtasks_state.json"
VAULT_TOKEN_PATH = VAULT_GTASKS_DIR / "token.json"
VAULT_STATE_PATH = VAULT_GTASKS_DIR / "gtasks_state.json"
BACKUP_BASE_DIR = VAULT_DIR / "06_Metadata" / "Gemini" / "Backups"
INBOX_DIR = VAULT_DIR / "00_Inbox" / "Daily Notes"

# Category tagging rules based on keywords
DOMAIN_TAGS = [
    (r"\b(doctor|clinic|dentist|pharmacy|medicine|therapy|health|workout)\b", "#health"),
    (r"\b(bill|invoice|tax|bank|budget|payment|insurance|renew)\b", "#finance"),
    (r"\b(meeting|project|client|report|review|deadline|email)\b", "#work"),
    (r"\b(grocery|groceries|store|buy|pick up|errand|amazon)\b", "#errand"),
    (r"\b(grocery|groceries|store|errand|costco|walmart|kroger|mail|post office)\b", "#errand"),
]


def get_domain_tag(text: str) -> str:
    """Classifies a task into an Obsidian domain tag."""
    lower = text.lower()
    for pattern, tag in DOMAIN_TAGS:
        if re.search(pattern, lower):
            return tag
    return "#personal"


def clean_for_mobile_title(text: str) -> str:
    """Cleans Obsidian Wikilinks and Markdown syntax into clean readable text for mobile phone notifications."""
    text = re.sub(r'\[\[(?:[^|\]]+\|)?([^\]]+)\]\]', r'\1', text)
    text = re.sub(r'[*_~`]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def authenticate_google_tasks():
    """Authenticates with Google Tasks API using OAuth 2.0, syncing token across workstations."""
    creds = None
    LOCAL_DIR.mkdir(parents=True, exist_ok=True)
    VAULT_GTASKS_DIR.mkdir(parents=True, exist_ok=True)

    # Prefer newest token between local and vault
    if VAULT_TOKEN_PATH.exists() and (
        not TOKEN_PATH.exists() or VAULT_TOKEN_PATH.stat().st_mtime > TOKEN_PATH.stat().st_mtime
    ):
        shutil.copy2(VAULT_TOKEN_PATH, TOKEN_PATH)

    if TOKEN_PATH.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
        except Exception as e:
            print(f"[AUTH] Existing token corrupted: {e}. Re-authenticating...")
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                print("[AUTH] Refreshing expired access token...")
                creds.refresh(Request())
            except Exception as e:
                print(f"[AUTH] Token refresh failed ({e}). Re-authenticating via browser...")
                creds = None

        if not creds:
            if not CREDENTIALS_PATH.exists():
                vault_creds = VAULT_GTASKS_DIR / "credentials.json"
                if vault_creds.exists():
                    shutil.copy2(vault_creds, CREDENTIALS_PATH)
                else:
                    raise FileNotFoundError(
                        f"OAuth credentials not found at {CREDENTIALS_PATH} or {vault_creds}."
                    )

            print("[AUTH] Initiating browser OAuth flow for Google Tasks on port 8088...")
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=8088)

        token_json = creds.to_json()
        TOKEN_PATH.write_text(token_json, encoding="utf-8")
        VAULT_TOKEN_PATH.write_text(token_json, encoding="utf-8")
        print("[AUTH] Authentication successful. Token cached locally and mirrored to vault.")

    return build("tasks", "v1", credentials=creds)


def load_state() -> dict:
    """Loads sync state database, preferring newest copy between local and vault."""
    if VAULT_STATE_PATH.exists() and (
        not STATE_PATH.exists() or VAULT_STATE_PATH.stat().st_mtime > STATE_PATH.stat().st_mtime
    ):
        LOCAL_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(VAULT_STATE_PATH, STATE_PATH)

    if STATE_PATH.exists():
        try:
            with open(STATE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "version": 1,
        "last_sync": None,
        "tasks": {}
    }


def save_state(state: dict):
    """Saves sync state database locally and mirrors to vault."""
    LOCAL_DIR.mkdir(parents=True, exist_ok=True)
    VAULT_GTASKS_DIR.mkdir(parents=True, exist_ok=True)
    state["last_sync"] = datetime.now(timezone.utc).isoformat()
    payload = json.dumps(state, indent=2)
    STATE_PATH.write_text(payload, encoding="utf-8")
    VAULT_STATE_PATH.write_text(payload, encoding="utf-8")


def take_backup_snapshot(file_path: Path) -> Path:
    """Takes a mandatory pre-edit timestamped backup per AGENTS.md Rule 5."""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H%M%S")
    backup_dir = BACKUP_BASE_DIR / date_str
    backup_dir.mkdir(parents=True, exist_ok=True)

    backup_path = backup_dir / f"{time_str}_{file_path.name}.bak.md"
    shutil.copy2(file_path, backup_path)
    print(f"[BACKUP] Snapshot saved: {backup_path}")
    return backup_path


def parse_rfc3339_date(rfc_str: str) -> tuple[str, str]:
    """Parses RFC 3339 timestamp into (YYYY-MM-DD, HH:MM)."""
    if not rfc_str:
        return "", ""
    try:
        dt = datetime.fromisoformat(rfc_str.replace("Z", "+00:00"))
        date_str = dt.strftime("%Y-%m-%d")
        time_str = dt.strftime("%H:%M") if (dt.hour != 0 or dt.minute != 0) else ""
        return date_str, time_str
    except Exception:
        return rfc_str[:10] if len(rfc_str) >= 10 else "", ""


def parse_obsidian_tasks(daily_note_path: Path, today_str: str) -> tuple[list[dict], list[dict]]:
    """Returns (open_tasks, completed_tasks) parsed from the specified Daily Note."""
    open_tasks = []
    completed_tasks = []
    if not daily_note_path.exists():
        return open_tasks, completed_tasks

    content = daily_note_path.read_text(encoding="utf-8")
    for line in content.splitlines():
        line_str = line.strip()
        if not (line_str.startswith("- [ ]") or line_str.startswith("- [x]") or line_str.startswith("- [X]")):
            continue

        is_completed = not line_str.startswith("- [ ]")
        match = re.search(
            r"-\s*\[([ xX])\]\s*\*\*(.+?)\*\*(?::\s*(.+?))?(?=\s*📅|\s*⏰|\s*✅|\s+#[a-zA-Z][\w-]*(?:\s+#[a-zA-Z][\w-]*)*\s*$|$)",
            line_str
        )
        if not match:
            continue

        headline = match.group(2).strip()
        details = match.group(3).strip() if match.group(3) else ""
        full_title = f"{headline}: {details}" if details else headline

        date_match = re.search(r"📅\s*(\d{4}-\d{2}-\d{2})", line_str)
        due_date_str = date_match.group(1) if date_match else today_str

        time_match = re.search(r"⏰\s*(\d{1,2}:\d{2})", line_str)
        due_time_str = time_match.group(1) if time_match else ""

        clean_title = clean_for_mobile_title(full_title)
        clean_headline = clean_for_mobile_title(headline)

        entry = {
            "raw_line": line_str,
            "headline": headline,
            "details": details,
            "full_title": full_title,
            "clean_title": clean_title,
            "clean_headline": clean_headline,
            "due": due_date_str,
            "time": due_time_str,
            "is_gtasks_origin": "#gtasks" in line_str,
        }
        if is_completed:
            completed_tasks.append(entry)
        else:
            open_tasks.append(entry)

    return open_tasks, completed_tasks


def is_obsidian_origin_task(remote_task: dict, synced_tasks: dict) -> bool:
    """Determines whether a Google Task originated from an Obsidian push."""
    t_id = remote_task.get("id", "")
    notes = remote_task.get("notes", "")
    if "Synced from Obsidian Daily Note" in notes:
        return True
    if t_id in synced_tasks and synced_tasks[t_id].get("source") == "obsidian":
        return True
    return False


def sync_google_tasks(dry_run=False, inbound_only=False, outbound_only=False, date_str=None):
    """Runs full two-way synchronization and stale-task pruning between Google Tasks and Obsidian."""
    today_str = date_str if date_str else datetime.now().strftime("%Y-%m-%d")
    daily_note_path = INBOX_DIR / f"{today_str}.md"

    if not daily_note_path.exists():
        print(f"[WARN] Target daily note not found: {daily_note_path}. Proceeding with inbound creation check.")

    service = authenticate_google_tasks()
    state = load_state()
    synced_tasks = state.setdefault("tasks", {})

    print(f"=== Google Tasks <-> Obsidian Sync Started ({today_str}) ===")

    # 1. Fetch Google Tasks lists
    tasklists_resp = service.tasklists().list().execute()
    tasklists = tasklists_resp.get("items", [])
    if not tasklists:
        print("[GTASKS] No task lists found.")
        return

    primary_list_id = tasklists[0]["id"]
    print(f"[GTASKS] Using primary task list: '{tasklists[0].get('title', 'Default')}' ({primary_list_id})")

    # Fetch all tasks (paginate if needed)
    remote_tasks = []
    page_token = None
    while True:
        tasks_resp = service.tasks().list(
            tasklist=primary_list_id,
            maxResults=100,
            showCompleted=True,
            showHidden=True,
            pageToken=page_token
        ).execute()
        remote_tasks.extend(tasks_resp.get("items", []))
        page_token = tasks_resp.get("nextPageToken")
        if not page_token:
            break

    open_remote = [t for t in remote_tasks if t.get("status") == "needsAction"]
    print(f"[GTASKS] Retrieved {len(remote_tasks)} total tasks ({len(open_remote)} currently open in Google Tasks).")

    # Parse today's Obsidian Daily Note
    obs_open, obs_completed = parse_obsidian_tasks(daily_note_path, today_str)
    obs_open_titles = {t["clean_title"] for t in obs_open} | {t["clean_headline"] for t in obs_open} | {t["full_title"] for t in obs_open}
    obs_comp_titles = {t["clean_title"] for t in obs_completed} | {t["clean_headline"] for t in obs_completed} | {t["full_title"] for t in obs_completed}

    # -------------------------------------------------------------
    # PHASE A: INBOUND SYNC (Phone-Created Google Tasks -> Obsidian Daily Note)
    # -------------------------------------------------------------
    inbound_added = 0
    inbound_completed = 0
    new_obsidian_lines = []

    if not outbound_only:
        for t in remote_tasks:
            t_id = t["id"]
            title = t.get("title", "").strip()
            notes = t.get("notes", "").strip()
            status = t.get("status", "needsAction")
            due_rfc = t.get("due", "")

            if not title:
                continue

            obs_origin = is_obsidian_origin_task(t, synced_tasks)
            due_date, due_time = parse_rfc3339_date(due_rfc)
            if not due_time:
                time_match = re.search(r"\b(?:at|@)\s*(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)\b", title, re.IGNORECASE)
                if time_match:
                    due_time = time_match.group(1).strip()

            if t_id not in synced_tasks and not obs_origin:
                # Genuine task created on phone/Google Tasks (not pushed from Obsidian)
                if status == "needsAction":
                    if title in obs_open_titles or title in obs_comp_titles:
                        # Already present in today's Daily Note
                        synced_tasks[t_id] = {
                            "title": title,
                            "clean_title": title,
                            "due": due_date or today_str,
                            "time": due_time,
                            "status": "needsAction",
                            "source": "gtasks",
                            "obsidian_file": str(daily_note_path),
                            "last_synced": datetime.now(timezone.utc).isoformat()
                        }
                        continue

                    domain_tag = get_domain_tag(f"{title} {notes}")
                    time_part = f" ⏰ {due_time}" if due_time else ""
                    date_part = f" 📅 {due_date}" if due_date else f" 📅 {today_str}"
                    notes_part = f": {notes}" if notes else ""

                    obs_line = f"- [ ] **{title}**{notes_part}{date_part}{time_part} {domain_tag} #gtasks"
                    new_obsidian_lines.append(obs_line)
                    inbound_added += 1

                    synced_tasks[t_id] = {
                        "title": title,
                        "notes": notes,
                        "due": due_date,
                        "time": due_time,
                        "status": "needsAction",
                        "source": "gtasks",
                        "obsidian_file": str(daily_note_path),
                        "last_synced": datetime.now(timezone.utc).isoformat()
                    }
                    print(f"[INBOUND NEW] Pulled from phone: '{title}' -> {domain_tag}")
            else:
                # Known task: check if completed on phone while still open in today's Obsidian note
                prior = synced_tasks.get(t_id, {})
                if status == "completed" and (prior.get("status") == "needsAction" or title in obs_open_titles):
                    if title in obs_open_titles:
                        print(f"[INBOUND COMPLETE] Task completed on phone: '{title}'")
                        inbound_completed += 1
                    if t_id in synced_tasks:
                        synced_tasks[t_id]["status"] = "completed"

    # Insert inbound tasks into Obsidian Daily Note
    if new_obsidian_lines and daily_note_path.exists():
        if not dry_run:
            take_backup_snapshot(daily_note_path)
            content = daily_note_path.read_text(encoding="utf-8")

            target_header = "### Personal, Home & Administration"
            if target_header in content:
                idx = content.find(target_header) + len(target_header)
                insertion = "\n" + "\n".join(new_obsidian_lines)
                content = content[:idx] + insertion + content[idx:]
            elif "## 📋 Tasks by Domain" in content:
                idx = content.find("## 📋 Tasks by Domain") + len("## 📋 Tasks by Domain")
                insertion = "\n" + "\n".join(new_obsidian_lines)
                content = content[:idx] + insertion + content[idx:]
            elif "## Tasks by Domain" in content:
                idx = content.find("## Tasks by Domain") + len("## Tasks by Domain")
                insertion = "\n" + "\n".join(new_obsidian_lines)
                content = content[:idx] + insertion + content[idx:]
            else:
                content += "\n\n## Inbound Tasks from Google Tasks\n" + "\n".join(new_obsidian_lines) + "\n"

            daily_note_path.write_text(content, encoding="utf-8")
            print(f"[OBSIDIAN WRITE] Ingested {len(new_obsidian_lines)} inbound task(s) into {daily_note_path.name}")
        else:
            print(f"[DRY RUN] Would insert {len(new_obsidian_lines)} tasks into {daily_note_path.name}")

    # -------------------------------------------------------------
    # PHASE B: RECONCILE & PRUNE STALE OBSIDIAN TASKS IN GOOGLE TASKS
    # -------------------------------------------------------------
    outbound_pushed = 0
    outbound_completed = 0
    stale_pruned = 0

    if not inbound_only and daily_note_path.exists():
        # Refresh obs_open in case inbound tasks were added
        obs_open, obs_completed = parse_obsidian_tasks(daily_note_path, today_str)

        # Map active Obsidian tasks to see which remote tasks match
        matched_remote_ids = set()
        matched_obs_indices = set()

        for idx, obs_task in enumerate(obs_open):
            for rt in open_remote:
                rt_id = rt["id"]
                if rt_id in matched_remote_ids:
                    continue
                rt_title = rt.get("title", "").strip()
                if rt_title in (obs_task["clean_title"], obs_task["clean_headline"], obs_task["full_title"], obs_task["headline"]):
                    matched_remote_ids.add(rt_id)
                    matched_obs_indices.add(idx)
                    synced_tasks[rt_id] = {
                        "title": obs_task["full_title"],
                        "clean_title": obs_task["clean_title"],
                        "due": obs_task["due"],
                        "time": obs_task["time"],
                        "status": "needsAction",
                        "source": "obsidian" if is_obsidian_origin_task(rt, synced_tasks) else "gtasks",
                        "obsidian_file": str(daily_note_path),
                        "last_synced": datetime.now(timezone.utc).isoformat()
                    }
                    break

        # Complete any open remote task that is NOT matched to an active open task in today's Daily Note
        # (if it was pushed from Obsidian or matches a completed task)
        for rt in open_remote:
            rt_id = rt["id"]
            if rt_id in matched_remote_ids:
                continue
            rt_title = rt.get("title", "").strip()
            obs_origin = is_obsidian_origin_task(rt, synced_tasks)
            is_comp_in_obs = rt_title in obs_comp_titles

            if obs_origin or is_comp_in_obs:
                if not dry_run:
                    service.tasks().patch(
                        tasklist=primary_list_id,
                        task=rt_id,
                        body={"status": "completed"}
                    ).execute()
                    if rt_id in synced_tasks:
                        synced_tasks[rt_id]["status"] = "completed"
                    if is_comp_in_obs:
                        outbound_completed += 1
                        print(f"[OUTBOUND COMPLETE] Marked completed in Google Tasks: '{rt_title}'")
                    else:
                        stale_pruned += 1
                        print(f"[STALE PRUNED] Completed prior-day/rolled-over task in Google Tasks: '{rt_title}'")
                else:
                    print(f"[DRY RUN] Would complete stale/completed task in Google Tasks: '{rt_title}'")

        # Push any active open task in today's Daily Note that wasn't already open in Google Tasks
        for idx, obs_task in enumerate(obs_open):
            if idx in matched_obs_indices or obs_task["is_gtasks_origin"]:
                continue

            clean_title = obs_task["clean_title"]
            due_date_str = obs_task["due"]
            due_time_str = obs_task["time"]
            full_title = obs_task["full_title"]

            task_body = {
                "title": clean_title,
                "notes": f"Synced from Obsidian Daily Note ({today_str}).\nScheduled: {due_date_str} {due_time_str}\nOriginal: {full_title}".strip(),
            }
            if due_date_str:
                task_body["due"] = f"{due_date_str}T00:00:00.000Z"

            if not dry_run:
                created = service.tasks().insert(tasklist=primary_list_id, body=task_body).execute()
                created_id = created["id"]
                synced_tasks[created_id] = {
                    "title": full_title,
                    "clean_title": clean_title,
                    "due": due_date_str,
                    "time": due_time_str,
                    "status": "needsAction",
                    "source": "obsidian",
                    "obsidian_file": str(daily_note_path),
                    "last_synced": datetime.now(timezone.utc).isoformat()
                }
                outbound_pushed += 1
                print(f"[OUTBOUND PUSH] Created Google Task: '{clean_title}' (Due: {due_date_str} {due_time_str})")
            else:
                print(f"[DRY RUN] Would push to Google Tasks: '{clean_title}' (Due: {due_date_str} {due_time_str})")

    # -------------------------------------------------------------
    # PHASE C: RECONCILE OBSIDIAN COMPLETIONS FROM INBOUND PHASE
    # -------------------------------------------------------------
    if inbound_completed > 0 and daily_note_path.exists():
        if not dry_run:
            take_backup_snapshot(daily_note_path)
            content = daily_note_path.read_text(encoding="utf-8")
            lines = content.splitlines()
            modified = False

            for i, line in enumerate(lines):
                if line.strip().startswith("- [ ]"):
                    for rt in remote_tasks:
                        if rt.get("status") == "completed":
                            rt_title = rt.get("title", "").strip()
                            if rt_title and rt_title in clean_for_mobile_title(line):
                                lines[i] = line.replace("- [ ]", "- [x]", 1) + f" ✅ {today_str}"
                                modified = True
                                print(f"[OBSIDIAN RECONCILE] Checked off completed item: {rt_title}")
                                break

            if modified:
                daily_note_path.write_text("\n".join(lines), encoding="utf-8")
                print(f"[OBSIDIAN WRITE] Reconciled completed tasks in {daily_note_path.name}")

    if not dry_run:
        save_state(state)

    print("=== Sync Summary ===")
    print(f"Inbound Added:      {inbound_added}")
    print(f"Inbound Completed:  {inbound_completed}")
    print(f"Outbound Pushed:    {outbound_pushed}")
    print(f"Outbound Completed: {outbound_completed}")
    print(f"Stale Tasks Pruned: {stale_pruned}")
    print("====================")


def main():
    parser = argparse.ArgumentParser(description="Google Tasks <-> Obsidian Two-Way Synchronizer")
    parser.add_argument("--dry-run", action="store_true", help="Simulate sync without writing to disk or Google Tasks")
    parser.add_argument("--inbound-only", action="store_true", help="Only pull tasks from Google Tasks to Obsidian")
    parser.add_argument("--outbound-only", action="store_true", help="Only push tasks from Obsidian to Google Tasks")
    parser.add_argument("--date", type=str, default=None, help="Target Daily Note date (YYYY-MM-DD)")
    args = parser.parse_args()

    sync_google_tasks(
        dry_run=args.dry_run,
        inbound_only=args.inbound_only,
        outbound_only=args.outbound_only,
        date_str=args.date
    )


if __name__ == "__main__":
    main()
