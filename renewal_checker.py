import pandas as pd
from datetime import datetime
from email_sender import send_email, send_summary

# 🔗 Google Sheet link (as CSV)
sheet_url = "https://docs.google.com/spreadsheets/d/17_HyRiUA3UMSt6uOOS_vTa29YbeCIuSCbP6XjsuUdg8/export?format=csv"
df = pd.read_csv(sheet_url)

# 📅 Today’s date
today = datetime.today().date()

# 📦 Store reminders for daily summary
summary = {
    "Expiring Soon": [],
    "Expired": []
}

# 🔁 Loop through each row (client)
for _, row in df.iterrows():
    client = str(row.get("Client Name", "")).strip()
    service = str(row.get("Service Type", "")).strip()
    due_date_str = str(row.get("Renewal Due Date", "")).strip()
    status = str(row.get("Status", "")).strip()
    email = str(row.get("Contact Email", "")).strip()
    is_onetime = str(row.get("Is Onetime Access", "No")).strip().lower()

    # 🚫 Skip one-time clients
    if is_onetime == "yes":
        continue

    # 🧠 Safely parse and check the due date
    try:
        parsed = pd.to_datetime(due_date_str, errors="coerce")
        if pd.isna(parsed):
            continue
        due_date = parsed.date()
    except Exception:
        continue  # skip if completely broken
#One-time + AMC Reminder
    # 🔍 Determine the current status
    if due_date < today:
        new_status = "Expired"
    elif (due_date - today).days <= 30:
        new_status = "Expiring Soon"
    else:
        new_status = "Active"

    # 📤 Send reminder if status has changed and needs action
    if new_status != status and new_status in ["Expiring Soon", "Expired"]:
        print(f"🔔 {client} | {status} → {new_status}")
        sent = send_email(client, service, due_date.strftime("%Y-%m-%d"), new_status, email)
        if sent:
            summary[new_status].append(f"• {client} ({service}) – Due: {due_date.strftime('%Y-%m-%d')}")

# 📧 Send daily summary to you (the manager)
expiring_count = len(summary["Expiring Soon"])
expired_count = len(summary["Expired"])
total = expiring_count + expired_count

if total > 0:
    report = f"""
📅 **Daily Renewal Summary – {today.strftime('%Y-%m-%d')}** 📅

🔸 Expiring Soon: {expiring_count}
{chr(10).join(summary["Expiring Soon"]) or 'None'}

🔴 Expired: {expired_count}
{chr(10).join(summary["Expired"]) or 'None'}

📨 Total Reminders Sent: {total}
"""
    send_summary(report)
else:
    print("✅ No reminders sent today.")
    
with open("logs/daily_log.txt", "a") as log:
    log.write(f"{datetime.now()} ✅ Ran successfully\n")

