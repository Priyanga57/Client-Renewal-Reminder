import pandas as pd
from datetime import datetime
from email_sender import send_email, send_summary

# Google Sheet CSV Export Link
sheet_url = "https://docs.google.com/spreadsheets/d/17_HyRiUA3UMSt6uOOS_vTa29YbeCIuSCbP6XjsuUdg8/export?format=csv"
df = pd.read_csv(sheet_url)

today = datetime.today().date()

summary = {
    "Expiring Soon": [],
    "Expired": [],
    "Expiring Today": []
}

for _, row in df.iterrows():
    client = row.get("Client Name", "").strip()
    service = row.get("Service Type", "").strip()
    due_date_str = str(row.get("Renewal Due Date", "")).strip()
    status = str(row.get("Status", "")).strip()
    email = row.get("Contact Email", "").strip()
    is_onetime = str(row.get("Is Onetime Access", "")).strip().lower()

    # Skip onetime access
    if is_onetime in ["yes", "true", "1"]:
        continue

    # Parse and validate due date
    try:
        due_date = pd.to_datetime(due_date_str, errors="coerce").date()
    except:
        due_date = None

    if pd.isna(due_date) or not due_date_str:
        continue

    # Determine new status
    days_remaining = (due_date - today).days

    if days_remaining < 0:
        new_status = "Expired"
    elif days_remaining == 0:
        new_status = "Expiring Today"
    elif days_remaining <= 30:
        new_status = "Expiring Soon"
    else:
        new_status = "Active"

    # Only send notification if new status is actionable
    if new_status in ["Expired", "Expiring Soon", "Expiring Today"] and new_status != status:
        print(f"🔔 {client}: {status} → {new_status}")
        sent = send_email(client, service, due_date.strftime("%Y-%m-%d"), new_status, email)
        if sent:
            summary[new_status].append(f"• {client} ({service}) – Due: {due_date.strftime('%Y-%m-%d')}")

# Send daily summary to admin
total_reminders = len(summary["Expired"]) + len(summary["Expiring Soon"]) + len(summary["Expiring Today"])

if total_reminders > 0:
    summary_text = f"""📬 Daily Renewal Summary ({today})
    
🔸 Expiring Today: {len(summary['Expiring Today'])}
{chr(10).join(summary["Expiring Today"])}

🔸 Expiring Soon (within 30 days): {len(summary['Expiring Soon'])}
{chr(10).join(summary["Expiring Soon"])}

🔸 Expired: {len(summary['Expired'])}
{chr(10).join(summary["Expired"])}

Total Reminders Sent: {total_reminders}
"""
    send_summary(summary_text)
else:
    print("✅ No reminders sent today.")
