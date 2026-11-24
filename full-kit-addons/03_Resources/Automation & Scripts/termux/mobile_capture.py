#!/usr/bin/env python3
r"""
mobile_capture.py - Android Share Sheet Capture Handler for Obsidian Vault
==========================================================================

Invoked by Termux's native Android Share Sheet hooks:
  - ~/bin/termux-url-opener  (shared web links, PDF URLs, articles)
  - ~/bin/termux-file-editor (shared files, PDFs, receipts, screenshots)

Enforces the OneDrive & Cross-Platform File Naming Standard:
  - No leading/trailing whitespace
  - No trailing periods on base names
  - No leading double periods (..)
  - No prohibited characters: \ / : * ? " < > |
"""

import datetime
import hashlib
import html
import os
import re
import shutil
import sys
import urllib.parse
import urllib.request
from pathlib import Path

DIRECT_FILE_EXTS = {
    ".pdf", ".png", ".jpg", ".jpeg", ".webp", ".gif",
    ".docx", ".xlsx", ".pptx", ".csv", ".txt", ".md", ".mht", ".mhtml",
}


def resolve_vault_root() -> Path:
    script_vault = Path(__file__).resolve().parents[3]
    if (script_vault / "06_Metadata" / "Gemini").exists():
        return script_vault
    home_vault = Path.home() / "vault"
    if (home_vault / "06_Metadata" / "Gemini").exists():
        return home_vault.resolve()
    raise FileNotFoundError("Cannot resolve Obsidian vault root.")


def sanitize_filename(name: str, max_len: int = 110) -> str:
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
    return name or "Untitled Capture"


def unique_path(dest_dir: Path, stem: str, suffix: str) -> Path:
    clean_stem = sanitize_filename(stem)
    clean_suffix = suffix.lower() if suffix else ""
    candidate = dest_dir / f"{clean_stem}{clean_suffix}"
    counter = 2
    while candidate.exists():
        candidate = dest_dir / f"{clean_stem} ({counter}){clean_suffix}"
        counter += 1
    return candidate


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_page_title(url: str) -> str:
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Linux; Android 15) ObsidianMobileCapture/1.0"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read(131072).decode("utf-8", errors="ignore")
        m = re.search(r"<title[^>]*>(.*?)</title>", raw, re.IGNORECASE | re.DOTALL)
        if m:
            title = re.sub(r"\s+", " ", html.unescape(m.group(1))).strip()
            if title:
                return title
    except Exception:
        pass
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.replace("www.", "")
    path_part = Path(urllib.parse.unquote(parsed.path)).stem
    return f"{host} - {path_part}" if path_part else host or "Web Capture"


def handle_url(url: str, inbox_dir: Path) -> Path:
    today = datetime.date.today().isoformat()
    parsed = urllib.parse.urlparse(url)
    url_path = Path(urllib.parse.unquote(parsed.path))
    ext = url_path.suffix.lower()

    if ext in DIRECT_FILE_EXTS:
        raw_stem = url_path.stem or parsed.netloc
        dest = unique_path(inbox_dir, f"{today} - {raw_stem}", ext)
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Linux; Android 15) ObsidianMobileCapture/1.0"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp, dest.open("wb") as out:
            shutil.copyfileobj(resp, out)
        print(f"[+] Downloaded file to 00_Inbox: {dest.name}")
        return dest

    title = fetch_page_title(url)
    dest = unique_path(inbox_dir, f"{today} - {title}", ".md")
    now_iso = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    content = (
        f"---\n"
        f"type: web-capture\n"
        f"title: \"{sanitize_filename(title)}\"\n"
        f"source: \"{url}\"\n"
        f"created: {today}\n"
        f"updated: {today}\n"
        f"captured_at: {now_iso}\n"
        f"tags:\n"
        f"  - inbox\n"
        f"  - mobile-capture\n"
        f"---\n\n"
        f"# {sanitize_filename(title)}\n\n"
        f"* **Source**: [{url}]({url})\n"
        f"* **Captured**: `{now_iso}` via Android Termux Share Sheet\n\n"
        f"## Notes\n\n"
        f"- \n"
    )
    dest.write_text(content, encoding="utf-8")
    print(f"[+] Saved web capture to 00_Inbox: {dest.name}")
    return dest


def handle_file(file_arg: str, inbox_dir: Path) -> Path:
    src = Path(file_arg).expanduser().resolve()
    if not src.exists():
        raise FileNotFoundError(f"Shared file not found: {src}")

    today = datetime.date.today().isoformat()
    stem = src.stem
    if not re.match(r"^\d{4}-\d{2}-\d{2}", stem):
        stem = f"{today} - {stem}"
    dest = unique_path(inbox_dir, stem, src.suffix)
    shutil.copy2(src, dest)

    src_hash = sha256_file(src)
    dst_hash = sha256_file(dest)
    if src_hash != dst_hash:
        dest.unlink(missing_ok=True)
        raise RuntimeError("SHA-256 verification failed during file capture.")

    print(f"[+] Copied shared file to 00_Inbox: {dest.name}")
    print(f"    SHA-256 verified: {dst_hash[:16]}...")
    return dest


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: mobile_capture.py <url|file> <target>", file=sys.stderr)
        sys.exit(1)

    mode = sys.argv[1].strip().lower()
    target = sys.argv[2].strip()

    vault_root = resolve_vault_root()
    inbox_dir = vault_root / "00_Inbox"
    inbox_dir.mkdir(parents=True, exist_ok=True)

    if mode == "url":
        handle_url(target, inbox_dir)
    elif mode == "file":
        handle_file(target, inbox_dir)
    else:
        print(f"ERROR: Unsupported mode '{mode}'. Use 'url' or 'file'.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
