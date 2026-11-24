#!/usr/bin/env python3
"""
ynab_sync.py - YNAB Budget Dashboard Synchronizer & Transaction CLI
Synchronizes your YNAB budget with 02_Areas/Finance & Admin/YNAB Budget Dashboard.md,
logs transactions via the YNAB REST API v1, and manages category targets/notes.
"""

import argparse
import datetime
import json
import os
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

def _resolve_vault_root() -> str:
    # 1. Resolve relative to this script inside the vault (works on Windows, Linux, Android Termux)
    script_vault = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    if os.path.exists(os.path.join(script_vault, "06_Metadata", "Gemini")):
        return script_vault
    # 2. Termux / Linux vault symlink
    home_vault = os.path.join(os.path.expanduser("~"), "vault")
    if os.path.exists(os.path.join(home_vault, "06_Metadata", "Gemini")):
        return os.path.realpath(home_vault)
    # 3. Environment variable fallback
    env_vault = os.environ.get("WAYPOST_VAULT") or os.environ.get("VAULT_DIR")
    if env_vault and os.path.exists(os.path.join(env_vault, "06_Metadata", "Gemini")):
        return os.path.abspath(env_vault)
    return script_vault

VAULT_ROOT = _resolve_vault_root()
DASHBOARD_PATH = os.path.join(
    VAULT_ROOT, "02_Areas", "Finance & Admin", "YNAB Budget Dashboard.md"
)
BACKUP_ROOT = os.path.join(VAULT_ROOT, "06_Metadata", "Gemini", "Backups")

ENV_SEARCH_PATHS = [
    os.path.join(VAULT_ROOT, "03_Resources", "Automation & Scripts", "ynab-sync", ".env"),
    os.path.join(os.path.expanduser("~"), ".gemini", "tools", "ynab-sync", ".env"),
]

YNAB_API_BASE = "https://api.ynab.com/v1"


def load_api_key() -> str:
    key = (os.environ.get("YNAB_API_KEY") or os.environ.get("YNAB_ACCESS_TOKEN") or "").strip()
    if key:
        return key
    for path in ENV_SEARCH_PATHS:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        k, v = line.split("=", 1)
                        if k.strip() in ("YNAB_API_KEY", "YNAB_ACCESS_TOKEN"):
                            val = v.strip().strip('"').strip("'")
                            if val and not val.startswith("PASTE_"):
                                return val
    return ""


def save_api_key(token: str) -> None:
    token = token.strip()
    for path in [
        os.path.join(VAULT_ROOT, "03_Resources", "Automation & Scripts", "ynab-sync", ".env"),
        os.path.join(os.path.expanduser("~"), ".gemini", "tools", "ynab-sync", ".env"),
    ]:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"YNAB_API_KEY={token}\n")
    print("[+] Saved YNAB_API_KEY to both local .gemini/tools/ynab-sync/.env and vault sync folder.")


def ynab_request(method: str, endpoint: str, token: str, payload: dict = None) -> dict:
    url = f"{YNAB_API_BASE}{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"YNAB API HTTP {e.code} on {method} {endpoint}: {err_body}")


def get_target_budget_id(token: str, preferred_name: str = "Antigravity") -> str:
    res = ynab_request("GET", "/budgets", token)
    budgets = res.get("data", {}).get("budgets", [])
    if not budgets:
        raise RuntimeError("No budgets found in YNAB account.")
    for b in budgets:
        if preferred_name.lower() in b.get("name", "").lower():
            return b["id"]
    return budgets[0]["id"]


def fmt_currency(milliunits: int) -> str:
    dollars = (milliunits or 0) / 1000.0
    if dollars < 0:
        return f"-${abs(dollars):,.2f}"
    return f"${dollars:,.2f}"


def backup_file(filepath: str) -> str:
    if not os.path.exists(filepath):
        return ""
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    ts_str = datetime.datetime.now().strftime("%H%M%S")
    dest_dir = os.path.join(BACKUP_ROOT, today_str)
    os.makedirs(dest_dir, exist_ok=True)
    fname = os.path.basename(filepath)
    dest_path = os.path.join(dest_dir, f"{ts_str}_{fname}.bak.md")
    shutil.copy2(filepath, dest_path)
    return dest_path


def log_transaction(
    token: str,
    budget_id: str,
    account_name: str,
    payee_name: str,
    amount_dollars: float,
    category_name: str = None,
    memo: str = "",
    date_str: str = None,
    is_inflow: bool = False,
) -> dict:
    acc_res = ynab_request("GET", f"/budgets/{budget_id}/accounts", token)
    accounts = [
        a for a in acc_res.get("data", {}).get("accounts", []) if not a.get("deleted")
    ]
    matched_acc = None
    for a in accounts:
        if account_name.lower() in a["name"].lower():
            matched_acc = a
            break
    if not matched_acc:
        # Fallback to TVA Checking or first checking/creditCard
        for a in accounts:
            if a.get("type") in ("checking", "creditCard"):
                matched_acc = a
                break

    cat_id = None
    if category_name:
        cat_res = ynab_request("GET", f"/budgets/{budget_id}/categories", token)
        for grp in cat_res.get("data", {}).get("category_groups", []):
            for c in grp.get("categories", []):
                if not c.get("deleted") and category_name.lower() in c["name"].lower():
                    cat_id = c["id"]
                    break
            if cat_id:
                break

    milliunits = int(round(abs(amount_dollars) * 1000))
    if not is_inflow:
        milliunits = -milliunits

    tx_date = date_str or datetime.date.today().strftime("%Y-%m-%d")
    tx_payload = {
        "transaction": {
            "account_id": matched_acc["id"],
            "date": tx_date,
            "amount": milliunits,
            "payee_name": payee_name,
            "memo": memo,
            "cleared": "uncleared",
            "approved": True,
        }
    }
    if cat_id:
        tx_payload["transaction"]["category_id"] = cat_id

    res = ynab_request("POST", f"/budgets/{budget_id}/transactions", token, tx_payload)
    print(
        f"[+] Logged YNAB transaction: {payee_name} ({fmt_currency(milliunits)}) on {tx_date} in account '{matched_acc['name']}'"
    )
    return res


def update_category_goal_or_note(
    token: str, budget_id: str, category_search: str, goal_target_dollars: float, note_append: str = ""
) -> dict:
    cat_res = ynab_request("GET", f"/budgets/{budget_id}/categories", token)
    target_cat = None
    for grp in cat_res.get("data", {}).get("category_groups", []):
        for c in grp.get("categories", []):
            if not c.get("deleted") and category_search.lower() in c["name"].lower():
                target_cat = c
                break
        if target_cat:
            break

    if not target_cat:
        # Fallback: find a sinking fund or household category or unused starter category to rename/repurpose
        for grp in cat_res.get("data", {}).get("category_groups", []):
            for c in grp.get("categories", []):
                if not c.get("deleted") and "stuff i forgot" in c["name"].lower():
                    target_cat = c
                    break
            if target_cat:
                break

    if not target_cat:
        raise RuntimeError(f"Could not find category matching '{category_search}' in YNAB.")

    milliunits = int(round(goal_target_dollars * 1000))
    patch_body = {
        "category": {
            "name": target_cat["name"]
            if "stuff i forgot" not in target_cat["name"].lower()
            else "🐜 Cook's Pest Control (~$800/yr)",
            "note": note_append or f"Target: ${goal_target_dollars:,.2f}/year (~${goal_target_dollars/12.0:,.2f}/month)",
            "goal_target": milliunits,
        }
    }
    res = ynab_request(
        "PATCH", f"/budgets/{budget_id}/categories/{target_cat['id']}", token, patch_body
    )
    print(f"[+] Updated YNAB category '{patch_body['category']['name']}' with target ${goal_target_dollars:,.2f}")
    return res


def update_transaction_payee(
    token: str, budget_id: str, old_payee: str, new_payee: str, amount_dollars: float = None
) -> dict:
    tx_res = ynab_request("GET", f"/budgets/{budget_id}/transactions", token)
    transactions = tx_res.get("data", {}).get("transactions", [])
    target_tx = None
    target_milliunits = -int(round(abs(amount_dollars) * 1000)) if amount_dollars is not None else None
    for t in sorted(transactions, key=lambda x: x.get("date", ""), reverse=True):
        if old_payee.lower() in (t.get("payee_name") or "").lower():
            if target_milliunits is None or t.get("amount") == target_milliunits:
                target_tx = t
                break
    if not target_tx:
        raise RuntimeError(f"Could not find transaction with payee matching '{old_payee}'")
    tx_id = target_tx["id"]
    put_payload = {
        "transaction": {
            "account_id": target_tx["account_id"],
            "date": target_tx["date"],
            "amount": target_tx["amount"],
            "payee_name": new_payee,
            "category_id": target_tx.get("category_id"),
            "memo": target_tx.get("memo"),
            "cleared": target_tx.get("cleared", "uncleared"),
            "approved": target_tx.get("approved", True),
        }
    }
    res = ynab_request("PUT", f"/budgets/{budget_id}/transactions/{tx_id}", token, put_payload)
    print(f"[+] Updated YNAB transaction {tx_id}: payee changed from '{target_tx.get('payee_name')}' to '{new_payee}'")
    return res


def sync_dashboard(token: str) -> str:
    budget_id = get_target_budget_id(token)
    month_res = ynab_request("GET", f"/budgets/{budget_id}/months/current", token)
    month_data = month_res.get("data", {}).get("month", {})

    acc_res = ynab_request("GET", f"/budgets/{budget_id}/accounts", token)
    accounts = [
        a for a in acc_res.get("data", {}).get("accounts", []) if not a.get("deleted") and not a.get("closed")
    ]

    cat_res = ynab_request("GET", f"/budgets/{budget_id}/categories", token)
    cat_groups = [
        g
        for g in cat_res.get("data", {}).get("category_groups", [])
        if not g.get("deleted") and not g.get("hidden") and "delete" not in g.get("name", "").lower()
    ]

    tx_res = ynab_request("GET", f"/budgets/{budget_id}/transactions", token)
    transactions = [
        t for t in tx_res.get("data", {}).get("transactions", []) if not t.get("deleted")
    ]
    transactions.sort(key=lambda x: x.get("date", ""), reverse=True)
    recent_tx = transactions[:15]

    now_iso = datetime.datetime.now().isoformat()
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    budget_month = month_data.get("month", today_str[:8] + "01")

    rta = fmt_currency(month_data.get("to_be_budgeted", 0))
    aom = month_data.get("age_of_money") or 0
    income = fmt_currency(month_data.get("income", 0))
    budgeted = fmt_currency(month_data.get("budgeted", 0))
    activity = fmt_currency(month_data.get("activity", 0))

    overspent = []
    for grp in cat_groups:
        if grp["name"] == "Hidden Categories":
            continue
        for c in grp.get("categories", []):
            if c.get("deleted") or c.get("hidden"):
                continue
            bal = c.get("balance", 0)
            if bal < 0:
                overspent.append((c["name"], grp["name"], fmt_currency(bal), fmt_currency(c.get("activity", 0))))

    lines = [
        "---",
        "type: finance",
        "system: ynab",
        "tags:",
        "  - finance",
        "  - budget",
        "  - personal",
        "created: 2026-11-02",
        f"updated: {today_str}",
        "---",
        "",
        "# 💳 YNAB Budget Dashboard",
        "",
        f"> *Last Synced: `{now_iso}` | Budget Month: `{budget_month}`*",
        "",
        "## 📊 Quick Financial Pulse",
        f"* **Ready to Assign**:: **{rta}**",
        f"* **Age of Money**:: **{aom} days**",
        f"* **Total Monthly Income**:: {income}",
        f"* **Total Monthly Budgeted**:: {budgeted}",
        f"* **Total Monthly Activity**:: {activity}",
        "",
        "---",
        "",
    ]

    if overspent:
        lines.append("> [!WARNING] Overspent Categories (Action Required)")
        for cname, gname, bal_str, act_str in overspent:
            lines.append(f"> * **{cname}** ({gname}): **{bal_str}** (Activity: {act_str})")
        lines.extend(["", "---", ""])

    lines.extend(
        [
            "## 🏦 Account Balances",
            "| Account | Type | Working Balance | Cleared | Uncleared |",
            "| :--- | :--- | :---: | :---: | :---: |",
        ]
    )
    for a in accounts:
        lines.append(
            f"| {a['name']} | {a['type']} | **{fmt_currency(a.get('balance', 0))}** | {fmt_currency(a.get('cleared_balance', 0))} | {fmt_currency(a.get('uncleared_balance', 0))} |"
        )

    lines.extend(["", "---", "", "## 📁 Category Budgets & Balances", ""])
    for grp in cat_groups:
        cats = [c for c in grp.get("categories", []) if not c.get("deleted") and not c.get("hidden")]
        if not cats:
            continue
        lines.extend(
            [
                f"### {grp['name']}",
                "| Category | Budgeted | Spent / Activity | Available Balance |",
                "| :--- | :---: | :---: | :---: |",
            ]
        )
        for c in cats:
            bal = c.get("balance", 0)
            warn = " ⚠️" if bal < 0 else ""
            lines.append(
                f"| {c['name']} | {fmt_currency(c.get('budgeted', 0))} | {fmt_currency(c.get('activity', 0))} | **{fmt_currency(bal)}**{warn} |"
            )
        lines.append("")

    lines.extend(
        [
            "---",
            "",
            "## ⏱️ Recent Transactions",
            "| Date | Payee | Category | Account | Amount | Memo |",
            "| :--- | :--- | :--- | :--- | :---: | :--- |",
        ]
    )
    for t in recent_tx:
        lines.append(
            f"| {t.get('date', '')} | {t.get('payee_name') or ''} | {t.get('category_name') or 'Uncategorized'} | {t.get('account_name') or ''} | {fmt_currency(t.get('amount', 0))} | {t.get('memo') or ''} |"
        )

    bak = backup_file(DASHBOARD_PATH)
    with open(DASHBOARD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[+] Updated YNAB Budget Dashboard: {DASHBOARD_PATH}")
    if bak:
        print(f"[+] Pre-edit backup saved: {bak}")
    return DASHBOARD_PATH


def main():
    parser = argparse.ArgumentParser(description="YNAB Vault Sync & Transaction Tool")
    parser.add_argument("--set-key", help="Save YNAB Personal Access Token to .env")
    parser.add_argument("--log-expense", action="store_true", help="Log an outflow transaction")
    parser.add_argument("--account", default="TVA Checking", help="Account name")
    parser.add_argument("--payee", help="Payee name")
    parser.add_argument("--category", help="Category name")
    parser.add_argument("--amount", type=float, help="Dollar amount (e.g. 4.77)")
    parser.add_argument("--memo", default="", help="Transaction memo")
    parser.add_argument("--date", default=None, help="Transaction date YYYY-MM-DD")
    parser.add_argument("--update-payee-from", help="Old payee to search and update")
    parser.add_argument("--update-payee-to", help="New payee name")
    parser.add_argument("--resolve-pending", action="store_true", help="Execute pending Keep YNAB tasks and sync")
    args = parser.parse_args()

    if args.set_key:
        save_api_key(args.set_key)

    token = load_api_key()
    if not token:
        print(
            "[-] ERROR: YNAB_API_KEY not found in .env. Run:\n"
            '    python ynab_sync.py --set-key "YOUR_YNAB_PERSONAL_ACCESS_TOKEN"',
            file=sys.stderr,
        )
        sys.exit(2)

    budget_id = get_target_budget_id(token)

    if args.update_payee_from and args.update_payee_to:
        update_transaction_payee(
            token,
            budget_id,
            old_payee=args.update_payee_from,
            new_payee=args.update_payee_to,
            amount_dollars=args.amount,
        )

    if args.log_expense:
        if not args.payee or args.amount is None:
            print("[-] --payee and --amount are required with --log-expense", file=sys.stderr)
            sys.exit(1)
        log_transaction(
            token,
            budget_id,
            account_name=args.account,
            payee_name=args.payee,
            amount_dollars=args.amount,
            category_name=args.category,
            memo=args.memo,
            date_str=args.date,
            is_inflow=False,
        )

    if args.resolve_pending:
        # 1. Log $4.77 Circle K Starbucks drink (2026-11-04)
        log_transaction(
            token,
            budget_id,
            account_name="TVA",
            payee_name="Circle K",
            amount_dollars=4.77,
            category_name="Dining Out",
            memo="Starbucks drink (logged from Google Keep)",
            date_str="2026-11-04",
            is_inflow=False,
        )
        # 2. Configure Cook's Pest Control (~$800/year target)
        update_category_goal_or_note(
            token,
            budget_id,
            category_search="Cook's Pest Control",
            goal_target_dollars=66.67,
            note_append="Cook's Pest Control: ~$800/year target (~$66.67/month)",
        )

    sync_dashboard(token)


if __name__ == "__main__":
    main()
