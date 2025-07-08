# email_sender.py

import smtplib
from email.message import EmailMessage
from datetime import datetime
import os
from config import SENDER_EMAIL, APP_PASSWORD, SUMMARY_RECEIVER, LOG_FILE_PATH

# 📤 Send individual client email
def send_email(client_name, service_type, due_date, status, contact_email):
    try:
        msg = EmailMessage()
        msg['Subject'] = f"🔔 Renewal Reminder: {client_name} – {service_type}"
        msg['From'] = SENDER_EMAIL
        msg['To'] = contact_email

        # 📩 Email body
        body = f"""👋 Hello {client_name},

This is a friendly reminder that your service ⤵️
📌 Service: {service_type}
📅 Due Date: {due_date}
📊 Status: {status}

Please take necessary action to renew or reach out to our team if needed.

Thanks,  
Team Priyanga 💼
"""
        msg.set_content(body)

        # ✉️ Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)

        # 📝 Log email
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} | Sent to {client_name} ({contact_email}) | {service_type} | {status} | Due: {due_date}\n"
        os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)

        print(f"✅ Email sent to {client_name} ({contact_email})")
        return True

    except Exception as e:
        print(f"❌ Failed to send email to {client_name}: {e}")
        return False

# 📬 Send summary email to yourself or your team
def send_summary(summary_text):
    try:
        msg = EmailMessage()
        msg['Subject'] = "📈 Daily Renewal Summary Report"
        msg['From'] = SENDER_EMAIL
        msg['To'] = SUMMARY_RECEIVER

        msg.set_content(summary_text)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)

        print("📤 Daily summary sent successfully.")
        return True

    except Exception as e:
        print(f"❌ Failed to send daily summary: {e}")
        return False
