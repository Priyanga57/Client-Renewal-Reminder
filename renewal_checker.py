import pandas as pd
from datetime import datetime
from email_sender import send_email, send_summary

# 📄 Link to your Google Sheet (CSV export format)
sheet_url = "https://docs.google.com/spreadsheets/d/17_HyRiUA3UMSt6uOOS_vTa29YbeCIuSCbP6XjsuUdg8/export?format=csv"

# 📥 Load the sheet
df = pd.read_csv(sheet_url)

today = datetime.today().date()

# Summary tracking
summary = {
    "Expiring Soon": [],
    "Expired": []
}

# 🔁 Process each row
for i, row in df.iterrows():
    client = row["Client Name"]
    service = row["Service Type"]
    due_date_str = str(row["Renewal Due Date"]).strip()
    status = str(row["Status"]).strip()
    email = row["Contact Email"]

    try:
        due_date = pd.to_datetime(due_date_str).date()
    except Exception as e:
        print(f"❌ Invalid date for {client}: {due_date_str}")
        continue

    # Determine new status
    if due_date < today:
        new_status = "Expired"
    elif (due_date - today).days <= 30:
        new_status = "Expiring Soon"
    else:
        new_status = "Active"

    # 📬 If status changed, send email
    if new_status != status and new_status in ["Expiring Soon", "Expired"]:
        print(f"🔄 {client}: {status} → {new_status}")
        sent = send_email(client, service, due_date.strftime("%Y-%m-%d"), new_status, email)
        if sent:
            summary[new_status].append(f"- {client} ({service}) – Due: {due_date.strftime('%Y-%m-%d')}")

# 📨 Prepare and send daily summary to team
expiring_count = len(summary["Expiring Soon"])
expired_count = len(summary["Expired"])
total = expiring_count + expired_count

if total > 0:
    summary_text = f"""📋 Daily Renewal Summary ({today})\n
🔸 Expiring Soon: {expiring_count}
{chr(10).join(summary['Expiring Soon']) if expiring_count > 0 else "None"}

🔸 Expired: {expired_count}
{chr(10).join(summary['Expired']) if expired_count > 0 else "None"}

📬 Total Reminders Sent: {total}
🔁 Visit your dashboard to manage renewals.
"""
    send_summary(summary_text)
else:
    print("✅ No reminders sent today.")
