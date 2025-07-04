import pandas as pd
from datetime import datetime, timedelta
from email_sender import send_email, send_summary

# Your Google Sheet as CSV export link
sheet_url = "https://docs.google.com/spreadsheets/d/17_HyRiUA3UMSt6uOOS_vTa29YbeCIuSCbP6XjsuUdg8/export?format=csv"

# Load data
df = pd.read_csv(sheet_url)

# Current date
today = datetime.today().date()

# Track how many emails sent
summary = {
    "Expiring Soon": 0,
    "Expired": 0
}

# Loop through each client
for i, row in df.iterrows():
    client = row["Client Name"]
    service = row["Service Type"]
    cycle = str(row["Renewal Cycle"]).strip().lower()
    due_date_str = row["Renewal Due Date"]
    status = row["Status"]
    email = row["Contact Email"]

    try:
        due_date = pd.to_datetime(due_date_str).date()
    except:
        print(f"⚠️ Invalid date for {client}")
        continue

    # Determine new status
    if due_date < today:
        new_status = "Expired"
    elif (due_date - today).days <= 30:
        new_status = "Expiring Soon"
    else:
        new_status = "Active"

    # If status has changed → send reminder
    if new_status != status:
        print(f"🔄 {client}: {status} → {new_status}")
        sent = send_email(client, service, due_date_str, new_status, email)
        if sent:
            summary[new_status] += 1

# Send summary to internal team
total = summary["Expiring Soon"] + summary["Expired"]
summary_text = (
    f"📋 Daily Renewal Summary ({today}):\n"
    f"🔸 Expiring Soon: {summary['Expiring Soon']}\n"
    f"🔸 Expired: {summary['Expired']}\n"
    f"📬 Total Reminders Sent: {total}"
)

# Optional: send to team email
if total > 0:
    send_summary(summary_text)
else:
    print("✅ No expiring/expired clients today.")
