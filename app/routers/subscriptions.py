from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime
from app import database, crud, schemas
from app.dependencies import get_current_user
from app.permissions import is_admin_or_owner
import stripe
import os
import json

router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://car-wash-website-khaki.vercel.app")

# Stripe Price IDs from environment
STRIPE_PRICE_LITE = os.getenv("STRIPE_PRICE_LITE", "")
STRIPE_PRICE_PLUS = os.getenv("STRIPE_PRICE_PLUS", "")
STRIPE_PRICE_PRO = os.getenv("STRIPE_PRICE_PRO", "")

PRICE_MAP = {
    "lite": STRIPE_PRICE_LITE,
    "plus": STRIPE_PRICE_PLUS,
    "pro": STRIPE_PRICE_PRO,
}


@router.post("/activate-trial")
def activate_trial(
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(is_admin_or_owner),
):
    """Activate a 15-day free trial for the current user's business."""
    if not current_user.business_number:
        raise HTTPException(
            status_code=400, detail="No business associated with account"
        )

    existing = crud.get_business_subscription(db, current_user.business_number)
    if existing:
        raise HTTPException(
            status_code=400, detail="Business already has a subscription"
        )

    subscription = crud.activate_trial(db, current_user.business_number)
    return {
        "message": "Trial activated successfully",
        "status": subscription.status,
        "plan_type": subscription.plan_type,
        "trial_end_date": (
            subscription.trial_end_date.isoformat()
            if subscription.trial_end_date
            else None
        ),
    }


@router.post("/create-checkout")
def create_checkout(
    data: schemas.CreateCheckoutRequest,
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(is_admin_or_owner),
):
    """Create a Stripe Checkout Session for a subscription plan."""
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Stripe is not configured")

    if not current_user.business_number:
        raise HTTPException(
            status_code=400, detail="No business associated with account"
        )

    price_id = PRICE_MAP.get(data.plan)
    if not price_id:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid plan: {data.plan}. Must be lite, plus, or pro.",
        )

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            mode="subscription",
            success_url=f"{FRONTEND_URL}/plan-selection.html?payment=success",
            cancel_url=f"{FRONTEND_URL}/plan-selection.html?payment=cancelled",
            customer_email=current_user.email,
            metadata={
                "business_number": current_user.business_number,
                "plan": data.plan,
                "user_id": str(current_user.id),
            },
        )
        return {"checkout_url": session.url, "session_id": session.id}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=502, detail="Payment service unavailable")


@router.get("/status")
def get_subscription_status(
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(get_current_user),
):
    """Get current subscription status for the user's business."""
    if not current_user.business_number:
        return {
            "status": None,
            "plan_type": None,
            "is_trial": None,
            "trial_end_date": None,
            "days_remaining": None,
            "stripe_subscription_id": None,
        }

    subscription = crud.get_business_subscription(db, current_user.business_number)
    if not subscription:
        return {
            "status": None,
            "plan_type": None,
            "is_trial": None,
            "trial_end_date": None,
            "days_remaining": None,
            "stripe_subscription_id": None,
        }

    days_remaining = None
    if subscription.trial_end_date:
        delta = subscription.trial_end_date - datetime.utcnow()
        days_remaining = max(0, delta.days)

    return {
        "status": subscription.status,
        "plan_type": subscription.plan_type,
        "is_trial": subscription.is_trial,
        "trial_end_date": (
            subscription.trial_end_date.isoformat()
            if subscription.trial_end_date
            else None
        ),
        "days_remaining": days_remaining,
        "stripe_subscription_id": subscription.stripe_subscription_id,
    }


@router.get("/billing-history")
def get_billing_history(
    db: Session = Depends(database.get_db),
    current_user: database.User = Depends(is_admin_or_owner),
):
    """Retrieve billing history (invoices) from Stripe."""
    if not current_user.business_number:
        return {"invoices": []}

    subscription = crud.get_business_subscription(db, current_user.business_number)
    if not subscription or not subscription.stripe_customer_id:
        return {"invoices": []}

    if not stripe.api_key:
        return {"invoices": []}

    try:
        invoices = stripe.Invoice.list(
            customer=subscription.stripe_customer_id, limit=20
        )
        result = []
        for inv in invoices.data:
            result.append(
                {
                    "id": inv.id,
                    "amount_due": inv.amount_due / 100,
                    "amount_paid": inv.amount_paid / 100,
                    "currency": inv.currency,
                    "status": inv.status,
                    "created": inv.created,
                    "invoice_pdf": inv.invoice_pdf,
                }
            )
        return {"invoices": result}
    except stripe.error.StripeError:
        return {"invoices": []}


@router.post("/webhook")
async def subscription_webhook(
    request: Request, db: Session = Depends(database.get_db)
):
    """Handle Stripe subscription webhook events."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    try:
        if STRIPE_WEBHOOK_SECRET:
            event = stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_WEBHOOK_SECRET
            )
        else:
            event = json.loads(payload)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Webhook signature verification failed: {e}"
        )

    event_type = event.get("type") if isinstance(event, dict) else event["type"]
    data_object = (
        event.get("data", {}).get("object", {})
        if isinstance(event, dict)
        else event["data"]["object"]
    )

    if event_type == "checkout.session.completed":
        metadata = data_object.get("metadata", {})
        business_number = metadata.get("business_number")
        plan = metadata.get("plan")
        stripe_subscription_id = data_object.get("subscription")
        stripe_customer_id = data_object.get("customer")

        if business_number:
            subscription = crud.get_business_subscription(db, business_number)
            if subscription:
                subscription.status = "active"
                subscription.is_trial = False
                subscription.plan_type = plan or subscription.plan_type
                if stripe_subscription_id:
                    subscription.stripe_subscription_id = stripe_subscription_id
                if stripe_customer_id:
                    subscription.stripe_customer_id = stripe_customer_id
                subscription.updated_at = datetime.utcnow()
                db.commit()
            else:
                # Create new subscription record
                crud.update_subscription_from_webhook(
                    db,
                    business_number,
                    "active",
                    stripe_subscription_id=stripe_subscription_id,
                    plan_type=plan,
                )
            print(f"[SUBSCRIPTION] Business {business_number} activated plan: {plan}")

    elif event_type == "customer.subscription.deleted":
        stripe_subscription_id = data_object.get("id")
        if stripe_subscription_id:
            sub = (
                db.query(database.Subscription)
                .filter(
                    database.Subscription.stripe_subscription_id
                    == stripe_subscription_id
                )
                .first()
            )
            if sub:
                sub.status = "cancelled"
                sub.updated_at = datetime.utcnow()
                db.commit()
                print(f"[SUBSCRIPTION] Business {sub.business_number} cancelled")

    elif event_type == "invoice.payment_failed":
        stripe_subscription_id = data_object.get("subscription")
        if stripe_subscription_id:
            sub = (
                db.query(database.Subscription)
                .filter(
                    database.Subscription.stripe_subscription_id
                    == stripe_subscription_id
                )
                .first()
            )
            if sub:
                sub.status = "expired"
                sub.updated_at = datetime.utcnow()
                db.commit()
                print(
                    f"[SUBSCRIPTION] Business {sub.business_number} payment failed - expired"
                )

    return {"status": "ok"}
