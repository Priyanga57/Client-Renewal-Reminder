import smtplib
from email.mime.text import MIMEText

# -------------------
# 🔐 CONFIGURATION
# -------------------
EMAIL_SENDER = "your_email@gmail.com"           # Your Gmail ID
EMAIL_PASSWORD = "your_app_password"            # Gmail App Password (not your regular password)
TEAM_EMAIL = "your_team_email@example.com"      # Optional: Send internal summary to your team


# -------------------
# ✉️ SEND REMINDER TO CLIENT
# -------------------
def send_email(client, service, due_date, status, to_email):
    status_emoji = {
        "Active": "✅",
        "Expiring Soon": "⏳",
        "Expired": "❌"
    }.get(status, "📌")

    subject = f"{status_emoji} Reminder: {service} Renewal for {client}"
    body = f"""\
Hello {client}, 👋

🔔 This is a friendly reminder from our team.

🧾 Client: {client}  
🛠️ Service: {service}  
📅 Renewal Due Date: {due_date}  
📌 Current Status: {status_emoji} {status}

Please take action to renew if required.  
This message was generated automatically by our system.

Thanks,  
Client Renewal Team 🤖
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
        print(f"❌ Failed to send email to {to_email}: {e}")
        return False


# -------------------
# 📬 OPTIONAL: SEND DAILY SUMMARY TO TEAM
# -------------------
def send_summary(summary_text):
    subject = "📊 Daily Renewal Summary Report"
    body = f"""\
Hello Team, 👋

Here's your automated summary for today:  

{summary_text}

💡 Tip: You can view all records on the Streamlit Dashboard.

Best regards,  
Renewal Reminder System 🤖
"""

    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = TEAM_EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"📨 Daily summary sent to team ({TEAM_EMAIL})")
        return True

    except Exception as e:
        print(f"❌ Failed to send summary email: {e}")
        return False
