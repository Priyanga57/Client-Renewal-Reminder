# renewal_checker.py

import pandas as pd
from datetime import datetime
from config import EXPIRY_DAYS
from email_sender import send_email, send_summary

# 📥 Updated Google Sheet CSV export URL
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1vEZ9w3nkncT4-cFhEyU7ogHk705sc_KhWgY2HiejLv8/export?format=csv"

# 📊 Load the sheet
df = pd.read_csv(GOOGLE_SHEET_CSV_URL)
today = datetime.today().date()

# 📊 Summary to track what emails we send
summary = {
    "Expiring Soon": [],
    "Expired": []
}

# 🔁 Loop through each client record
for i, row in df.iterrows():
    client = str(row.get("Client Name", "")).strip()
    service = str(row.get("Service Type", "")).strip()
    due_date_str = str(row.get("Renewal Due Date", "")).strip()
    current_status = str(row.get("Status", "")).strip()
    contact_email = str(row.get("Contact Email", "")).strip()
    onetime = str(row.get("Is Onetime Access", "")).strip().lower()

    # ⛔ Skip rows that are "Transform" or One-time
    if current_status.lower() == "transform" or onetime == "yes":
        continue

    # 🗓️ Try to parse the due date
    try:
        due_date = pd.to_datetime(due_date_str, errors="coerce").date()
    except Exception:
        due_date = None

    # Skip if invalid due date
    if pd.isna(due_date) or due_date is None:
        continue

    # 📌 Determine what the new status should be
    if due_date < today:
        new_status = "Expired"
    elif (due_date - today).days <= EXPIRY_DAYS:
        new_status = "Expiring Soon"
    else:
        new_status = "Active"

    # ✉️ If there's a change in status and it's important, notify
    if new_status != current_status and new_status in ["Expired", "Expiring Soon"]:
        print(f"🔄 Updating: {client} → {new_status}")
        sent = send_email(client, service, due_date.strftime("%Y-%m-%d"), new_status, contact_email)
        if sent:
            summary[new_status].append(f"• {client} ({service}) - {due_date.strftime('%d %b %Y')}")

# 📬 Send daily summary email to internal team
total_sent = len(summary["Expiring Soon"]) + len(summary["Expired"])
if total_sent > 0:
    summary_text = f"""
📬 Daily Renewal Reminder Summary

🔸 Expiring Soon: {len(summary['Expiring Soon'])}
{chr(10).join(summary['Expiring Soon'])}

🔻 Expired: {len(summary['Expired'])}
{chr(10).join(summary['Expired'])}

🧾 Total reminders sent: {total_sent}
"""
    send_summary(summary_text)
else:
    print("✅ No reminders sent today.")
