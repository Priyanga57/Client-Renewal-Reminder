

import smtplib
from email.mime.text import MIMEText

# Replace these with your actual Gmail credentials (use app password)
EMAIL_SENDER = "priyangaa7512@gmail.com"
EMAIL_PASSWORD = "Priyang@5757"  # Use App Password from Google
EMAIL_SUBJECT = "🔔 Client Subscription Renewal Reminder"

def send_email(client, service, due_date, status, to_email):
    status_emoji = {
        "Active": "✅",
        "Expiring Soon": "⏳",
        "Expired": "❌"
    }.get(status, "📌")

    body = f"""
Hi {client}, 👋

This is a reminder for your upcoming service renewal:

🔧 Service: {service}  
📅 Due Date: {due_date}  
📌 Status: {status_emoji} {status}

Please take the necessary action to continue uninterrupted service.

Thank you,  
Team Automation 🤖
"""

    msg = MIMEText(body)
    msg['Subject'] = f"{status_emoji} Renewal Reminder - {service}"
    msg['From'] = EMAIL_SENDER
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"📨 Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
        return False
