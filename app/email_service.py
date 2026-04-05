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



FRONTEND_URL = os.getenv("FRONTEND_URL", "https://car-wash-website-khaki.vercel.app")


def _base_template(header_emoji: str, header_title: str, body_html: str) -> str:
    return f"""
    <!DOCTYPE html><html><head><meta charset="UTF-8"></head>
    <body style="margin:0;padding:0;font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;background:#f5f5f5;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#f5f5f5;padding:40px 20px;">
        <tr><td align="center">
        <table role="presentation" width="500" cellspacing="0" cellpadding="0" style="background:#fff;border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,0.1);overflow:hidden;">
            <tr><td style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:30px;text-align:center;">
                <h1 style="color:#fff;margin:0;font-size:24px;font-weight:600;">{header_emoji} {header_title}</h1>
            </td></tr>
            <tr><td style="padding:35px 30px;">{body_html}</td></tr>
            <tr><td style="background:#f9f9f9;padding:20px 30px;text-align:center;border-top:1px solid #eee;">
                <p style="color:#aaa;font-size:12px;margin:0;">&copy; Car Wash Management System</p>
            </td></tr>
        </table>
        </td></tr>
    </table>
    </body></html>
    """


def _action_button(label: str, url: str) -> str:
    return f"""
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
        <tr><td align="center" style="padding:15px 0 25px 0;">
            <a href="{url}" style="display:inline-block;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;text-decoration:none;padding:14px 40px;border-radius:8px;font-size:16px;font-weight:600;">{label}</a>
        </td></tr>
    </table>
    """


def _items_table(items: list) -> str:
    rows = "".join(
        f"<tr><td style='padding:8px 12px;border-bottom:1px solid #eee;'>{i.get('name','')}</td>"
        f"<td style='padding:8px 12px;border-bottom:1px solid #eee;text-align:center;'>x{i.get('quantity',1)}</td>"
        f"<td style='padding:8px 12px;border-bottom:1px solid #eee;text-align:right;color:#667eea;font-weight:600;'>${i.get('subtotal',0):.2f}</td></tr>"
        for i in items
    )
    return f"""
    <table width="100%" cellspacing="0" cellpadding="0" style="border-collapse:collapse;margin:15px 0;">
        <tr style="background:#f8f9fa;">
            <th style="padding:10px 12px;text-align:left;font-size:13px;color:#555;">Item</th>
            <th style="padding:10px 12px;text-align:center;font-size:13px;color:#555;">Qty</th>
            <th style="padding:10px 12px;text-align:right;font-size:13px;color:#555;">Subtotal</th>
        </tr>
        {rows}
    </table>
    """


def send_order_confirmation_client(to_email: str, order_number: str, items: list, total: float, payment_method: str):
    items_html = _items_table(items)
    body = f"""
        <p style="color:#333;font-size:16px;margin:0 0 15px 0;">Hi there,</p>
        <p style="color:#555;font-size:15px;margin:0 0 20px 0;">Your order has been placed successfully!</p>
        <div style="background:#f8f9fa;border-radius:8px;padding:15px;margin-bottom:20px;">
            <p style="margin:0 0 8px 0;"><strong>Order #:</strong> {order_number}</p>
            <p style="margin:0 0 8px 0;"><strong>Payment:</strong> {payment_method or 'N/A'}</p>
            <p style="margin:0;"><strong>Total:</strong> <span style="color:#667eea;font-size:18px;font-weight:700;">${total:.2f}</span></p>
        </div>
        {items_html}
        <p style="color:#888;font-size:13px;">We'll notify you as your order status changes. Thank you!</p>
    """
    return send_email(to_email, f"Order Confirmed — {order_number}", _base_template("🧾", "Order Confirmed!", body))


def send_order_notification_owner(to_email: str, order_number: str, client_email: str, items: list, total: float, payment_method: str):
    order_url = f"{FRONTEND_URL}/order-management.html"
    items_html = _items_table(items)
    body = f"""
        <p style="color:#333;font-size:16px;margin:0 0 15px 0;">New order received!</p>
        <div style="background:#f8f9fa;border-radius:8px;padding:15px;margin-bottom:20px;">
            <p style="margin:0 0 8px 0;"><strong>Order #:</strong> {order_number}</p>
            <p style="margin:0 0 8px 0;"><strong>Client:</strong> {client_email}</p>
            <p style="margin:0 0 8px 0;"><strong>Payment:</strong> {payment_method or 'N/A'}</p>
            <p style="margin:0;"><strong>Total:</strong> <span style="color:#667eea;font-size:18px;font-weight:700;">${total:.2f}</span></p>
        </div>
        {items_html}
        {_action_button('View Order', order_url)}
    """
    return send_email(to_email, f"New Order Received — {order_number}", _base_template("🛒", "New Order Received", body))


def send_order_status_update(to_email: str, order_number: str, new_status: str):
    status_colors = {
        'accepted': '#28a745', 'processing': '#007bff',
        'completed': '#20c997', 'cancelled': '#dc3545', 'delayed': '#f0932b'
    }
    color = status_colors.get(new_status, '#667eea')
    body = f"""
        <p style="color:#333;font-size:16px;margin:0 0 15px 0;">Hi there,</p>
        <p style="color:#555;font-size:15px;margin:0 0 20px 0;">Your order status has been updated:</p>
        <div style="background:#f8f9fa;border-radius:8px;padding:20px;text-align:center;margin-bottom:20px;">
            <p style="margin:0 0 8px 0;font-size:15px;"><strong>Order #:</strong> {order_number}</p>
            <span style="display:inline-block;background:{color};color:#fff;padding:8px 24px;border-radius:20px;font-weight:700;font-size:16px;text-transform:uppercase;">{new_status}</span>
        </div>
        <p style="color:#888;font-size:13px;">Thank you for choosing us!</p>
    """
    return send_email(to_email, f"Order Update — {order_number} is now {new_status.upper()}", _base_template("📦", "Order Status Updated", body))


def send_reservation_confirmation_client(to_email: str, reservation_number: str, service_name: str, location_name: str, vehicle_plate: str, queue_position: int):
    body = f"""
        <p style="color:#333;font-size:16px;margin:0 0 15px 0;">Hi there,</p>
        <p style="color:#555;font-size:15px;margin:0 0 20px 0;">Your reservation has been confirmed!</p>
        <div style="background:#f8f9fa;border-radius:8px;padding:15px;margin-bottom:20px;">
            <p style="margin:0 0 8px 0;"><strong>Reservation #:</strong> {reservation_number}</p>
            <p style="margin:0 0 8px 0;"><strong>Service:</strong> {service_name}</p>
            <p style="margin:0 0 8px 0;"><strong>Location:</strong> {location_name}</p>
            <p style="margin:0 0 8px 0;"><strong>Vehicle Plate:</strong> {vehicle_plate}</p>
            <p style="margin:0;"><strong>Queue Position:</strong> <span style="color:#667eea;font-size:18px;font-weight:700;">#{queue_position}</span></p>
        </div>
        <p style="color:#888;font-size:13px;">We'll notify you as your reservation status changes. See you soon!</p>
    """
    return send_email(to_email, f"Reservation Confirmed — {reservation_number}", _base_template("🚗", "Reservation Confirmed!", body))


def send_reservation_notification_owner(to_email: str, reservation_number: str, client_email: str, service_name: str, location_name: str, vehicle_plate: str, queue_position: int):
    queue_url = f"{FRONTEND_URL}/queue-management.html"
    body = f"""
        <p style="color:#333;font-size:16px;margin:0 0 15px 0;">New reservation received!</p>
        <div style="background:#f8f9fa;border-radius:8px;padding:15px;margin-bottom:20px;">
            <p style="margin:0 0 8px 0;"><strong>Reservation #:</strong> {reservation_number}</p>
            <p style="margin:0 0 8px 0;"><strong>Client:</strong> {client_email}</p>
            <p style="margin:0 0 8px 0;"><strong>Service:</strong> {service_name}</p>
            <p style="margin:0 0 8px 0;"><strong>Location:</strong> {location_name}</p>
            <p style="margin:0 0 8px 0;"><strong>Vehicle Plate:</strong> {vehicle_plate}</p>
            <p style="margin:0;"><strong>Queue Position:</strong> #{queue_position}</p>
        </div>
        {_action_button('View Queue', queue_url)}
    """
    return send_email(to_email, f"New Reservation — {reservation_number}", _base_template("📅", "New Reservation Received", body))


def send_reservation_status_update(to_email: str, reservation_number: str, new_status: str):
    status_colors = {
        'accepted': '#28a745', 'in_progress': '#007bff',
        'completed': '#20c997', 'cancelled': '#dc3545', 'delayed': '#f0932b'
    }
    color = status_colors.get(new_status, '#667eea')
    body = f"""
        <p style="color:#333;font-size:16px;margin:0 0 15px 0;">Hi there,</p>
        <p style="color:#555;font-size:15px;margin:0 0 20px 0;">Your reservation status has been updated:</p>
        <div style="background:#f8f9fa;border-radius:8px;padding:20px;text-align:center;margin-bottom:20px;">
            <p style="margin:0 0 8px 0;font-size:15px;"><strong>Reservation #:</strong> {reservation_number}</p>
            <span style="display:inline-block;background:{color};color:#fff;padding:8px 24px;border-radius:20px;font-weight:700;font-size:16px;text-transform:uppercase;">{new_status.replace('_', ' ')}</span>
        </div>
        <p style="color:#888;font-size:13px;">Thank you for choosing us!</p>
    """
    return send_email(to_email, f"Reservation Update — {reservation_number} is now {new_status.upper()}", _base_template("🔧", "Reservation Status Updated", body))
