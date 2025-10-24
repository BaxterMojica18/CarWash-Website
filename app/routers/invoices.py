from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, database
from app.routers.auth import get_current_user
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

router = APIRouter()

@router.post("/", response_model=schemas.Invoice)
def create_invoice(invoice: schemas.InvoiceCreate, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    return crud.create_invoice(db, invoice, current_user.id)

@router.get("/", response_model=List[schemas.Invoice])
def get_invoices(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    return crud.get_invoices(db)

@router.get("/{invoice_id}", response_model=schemas.Invoice)
def get_invoice(invoice_id: int, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    invoice = crud.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.get("/{invoice_id}/pdf")
def download_invoice_pdf(invoice_id: int, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    invoice = crud.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph(f"<b>Invoice Receipt #{invoice.invoice_number}</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Invoice details
    details = Paragraph(f"<b>Date:</b> {invoice.date.strftime('%Y-%m-%d %H:%M')}<br/>"
                       f"<b>Customer:</b> {invoice.customer_name}<br/>"
                       f"<b>Location:</b> {invoice.location.name}", styles['Normal'])
    elements.append(details)
    elements.append(Spacer(1, 0.3*inch))
    
    # Items table
    data = [['Item', 'Quantity', 'Unit Price', 'Subtotal']]
    for item in invoice.items:
        product = db.query(database.ProductService).filter(database.ProductService.id == item.product_service_id).first()
        item_name = product.name if product else f"Item #{item.product_service_id}"
        data.append([item_name, str(item.quantity), f"${item.unit_price:.2f}", f"${item.subtotal:.2f}"])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Total
    total = Paragraph(f"<b>TOTAL: ${invoice.total_amount:.2f}</b>", styles['Heading2'])
    elements.append(total)
    
    doc.build(elements)
    buffer.seek(0)
    
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={'Content-Disposition': f'attachment; filename="invoice-{invoice.invoice_number}.pdf"'}
    )

@router.get("/dashboard/stats", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    return crud.get_dashboard_stats(db)
