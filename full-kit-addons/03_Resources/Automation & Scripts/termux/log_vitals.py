#!/usr/bin/env python3
"""
log_vitals.py - Quick Health, BP & Cognitive Energy Logger for Termux:Widget
============================================================================

Prompts for Blood Pressure, Cognitive Energy (1-5), Headache (0-10), Body Pain (0-10),
and Interventions/Notes, creates a mandatory pre-edit backup, updates today's Daily Note
inline Dataview fields, and outputs adaptive pacing recommendations if vitals are elevated.
"""

import datetime
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from daily_note_init import ensure_daily_note, resolve_vault_root


def backup_file(vault_root: Path, filepath: Path) -> Path:
    today_str = datetime.date.today().isoformat()
    ts_str = datetime.datetime.now().strftime("%H%M%S")
    dest_dir = vault_root / "06_Metadata" / "Gemini" / "Backups" / today_str
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{ts_str}_{filepath.stem}.bak.md"
    shutil.copy2(filepath, dest)
    return dest


def update_field(text: str, field_label: str, value: str, section_heading: str = None) -> str:
    if not value:
        return text
    pattern = re.compile(rf"^(\*\s+\*\*{re.escape(field_label)}\*\*::).*$", re.MULTILINE)
    if section_heading:
        idx = text.find(section_heading)
        if idx != -1:
            next_idx = text.find("\n### ", idx + len(section_heading))
            end_idx = next_idx if next_idx != -1 else len(text)
            segment = text[idx:end_idx]
            new_segment, count = pattern.subn(rf"\1 {value}", segment, count=1)
            if count:
                return text[:idx] + new_segment + text[end_idx:]
    new_text, _ = pattern.subn(rf"\1 {value}", text, count=1)
    return new_text


def parse_bp(bp_str: str) -> tuple[int, int] | None:
    m = re.match(r"^\s*(\d{2,3})\s*/\s*(\d{2,3})\s*$", bp_str or "")
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def main() -> None:
    today = datetime.date.today()
    vault_root = resolve_vault_root()
    note_path = ensure_daily_note(today)

    hour = datetime.datetime.now().hour
    default_period = "Morning" if hour < 15 else "Evening"

    print(f"=== Health & Cognitive Energy Check ({today.isoformat()}) ===")
    print("Press Enter on any field to skip.\n")

    bp = input("Blood Pressure (e.g. 122/78): ").strip()
    energy = input("Cognitive Energy (1-5): ").strip()
    impact = input("Functional Impact [1=Normal, 2=Slowed Down, 3=Stopped Work]: ").strip()
    impact_map = {"1": "Normal", "2": "Slowed Down", "3": "Stopped Work"}
    impact_val = impact_map.get(impact, impact)

    period_in = input(f"Headache period (M=Morning, E=Evening) [default: {default_period[0]}]: ").strip().lower()
    period = "Evening" if period_in.startswith("e") else ("Morning" if period_in.startswith("m") else default_period)

    headache = input(f"{period} Headache Score (0-10): ").strip()
    headache_loc = input(f"{period} Headache Trigger / Location: ").strip() if headache else ""

    body_pain = input("Body Pain Score (0-10): ").strip()
    body_loc = input("Body Pain Type / Location: ").strip() if body_pain else ""

    meds = input("Interventions / Meds: ").strip()
    notes = input("Health Notes: ").strip()

    if not any([bp, energy, impact_val, headache, body_pain, meds, notes]):
        print("\n[=] Nothing entered. Daily Note unchanged.")
        return

    bak = backup_file(vault_root, note_path)
    content = note_path.read_text(encoding="utf-8", errors="replace")

    if bp:
        content = update_field(content, "Blood Pressure (BP)", bp)
    if energy:
        content = update_field(content, "Cognitive Energy (1-5)", energy)
    if impact_val:
        content = update_field(
            content,
            "Functional Impact",
            f"{impact_val} # Normal / Slowed Down / Stopped Work",
        )
    if headache:
        sec = f"### {period} Headaches & Cranial Symptoms"
        content = update_field(content, f"{period} Headache Score (0-10)", headache, section_heading=sec)
        if headache_loc:
            content = update_field(content, "Trigger / Location", headache_loc, section_heading=sec)
    if body_pain:
        sec = "### Body & Musculoskeletal Pain"
        content = update_field(content, "Body Pain Score (0-10)", body_pain, section_heading=sec)
        if body_loc:
            content = update_field(content, "Pain Type / Location", body_loc, section_heading=sec)
    if meds:
        content = update_field(content, "Interventions / Meds", meds)
    if notes:
        content = update_field(content, "Health Notes", notes)

    content = re.sub(r"^updated:.*$", f"updated: {today.isoformat()}", content, count=1, flags=re.MULTILINE)
    note_path.write_text(content, encoding="utf-8")

    print(f"\n[+] Logged vitals into {note_path.name}")
    print(f"    Backup saved: {bak}")

    # Adaptive cognitive pacing check
    warnings = []
    parsed_bp = parse_bp(bp)
    if parsed_bp and (parsed_bp[0] >= 140 or parsed_bp[1] >= 90):
        warnings.append(f"BP is elevated ({bp}). Hydrate, take a seated break, and avoid high-stress blocks.")
    try:
        if headache and float(headache) >= 5:
            warnings.append(f"Headache is {headache}/10. Shift deep coding/architecture to light review or rest.")
    except ValueError:
        pass
    try:
        if energy and float(energy) <= 2:
            warnings.append(f"Cognitive energy is {energy}/5. Stick strictly to 1 concrete micro-step at a time.")
    except ValueError:
        pass

    if warnings:
        print("\n[!] Adaptive Pacing Alert:")
        for w in warnings:
            print(f"    - {w}")


if __name__ == "__main__":
    main()
