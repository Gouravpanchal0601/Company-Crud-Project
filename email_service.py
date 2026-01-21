# # email_service.py
# import os
# import smtplib
# from email.message import EmailMessage
# from dotenv import load_dotenv

# load_dotenv()

# SMTP_HOST = os.getenv("SMTP_HOST")
# SMTP_PORT = int(os.getenv("SMTP_PORT"))
# SMTP_USER = os.getenv("SMTP_USER")
# SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
# EMAIL_FROM = os.getenv("EMAIL_FROM")

# def send_otp_email(to_email: str, otp: str):
#     msg = EmailMessage()
#     msg["Subject"] = "Your OTP Code"
#     msg["From"] = EMAIL_FROM
#     msg["To"] = to_email
#     msg.set_content(f"""
# Your OTP code is: {otp}

# This OTP will expire in 10 minutes.
# If you did not request this, ignore this email.
# """)

#     with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
#         server.starttls()
#         server.login(SMTP_USER, SMTP_PASSWORD)
#         server.send_message(msg)
