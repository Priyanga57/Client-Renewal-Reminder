import smtplib
from email.mime.text import MIMEText

# 🔐 Gmail credentials
EMAIL_SENDER = "priyangaa7512@gmail.com"
EMAIL_PASSWORD = "pafx qkdp ivfi lcaj"
TEAM_EMAIL = "priyangaa7512@gmail.com"

# ✉️ Client Reminder
def send_email(client, service, due_date, status, to_email):
    emoji = {
        "Active": "✅",
        "Expiring Soon": "⏳",
        "Expired": "❌"
    }.get(status, "📌")

    subject = f"{emoji} Reminder: {service} for {client}"
    body = f"""\
Hello {client}, 👋

🔔 This is a friendly reminder.

🧾 Client: {client}  
🛠️ Service: {service}  
📅 Due Date: {due_date}  
📌 Status: {emoji} {status}

Please take action if needed.  
This is an automated message from our renewal system.

Thanks,  
Renewal Reminder Team 🤖
"""

    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"✅ Email sent to {to_email}")
        return True

    except Exception as e:
        print(f"❌ Failed to send to {to_email}: {e}")
        return False

# 📬 Daily Summary to Team
def send_summary(summary_text):
    subject = "📊 Daily Client Renewal Summary"
    try:
        msg = MIMEText(summary_text)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = TEAM_EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"📨 Summary sent to {TEAM_EMAIL}")
        return True

    except Exception as e:
        print(f"❌ Failed to send summary: {e}")
        return False
