#!/usr/bin/env python3
"""
calendar_sync.py - Cross-Platform Calendar Reader via Private ICS Feeds
=======================================================================

Works with New Outlook / Microsoft 365, Google Calendar, and Apple iCloud
private ICS links across Windows, macOS, Linux, and Android Termux.

Configuration:
  Store private ICS URLs in ~/.gemini/tools/calendar.env (kept local/private):
    CALENDAR_ICS_PERSONAL="https://.../calendar.ics"
    CALENDAR_ICS_WORK="https://.../calendar.ics"
    CALENDAR_TIMEZONE="America/New_York"

Usage:
  python calendar_sync.py                    # Print today's schedule as Obsidian Markdown
  python calendar_sync.py --date 2026-11-24  # Print a specific date
  python calendar_sync.py --json             # Output structured JSON
  python calendar_sync.py --setup            # Interactive setup to save ICS URL(s)
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def resolve_vault_root() -> Path:
    env_vault = os.environ.get("CALM_SLATE_VAULT") or os.environ.get("VAULT_DIR")
    if env_vault and (Path(env_vault) / "06_Metadata" / "Gemini").exists():
        return Path(env_vault).resolve()
    script_vault = Path(__file__).resolve().parents[2]
    if (script_vault / "06_Metadata" / "Gemini").exists():
        return script_vault
    home_vault = Path.home() / "vault"
    if (home_vault / "06_Metadata" / "Gemini").exists():
        return home_vault.resolve()
    return script_vault


VAULT_ROOT = resolve_vault_root()
LOCAL_ENV_PATH = Path.home() / ".gemini" / "tools" / "calendar.env"
VAULT_ENV_PATH = VAULT_ROOT / "03_Resources" / "Automation & Scripts" / "calendar.env"

MEETING_LINK_RE = re.compile(
    r"(https://(?:[a-zA-Z0-9-]+\.)?(?:zoom\.us|teams\.microsoft\.com|teams\.live\.com|webex\.com|meet\.google\.com)/[^\s<>\"')]+)"
)


def load_env_files() -> dict:
    cfg = {}
    for env_path in (VAULT_ENV_PATH, LOCAL_ENV_PATH):
        if env_path.exists():
            for raw_line in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                val = v.strip().strip('"').strip("'")
                if val:
                    cfg[k.strip()] = val
    for key in ("CALENDAR_ICS_PERSONAL", "CALENDAR_ICS_WORK", "CALENDAR_ICS_EXTRA", "CALENDAR_TIMEZONE"):
        if os.environ.get(key):
            cfg[key] = os.environ[key].strip()
    return cfg


def get_configured_feeds(cfg: dict) -> list[tuple[str, str]]:
    feeds = []
    for label, key in (
        ("Personal", "CALENDAR_ICS_PERSONAL"),
        ("Work", "CALENDAR_ICS_WORK"),
        ("Extra", "CALENDAR_ICS_EXTRA"),
    ):
        raw = cfg.get(key, "").strip()
        if not raw or raw.startswith("PASTE_"):
            continue
        for idx, part in enumerate(raw.split(","), start=1):
            url = part.strip()
            if url:
                name = label if idx == 1 else f"{label}-{idx}"
                feeds.append((name, url))
    return feeds


def interactive_setup() -> None:
    print("=== Calendar Sync Setup (Private ICS Feeds) ===")
    print("Where to copy your read-only ICS URL:")
    print("  - New Outlook / M365: Settings > Calendar > Shared calendars > Publish a calendar")
    print("  - Google Calendar:    Settings > Integrate calendar > Secret address in iCal format\n")
    personal = input("Personal ICS URL [Enter to skip]: ").strip()
    work = input("Work ICS URL [Enter to skip]: ").strip()
    tz = input("Timezone (IANA format, e.g. America/New_York, America/Chicago) [default: America/New_York]: ").strip() or "America/New_York"

    LOCAL_ENV_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Private Calendar ICS Feeds (kept local, never share publicly)",
        f'CALENDAR_TIMEZONE="{tz}"',
    ]
    if personal:
        lines.append(f'CALENDAR_ICS_PERSONAL="{personal}"')
    if work:
        lines.append(f'CALENDAR_ICS_WORK="{work}"')
    LOCAL_ENV_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    try:
        os.chmod(LOCAL_ENV_PATH, 0o600)
    except OSError:
        pass
    print(f"\n[+] Saved calendar config to {LOCAL_ENV_PATH}")


def fetch_ics(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "CalmSlateCalendarSync/1.0"},
    )
    with urllib.request.urlopen(req, timeout=25) as resp:
        return resp.read()


def extract_meeting_link(location: str, description: str) -> str:
    for text in (location, description):
        if not text:
            continue
        m = MEETING_LINK_RE.search(text)
        if m:
            return m.group(1).rstrip(".,;>")
    return ""


def parse_events_for_date(ics_bytes: bytes, source: str, target_date: datetime.date, tz: ZoneInfo) -> list[dict]:
    try:
        from icalendar import Calendar
        import recurring_ical_events
    except ImportError:
        print(
            "ERROR: Missing dependencies 'icalendar' and 'recurring-ical-events'.\n"
            "Install via: pip install icalendar recurring-ical-events",
            file=sys.stderr,
        )
        sys.exit(1)

    cal = Calendar.from_ical(ics_bytes)
    day_start = datetime.datetime.combine(target_date, datetime.time.min, tzinfo=tz)
    day_end = day_start + datetime.timedelta(days=1)

    raw_events = recurring_ical_events.of(cal).between(day_start, day_end)
    parsed = []

    for comp in raw_events:
        summary = str(comp.get("summary", "(No Subject)")).strip() or "(No Subject)"
        location = str(comp.get("location", "")).strip()
        description = str(comp.get("description", "")).strip()
        dtstart_prop = comp.get("dtstart")
        dtend_prop = comp.get("dtend")
        if not dtstart_prop:
            continue

        start_val = dtstart_prop.dt
        end_val = dtend_prop.dt if dtend_prop else start_val

        is_all_day = isinstance(start_val, datetime.date) and not isinstance(start_val, datetime.datetime)
        if is_all_day:
            sort_dt = day_start
            start_str = "ALLDAY"
            end_str = "ALLDAY"
            time_label = "All Day"
        else:
            start_dt = start_val.replace(tzinfo=tz) if start_val.tzinfo is None else start_val.astimezone(tz)
            if isinstance(end_val, datetime.datetime):
                end_dt = end_val.replace(tzinfo=tz) if end_val.tzinfo is None else end_val.astimezone(tz)
            else:
                end_dt = start_dt
            if end_dt <= day_start or start_dt >= day_end:
                continue
            sort_dt = start_dt
            start_str = start_dt.strftime("%H:%M")
            end_str = end_dt.strftime("%H:%M")
            time_label = f"{start_dt.strftime('%I:%M %p').lstrip('0')} - {end_dt.strftime('%I:%M %p').lstrip('0')}"

        meeting_link = extract_meeting_link(location, description)
        parsed.append(
            {
                "source": source,
                "subject": summary,
                "norm_subject": summary.lower(),
                "all_day": is_all_day,
                "sort_key": sort_dt.isoformat(),
                "start": start_str,
                "end": end_str,
                "time_label": time_label,
                "location": location,
                "meeting_link": meeting_link,
            }
        )
    return parsed


def deduplicate(events: list[dict]) -> list[dict]:
    events.sort(key=lambda e: (e["all_day"] is False, e["sort_key"], e["norm_subject"]))
    seen = set()
    result = []
    for evt in events:
        key = f"{evt['start']}-{evt['end']}-{evt['norm_subject']}"
        if key not in seen:
            seen.add(key)
            result.append(evt)
    return result


def format_markdown(events: list[dict], target_date: datetime.date) -> str:
    if not events:
        return f"* *No scheduled meetings or calendar events found for {target_date.isoformat()}.*"

    lines = []
    for evt in events:
        loc_suffix = ""
        if evt["meeting_link"]:
            loc_suffix = f" ([Meeting Link]({evt['meeting_link']}))"
        elif evt["location"]:
            loc_suffix = f" (Location: {evt['location']})"
        lines.append(f"* **{evt['time_label']}**: {evt['subject']}{loc_suffix}")
    return "\n".join(lines)


def find_granola_notes_for_date(target_date: datetime.date) -> list[str]:
    granola_dir = VAULT_ROOT / "00_Inbox" / "Granola"
    if not granola_dir.exists():
        return []
    prefix = target_date.isoformat()
    return sorted(p.stem for p in granola_dir.glob(f"{prefix}*.md"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Cross-platform ICS calendar sync for Obsidian Daily Notes")
    parser.add_argument("--date", help="Target date YYYY-MM-DD (default: today)")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of Markdown")
    parser.add_argument("--setup", action="store_true", help="Run interactive ICS feed configuration")
    parser.add_argument("--with-granola", action="store_true", help="Also pull recent Granola notes via granola_sync.py")
    args = parser.parse_args()

    if args.setup:
        interactive_setup()
        return

    cfg = load_env_files()
    tz_name = cfg.get("CALENDAR_TIMEZONE", "America/New_York")
    try:
        tz = ZoneInfo(tz_name)
    except Exception:
        tz = ZoneInfo("UTC")

    if args.date:
        target_date = datetime.date.fromisoformat(args.date)
    else:
        target_date = datetime.datetime.now(tz).date()

    if args.with_granola:
        granola_script = Path(__file__).resolve().parent / "granola_sync.py"
        if granola_script.exists():
            subprocess.run(
                [sys.executable, str(granola_script), "--days", "3"],
                check=False,
                stdout=sys.stderr if args.json else None,
            )

    feeds = get_configured_feeds(cfg)
    if not feeds:
        granola_notes = find_granola_notes_for_date(target_date)
        msg = (
            "No calendar ICS feeds configured yet. Run:\n"
            f'  python "{Path(__file__).name}" --setup'
        )
        if args.json:
            print(json.dumps({"date": target_date.isoformat(), "configured": False, "events": [], "granola_notes": granola_notes, "message": msg}, indent=2))
        else:
            print(f"* *{msg}*")
            for note in granola_notes:
                print(f"* Meeting Note: [[{note}]]")
        return

    all_events = []
    errors = []
    for source, url in feeds:
        try:
            ics_bytes = fetch_ics(url)
            all_events.extend(parse_events_for_date(ics_bytes, source, target_date, tz))
        except urllib.error.URLError as exc:
            errors.append(f"{source}: {exc}")
        except Exception as exc:
            errors.append(f"{source}: {exc}")

    events = deduplicate(all_events)
    granola_notes = find_granola_notes_for_date(target_date)

    if args.json:
        print(
            json.dumps(
                {
                    "date": target_date.isoformat(),
                    "timezone": tz_name,
                    "configured": True,
                    "events": events,
                    "granola_notes": granola_notes,
                    "errors": errors,
                },
                indent=2,
            )
        )
    else:
        print(format_markdown(events, target_date))
        if granola_notes:
            for note in granola_notes:
                print(f"* Meeting Note: [[{note}]]")
        for err in errors:
            print(f"* *Calendar fetch warning ({err})*", file=sys.stderr)


if __name__ == "__main__":
    main()
