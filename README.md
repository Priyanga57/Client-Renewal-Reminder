# 🔁 Automated Client Renewal Reminder System

## 🎯 Project Objective

To develop a system that tracks client onboarding and subscription renewal dates (e.g., domain, server, website services) and **automatically sends reminder notifications** to your team or clients before expiry.

---

## 📁 Folder Structure

renewal_reminder/
├── client_data.xlsx # 📋 Main client data file (Excel)
├── config.py # ⚙️ Email & system settings
├── renewal_checker.py # ⏳ Updates renewal statuses (Expiring Soon, Expired)
├── email_sender.py # 📬 Sends reminder emails to team/clients
├── dashboard.py # 📊 Streamlit dashboard for live monitoring
├── logs/ # 📂 Log files of emails sent
└── README.md # 📘 This file

1.YAML

---

## 🚀 Features

✅ Track clients’ services (Domain, Server, Web Dev, Marketing, etc.)  
✅ Supports one-time & renewable cycles (monthly, yearly, half-yearly, 15 days)  
✅ Automatically flags services as `Expiring Soon` or `Expired`  
✅ Sends clean reminder emails with emojis (no HTML, no payments)  
✅ 📊 Streamlit-based dashboard to filter by service, date, or status  
✅ Maintains logs of emails sent  

---

## 🛠️ Installation & Setup

1. **Install Dependencies**

```bash
pip install pandas openpyxl streamlit

Configure Email Settings

Edit config.py:

python
Copy
Edit
EMAIL_SENDER = "your_email@gmail.com"           # your Gmail address
EMAIL_PASSWORD = "your_gmail_app_password"       # use Gmail App Password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
🔒 Use Gmail App Passwords: Generate Here
