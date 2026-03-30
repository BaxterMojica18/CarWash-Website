import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USERNAME)


def send_email(to_email: str, subject: str, html_body: str, text_body: str = None):
    """Send an email via Gmail SMTP. Returns True on success, False on failure."""
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        print("[EMAIL] SMTP not configured — skipping email send")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Car Wash Management <{FROM_EMAIL}>"
    msg["To"] = to_email

    # Plain text fallback
    if text_body:
        msg.attach(MIMEText(text_body, "plain"))

    # HTML body
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, to_email, msg.as_string())
        print(f"[EMAIL] Sent to {to_email}: {subject}")
        return True
    except Exception as e:
        print(f"[EMAIL] Failed to send to {to_email}: {e}")
        return False


def send_password_reset_email(to_email: str, reset_token: str, base_url: str = "http://localhost:8000"):
    """Send a password reset email with a styled HTML template."""
    reset_url = f"{base_url}/reset-password.html?token={reset_token}"

    subject = "Reset Your Password — Car Wash Management"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f5f5f5; padding: 40px 20px;">
            <tr>
                <td align="center">
                    <table role="presentation" width="500" cellspacing="0" cellpadding="0" style="background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); overflow: hidden;">
                        <!-- Header -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 600;">🔒 Password Reset</h1>
                            </td>
                        </tr>
                        <!-- Body -->
                        <tr>
                            <td style="padding: 35px 30px;">
                                <p style="color: #333; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                                    Hi there,
                                </p>
                                <p style="color: #555; font-size: 15px; line-height: 1.6; margin: 0 0 25px 0;">
                                    We received a request to reset your password for your Car Wash Management account. Click the button below to set a new password:
                                </p>
                                <!-- Button -->
                                <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
                                    <tr>
                                        <td align="center" style="padding: 10px 0 25px 0;">
                                            <a href="{reset_url}" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; text-decoration: none; padding: 14px 40px; border-radius: 8px; font-size: 16px; font-weight: 600; letter-spacing: 0.3px;">
                                                Reset Password
                                            </a>
                                        </td>
                                    </tr>
                                </table>
                                <p style="color: #888; font-size: 13px; line-height: 1.5; margin: 0 0 15px 0;">
                                    This link will expire in <strong>15 minutes</strong>. If you didn't request a password reset, you can safely ignore this email.
                                </p>
                                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                                <p style="color: #aaa; font-size: 12px; line-height: 1.5; margin: 0;">
                                    If the button doesn't work, copy and paste this URL into your browser:<br>
                                    <a href="{reset_url}" style="color: #667eea; word-break: break-all;">{reset_url}</a>
                                </p>
                            </td>
                        </tr>
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #f9f9f9; padding: 20px 30px; text-align: center; border-top: 1px solid #eee;">
                                <p style="color: #aaa; font-size: 12px; margin: 0;">
                                    &copy; Car Wash Management System
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    text_body = f"""Password Reset Request

Hi there,

We received a request to reset your password for your Car Wash Management account.

Click this link to reset your password:
{reset_url}

This link will expire in 15 minutes. If you didn't request this, please ignore this email.

— Car Wash Management System
"""

    return send_email(to_email, subject, html_body, text_body)


def send_otp_email(to_email: str, otp_code: str):
    """Send a password reset OTP email with a styled HTML template."""
    subject = "Your Password Reset Code — Car Wash Management"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f5f5f5; padding: 40px 20px;">
            <tr>
                <td align="center">
                    <table role="presentation" width="500" cellspacing="0" cellpadding="0" style="background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); overflow: hidden;">
                        <!-- Header -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 600;">🔐 Password Reset Code</h1>
                            </td>
                        </tr>
                        <!-- Body -->
                        <tr>
                            <td style="padding: 35px 30px;">
                                <p style="color: #333; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                                    Hi there,
                                </p>
                                <p style="color: #555; font-size: 15px; line-height: 1.6; margin: 0 0 25px 0;">
                                    We received a request to reset your password. Use the following 6-digit code to verify your identity:
                                </p>
                                <!-- OTP Code -->
                                <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
                                    <tr>
                                        <td align="center" style="padding: 15px 0 30px 0;">
                                            <div style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; padding: 18px 50px; border-radius: 12px; font-size: 36px; font-weight: 700; letter-spacing: 12px; font-family: 'Courier New', monospace;">
                                                {otp_code}
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                                <p style="color: #888; font-size: 13px; line-height: 1.5; margin: 0 0 15px 0;">
                                    This code will expire in <strong>15 minutes</strong>. If you didn't request a password reset, you can safely ignore this email.
                                </p>
                                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                                <p style="color: #aaa; font-size: 12px; line-height: 1.5; margin: 0;">
                                    Do not share this code with anyone. Our team will never ask you for this code.
                                </p>
                            </td>
                        </tr>
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #f9f9f9; padding: 20px 30px; text-align: center; border-top: 1px solid #eee;">
                                <p style="color: #aaa; font-size: 12px; margin: 0;">
                                    &copy; Car Wash Management System
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    text_body = f"""Password Reset Code

Hi there,

We received a request to reset your password for your Car Wash Management account.

Your verification code is: {otp_code}

This code will expire in 15 minutes. If you didn't request this, please ignore this email.

— Car Wash Management System
"""

    return send_email(to_email, subject, html_body, text_body)

