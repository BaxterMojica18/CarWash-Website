from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from app import schemas, crud, database
from app.dependencies import get_current_user
from app.routers.auth import get_current_user_optional_query
from app.permissions import has_permission
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from PIL import Image
import io

router = APIRouter()

@router.post("/", response_model=schemas.Invoice)
def create_invoice(invoice: schemas.InvoiceCreate, db: Session = Depends(database.get_db), current_user = Depends(has_permission("manage_invoices"))):
    return crud.create_invoice(db, invoice, current_user.id)

@router.get("/", response_model=List[schemas.Invoice])
def get_invoices(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    from app.permissions import get_user_permissions
    perms = get_user_permissions(current_user)
    if 'view_invoices' not in perms and 'manage_invoices' not in perms:
        raise HTTPException(status_code=403, detail="Permission denied")
    return crud.get_invoices(db)

@router.get("/{invoice_id}", response_model=schemas.Invoice)
def get_invoice(invoice_id: int, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    from app.permissions import get_user_permissions
    perms = get_user_permissions(current_user)
    if 'view_invoices' not in perms and 'manage_invoices' not in perms:
        raise HTTPException(status_code=403, detail="Permission denied")
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

@router.get("/{invoice_id}/jpg")
def download_invoice_jpg(invoice_id: int, db: Session = Depends(database.get_db), current_user = Depends(get_current_user_optional_query)):
    from PIL import Image, ImageDraw, ImageFont
    
    invoice = crud.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # Create image
    img = Image.new('RGB', (850, 1100), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 28)
        font_normal = ImageFont.truetype("arial.ttf", 16)
        font_bold = ImageFont.truetype("arialbd.ttf", 18)
    except:
        font_title = ImageFont.load_default()
        font_normal = ImageFont.load_default()
        font_bold = ImageFont.load_default()
    
    # Draw invoice content
    y = 50
    draw.text((250, y), f"Invoice #{invoice.invoice_number}", fill='black', font=font_title)
    
    y += 70
    draw.text((50, y), f"Date: {invoice.date.strftime('%Y-%m-%d %H:%M')}", fill='black', font=font_normal)
    y += 35
    draw.text((50, y), f"Customer: {invoice.customer_name}", fill='black', font=font_normal)
    y += 35
    draw.text((50, y), f"Location: {invoice.location.name}", fill='black', font=font_normal)
    
    # Draw table
    y += 60
    table_top = y
    
    # Table header background
    draw.rectangle([(40, y), (810, y + 35)], fill='#4CAF50')
    
    # Table header text
    draw.text((50, y + 8), "Item", fill='white', font=font_bold)
    draw.text((350, y + 8), "Qty", fill='white', font=font_bold)
    draw.text((480, y + 8), "Unit Price", fill='white', font=font_bold)
    draw.text((650, y + 8), "Subtotal", fill='white', font=font_bold)
    
    y += 35
    
    # Table rows
    for item in invoice.items:
        product = db.query(database.ProductService).filter(database.ProductService.id == item.product_service_id).first()
        item_name = product.name if product else f"Item #{item.product_service_id}"
        
        # Alternate row background
        draw.rectangle([(40, y), (810, y + 30)], fill='#F5F5DC')
        
        draw.text((50, y + 5), item_name[:35], fill='black', font=font_normal)
        draw.text((350, y + 5), str(item.quantity), fill='black', font=font_normal)
        draw.text((480, y + 5), f"${item.unit_price:.2f}", fill='black', font=font_normal)
        draw.text((650, y + 5), f"${item.subtotal:.2f}", fill='black', font=font_normal)
        y += 30
    
    # Table border
    draw.rectangle([(40, table_top), (810, y)], outline='black', width=2)
    
    # Vertical lines
    draw.line([(340, table_top), (340, y)], fill='black', width=1)
    draw.line([(470, table_top), (470, y)], fill='black', width=1)
    draw.line([(640, table_top), (640, y)], fill='black', width=1)
    
    # Total
    y += 40
    draw.text((480, y), f"TOTAL: ${invoice.total_amount:.2f}", fill='black', font=font_bold)
    
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='JPEG', quality=95)
    img_buffer.seek(0)
    
    return StreamingResponse(
        img_buffer,
        media_type="image/jpeg",
        headers={'Content-Disposition': f'attachment; filename="invoice-{invoice.invoice_number}.jpg"'}
    )

@router.get("/dashboard/stats", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    return crud.get_dashboard_stats(db)
