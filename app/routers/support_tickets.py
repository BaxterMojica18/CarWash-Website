from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from app import database
from app.dependencies import get_current_user
from app.email_service import send_email

router = APIRouter()


class TicketCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    concern: str


class TicketReply(BaseModel):
    reply: str


@router.post("/")
def create_ticket(data: TicketCreate, db: Session = Depends(database.get_db)):
    ticket = database.SupportTicket(
        name=data.name,
        email=data.email,
        phone=data.phone,
        concern=data.concern,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return {"message": "Ticket submitted successfully", "id": ticket.id}


@router.get("/")
def get_tickets(
    db: Session = Depends(database.get_db),
    current_user=Depends(get_current_user),
):
    roles = [r.name for r in current_user.roles]
    if not any(r in roles for r in ["superadmin", "owner"]):
        raise HTTPException(status_code=403, detail="Owner access required")
    tickets = db.query(database.SupportTicket).order_by(database.SupportTicket.created_at.desc()).all()
    return tickets


@router.get("/{ticket_id}")
def get_ticket(
    ticket_id: int,
    db: Session = Depends(database.get_db),
    current_user=Depends(get_current_user),
):
    roles = [r.name for r in current_user.roles]
    if not any(r in roles for r in ["superadmin", "owner"]):
        raise HTTPException(status_code=403, detail="Owner access required")
    ticket = db.query(database.SupportTicket).filter(database.SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.post("/{ticket_id}/reply")
def reply_ticket(
    ticket_id: int,
    data: TicketReply,
    db: Session = Depends(database.get_db),
    current_user=Depends(get_current_user),
):
    roles = [r.name for r in current_user.roles]
    if not any(r in roles for r in ["superadmin", "owner"]):
        raise HTTPException(status_code=403, detail="Owner access required")
    ticket = db.query(database.SupportTicket).filter(database.SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.reply = data.reply
    ticket.status = "replied"
    ticket.replied_at = datetime.utcnow()
    db.commit()

    html = f"""
    <div style="font-family:'Segoe UI',sans-serif;max-width:600px;margin:0 auto;background:#f5f5f5;padding:30px;">
        <div style="background:linear-gradient(135deg,#667eea,#764ba2);padding:25px;border-radius:12px 12px 0 0;text-align:center;">
            <h1 style="color:white;margin:0;font-size:22px;">Support Ticket Reply</h1>
        </div>
        <div style="background:white;padding:30px;border-radius:0 0 12px 12px;box-shadow:0 4px 20px rgba(0,0,0,0.1);">
            <p style="color:#555;">Hi <strong>{ticket.name}</strong>,</p>
            <p style="color:#555;">We've responded to your support ticket:</p>
            <div style="background:#f0f4ff;border-left:4px solid #667eea;padding:16px;border-radius:8px;margin:16px 0;">
                <p style="margin:0;color:#333;font-style:italic;">"{ticket.concern}"</p>
            </div>
            <p style="font-weight:600;color:#2c3e50;">Our Response:</p>
            <p style="color:#333;line-height:1.6;">{data.reply}</p>
            <p style="color:#888;font-size:13px;margin-top:24px;">If you have further questions, feel free to contact us again.</p>
        </div>
        <p style="text-align:center;color:#aaa;font-size:12px;margin-top:15px;">&copy; BuxTek Inc. 2025</p>
    </div>
    """
    send_email(ticket.email, "Re: Your Support Ticket", html, f"Hi {ticket.name},\n\nOur response:\n{data.reply}")

    return {"message": "Reply sent successfully"}


@router.patch("/{ticket_id}/close")
def close_ticket(
    ticket_id: int,
    db: Session = Depends(database.get_db),
    current_user=Depends(get_current_user),
):
    roles = [r.name for r in current_user.roles]
    if not any(r in roles for r in ["superadmin", "owner"]):
        raise HTTPException(status_code=403, detail="Owner access required")
    ticket = db.query(database.SupportTicket).filter(database.SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket.status = "closed"
    db.commit()
    return {"message": "Ticket closed"}
