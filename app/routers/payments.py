from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app import database, crud
from app.dependencies import get_current_user
from app.notification_service import notify_business_admins
import stripe
import os

router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://car-wash-website-khaki.vercel.app")


class CreatePaymentIntentRequest(BaseModel):
    payment_method: Optional[str] = "card"


class CreateCheckoutSessionRequest(BaseModel):
    payment_method: Optional[str] = "card"


def _is_demo(user) -> bool:
    return user.is_demo


@router.post("/create-payment-intent")
def create_payment_intent(
    data: CreatePaymentIntentRequest,
    db: Session = Depends(database.get_db),
    current_user=Depends(get_current_user),
):
    """Create a Stripe PaymentIntent from the user's current cart."""
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Stripe is not configured")

    # Get cart total
    cart_items = crud.get_cart_items(db, current_user.id)
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = sum(item.quantity * item.price_at_add for item in cart_items)
    amount_cents = int(total * 100)  # Stripe uses cents

    is_demo = _is_demo(current_user)

    try:
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency="usd",
            payment_method_types=["card"],
            metadata={
                "user_id": str(current_user.id),
                "user_email": current_user.email,
                "is_demo": str(is_demo),
            },
        )
        return {
            "client_secret": intent.client_secret,
            "amount": total,
            "amount_cents": amount_cents,
            "is_demo": is_demo,
        }
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/create-checkout-session")
def create_checkout_session(
    data: CreateCheckoutSessionRequest,
    db: Session = Depends(database.get_db),
    current_user=Depends(get_current_user),
):
    """Create a Stripe Checkout Session from the user's current cart."""
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Stripe is not configured")

    cart_items = crud.get_cart_items(db, current_user.id)
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    line_items = [
        {
            "price_data": {
                "currency": "usd",
                "product_data": {"name": item.product_service.name},
                "unit_amount": int(item.price_at_add * 100),
            },
            "quantity": item.quantity,
        }
        for item in cart_items
    ]

    is_demo = _is_demo(current_user)

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=f"{FRONTEND_URL}/client-dashboard.html?payment=success",
            cancel_url=f"{FRONTEND_URL}/cart.html?payment=cancelled",
            customer_email=current_user.email,
            metadata={
                "user_id": str(current_user.id),
                "user_email": current_user.email,
                "is_demo": str(is_demo),
            },
        )
        return {
            "checkout_url": session.url,
            "session_id": session.id,
            "is_demo": is_demo,
        }
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(database.get_db)):
    """Handle Stripe webhook events — auto-create order on successful payment."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    try:
        if STRIPE_WEBHOOK_SECRET:
            event = stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_WEBHOOK_SECRET
            )
        else:
            import json

            event = json.loads(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {e}")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = int(session["metadata"].get("user_id", 0))
        if user_id:
            user = db.query(database.User).filter(database.User.id == user_id).first()
            if user:
                order = crud.create_order_from_cart(db, user_id, "stripe")
                if order:
                    print(
                        f"[STRIPE] Order {order.order_number} created for user {user_id}"
                    )
                    # Notify business admins of payment received
                    amount = session.get("amount_total", 0) / 100
                    notify_business_admins(
                        db,
                        user.business_number,
                        "Payment Received",
                        f"Payment of ${amount:.2f} received for order #{order.order_number}",
                        "payment",
                    )

    elif event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        user_id = int(intent["metadata"].get("user_id", 0))
        if user_id:
            user = db.query(database.User).filter(database.User.id == user_id).first()
            if user:
                order = crud.create_order_from_cart(db, user_id, "stripe")
                if order:
                    print(
                        f"[STRIPE] Order {order.order_number} created via PaymentIntent for user {user_id}"
                    )
                    # Notify business admins of payment received
                    amount = intent.get("amount", 0) / 100
                    notify_business_admins(
                        db,
                        user.business_number,
                        "Payment Received",
                        f"Payment of ${amount:.2f} received for order #{order.order_number}",
                        "payment",
                    )

    return {"status": "ok"}


@router.get("/config")
def get_stripe_config():
    """Return Stripe publishable key for frontend."""
    pub_key = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
    if not pub_key:
        raise HTTPException(
            status_code=500, detail="Stripe publishable key not configured"
        )
    return {"publishable_key": pub_key}
