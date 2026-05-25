import smtplib #Python lib used to send mail transfer
import os #Use to access .env folder

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.quoprimime import body_check

from dotenv import load_dotenv
load_dotenv()#Help to load env folder

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_signup_email(revicer_email):
    subject = " Welcome to VaultCore Banking — Account Created Successfully"

    body = """
   Dear Customer,

Welcome to VaultCore Banking.

Your account has been successfully created and is now active.

You can now securely:

Access your banking dashboard
Manage accounts
Perform transactions
Monitor fraud alerts
Receive real-time banking notifications

If you did not create this account, please contact our support team immediately.

Thank you for choosing VaultCore Banking.

Regards,
VaultCore Banking Team
    """

    msg = MIMEMultipart() #create empty email container

    msg['From'] = EMAIL_USER
    msg['To'] = revicer_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:

        server = smtplib.SMTP(
            'smtp.gmail.com',
            587
        ) #Use to connect to email server 587 TLS secure email sending port

        server.starttls() #Enable encription

        server.login(
            EMAIL_USER,
            EMAIL_PASS
        )

        server.send_message(msg)

        server.quit()

        print("Signup email sent successfully")

    except Exception as e:

        print(
            "Email sending failed:",
            e
        )

def send_login_email(receiver_email):
    subject = "VaultCore Security Alert — New Login Detected"

    body = """
    Dear Customer,

A new login was detected in your VaultCore Banking account.

If this was you, no further action is required.

If you do not recognize this login activity, please secure your account immediately by changing your password.

For security reasons, never share your banking credentials with anyone.

Regards,
VaultCore Banking Security Team
"""

    msg = MIMEMultipart()

    msg['From'] = EMAIL_USER
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:

        server = smtplib.SMTP(
            'smtp.gmail.com',
            587
        )

        server.starttls()

        server.login(
            EMAIL_USER,
            EMAIL_PASS
        )

        server.send_message(msg)

        server.quit()

        print("Login email sent successfully")
    except Exception as e:
        print("Email sending failed:",e)

def send_transaction_email(
        revicer_email,
        transaction_type,
        amount
):

    subject = ("VaultCore Transaction Alert")

    body = f"""
    Dear Customer,
    A transaction has been successfully processed in your account.

Transaction Details:

Transaction Type: {transaction_type}
Amount: ₹{amount}

If this transaction was not performed by you, please contact support immediately.

Regards,
VaultCore Banking Team
"""
    msg = MIMEMultipart()

    msg['FROM'] = EMAIL_USER
    msg['To'] = revicer_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:

        server = smtplib.SMTP(
            'smtp.gmail.com',
            587
        )

        server.starttls()

        server.login(
            EMAIL_USER,
            EMAIL_PASS
        )

        server.send_message(msg)

        server.quit()

        print(
            "Transaction email sent successfully"
        )

    except Exception as e:

        print(
            "Email sending failed:",
            e
        )

def send_fraud_alert_email(
        receiver_email,
        fraud_reason,
        amount
):
    subject = (
        "⚠ VaultCore Fraud Alert Detected"
    )

    body = f"""
Dear Customer,
A suspicious transaction activity has been detected in your account.

Fraud Detection Details:

Reason: {fraud_reason}
Amount: ₹{amount}

If this transaction was NOT performed by you, please secure your account immediately.

Recommended Actions:
- Change your password
- Contact support
- Review recent transactions

Regards,
VaultCore Banking Security Team
"""

    msg = MIMEMultipart()

    msg['From'] = EMAIL_USER
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(
        MIMEText(body, 'plain')
    )

    try:

        server = smtplib.SMTP(
            'smtp.gmail.com',
            587
        )

        server.starttls()

        server.login(
            EMAIL_USER,
            EMAIL_PASS
        )

        server.send_message(msg)

        server.quit()

        print(
            "Fraud alert email sent successfully"
        )

    except Exception as e:

        print(
            "Email sending failed:",
            e
        )


