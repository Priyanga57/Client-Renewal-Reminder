# renewal_checker.py

import pandas as pd
from datetime import datetime
from email_sender import send_email

# === Google Sheet (CSV Export Link) ===
GOOGLE_SHEET_CSV = "https://docs.google.com/spreadsheets/d/17_HyRiUA3UMSt6uOOS_vTa29YbeCIuSCbP6XjsuUdg8/export?format=csv"

def check_and_notify():
    try:
        df = pd.read_csv(GOOGLE_SHEET_CSV)
    except Exception as e:
        print(f"❌ Failed to load Google Sheet: {e}")
        return

    today = datetime.today()
    logs = []

    for i, row in df.iterrows():
        try:
            client = row["Client Name"]
            service = row["Service Type"]
            email = row["Contact Email"]
            due_date_str = row["Renewal Due Date"]
            current_status = row["Status"]

            if pd.isna(due_date_str) or pd.isna(email):
                continue

            due_date = pd.to_datetime(due_date_str)
            days_left = (due_date - today).days

            if days_left < 0:
                new_status = "Expired"
            elif days_left <= 30:
                new_status = "Expiring Soon"
            else:
                new_status = "Active"

            if new_status != current_status:
                print(f"🔄 Updating status for {client}: {current_status} → {new_status}")
                sent = send_email(client, service, due_date_str, new_status, email)
                if sent:
                    logs.append(f"{datetime.now()}, {client}, {email}, {new_status}")
        except Exception as e:
            print(f"⚠️ Skipped row {i} due to error: {e}")

    if logs:
        print("\n📝 Email log:")
        for entry in logs:
            print("•", entry)
    else:
        print("✅ No status updates. All clients are up-to-date.")

if __name__ == "__main__":
    check_and_notify()
