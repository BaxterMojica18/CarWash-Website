import os

# Twilio parameters would normally be loaded here
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# In mock mode, we just log the SMS to the console
MOCK_MODE = not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_PHONE_NUMBER)

def send_sms(to_number: str, body: str) -> bool:
    """
    Sends an SMS message. If Twilio credentials are not fully configured,
    it falls back to a mock mode which logs the SMS to the standard output.
    """
    if MOCK_MODE:
        print(f"\n{'='*50}")
        print(f"📱 MOCK SMS OUTBOUND")
        print(f"To: {to_number}")
        print(f"Message:\n{body}")
        print(f"{'='*50}\n")
        return True
    else:
        # Here we would import twilio and send the real SMS
        print("[SMS] Twilio implementation is currently commented out as per user request.")
        return True
        # try:
        #     # from twilio.rest import Client
        #     # client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        #     # message = client.messages.create(
        #     #     body=body,
        #     #     from_=TWILIO_PHONE_NUMBER,
        #     #     to=to_number
        #     # )
        #     # print(f"[SMS] Sent to {to_number}, SID: {message.sid}")
        #     # return True
        # except ImportError:
        #     print("[SMS Error] Twilio package not installed. Run: pip install twilio")
        #     return False
        # except Exception as e:
        #     print(f"[SMS Error] Failed to send SMS explicitly: {e}")
        #     return False

def send_order_status_sms(to_number: str, order_number: str, status: str):
    """Specific template for order status updates."""
    body = f"Car Wash Management: Your order #{order_number} is now '{status}'."
    return send_sms(to_number, body)

def send_queue_update_sms(to_number: str, reservation_number: str, position: int, status: str):
    """Specific template for queue updates."""
    if status == "completed":
        body = f"Car Wash Management: Your service for reservation #{reservation_number} is complete! You can pick up your vehicle."
    elif status == "in_progress":
        body = f"Car Wash Management: We've started working on your vehicle for reservation #{reservation_number}!"
    else:
        body = f"Car Wash Management: Update for reservation #{reservation_number}. You are now number {position} in the queue."
    
    return send_sms(to_number, body)
