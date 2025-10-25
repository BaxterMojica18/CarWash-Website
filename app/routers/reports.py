from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.database import get_db, Invoice, ReportCache
from app.routers.auth import get_current_user, get_current_user_optional_query
from datetime import datetime, timedelta
from typing import Optional
from fastapi.responses import StreamingResponse
import io
import csv

router = APIRouter()

@router.get("/sales")
def get_sales_report(
    period: str = "day",
    date: Optional[str] = None,
    month: Optional[int] = None,
    year: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    start_month: Optional[int] = None,
    end_month: Optional[int] = None,
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    from app.database import InvoiceItem, ProductService
    user_id = current_user.id
    query = db.query(Invoice).filter(Invoice.user_id == user_id)
    
    # Range filters
    if period == "day_range" and start_date and end_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        query = query.filter(func.date(Invoice.date).between(start.date(), end.date()))
    elif period == "month_range" and start_month and end_month and year:
        query = query.filter(
            extract('year', Invoice.date) == year,
            extract('month', Invoice.date).between(start_month, end_month)
        )
    elif period == "year_range" and start_year and end_year:
        query = query.filter(extract('year', Invoice.date).between(start_year, end_year))
    # Single filters
    elif period == "day" and date:
        target_date = datetime.strptime(date, "%Y-%m-%d")
        query = query.filter(func.date(Invoice.date) == target_date.date())
    elif period == "month" and month and year:
        query = query.filter(
            extract('month', Invoice.date) == month,
            extract('year', Invoice.date) == year
        )
    elif period == "year" and year:
        query = query.filter(extract('year', Invoice.date) == year)
    
    invoices = query.order_by(Invoice.date).all()
    
    total_sales = sum(inv.total_amount for inv in invoices)
    total_invoices = len(invoices)
    
    # Chart data - group by date
    chart_data = {}
    for inv in invoices:
        date_key = inv.date.strftime("%Y-%m-%d")
        chart_data[date_key] = chart_data.get(date_key, 0) + inv.total_amount
    
    # Category breakdown
    category_sales = {}
    product_category_sales = {}
    for inv in invoices:
        items = db.query(InvoiceItem).filter(InvoiceItem.invoice_id == inv.id).all()
        for item in items:
            product = db.query(ProductService).filter(ProductService.id == item.product_service_id).first()
            if product:
                category = product.type
                category_sales[category] = category_sales.get(category, 0) + item.subtotal
                
                if product.type == "product" and product.quantity_unit:
                    product_key = f"{product.name} ({product.quantity_unit})"
                    product_category_sales[product_key] = product_category_sales.get(product_key, 0) + item.subtotal
    
    report_data = {
        "period": period,
        "filter": {"date": date, "month": month, "year": year, "start_date": start_date, "end_date": end_date},
        "total_sales": total_sales,
        "total_invoices": total_invoices,
        "chart_data": {"labels": list(chart_data.keys()), "values": list(chart_data.values())},
        "category_data": {"labels": list(category_sales.keys()), "values": list(category_sales.values())},
        "product_category_data": {"labels": list(product_category_sales.keys()), "values": list(product_category_sales.values())},
        "invoices": [
            {
                "id": inv.id,
                "invoice_number": inv.invoice_number,
                "date": inv.date.isoformat(),
                "customer_name": inv.customer_name,
                "total_amount": inv.total_amount
            }
            for inv in invoices
        ]
    }
    
    # Cache report
    cache = ReportCache(
        user_id=user_id,
        report_type="sales",
        filter_period=period,
        filter_value=f"{date or ''}{month or ''}{year or ''}{start_date or ''}{end_date or ''}",
        generated_at=datetime.now(),
        total_sales=total_sales,
        total_invoices=total_invoices
    )
    db.add(cache)
    db.commit()
    
    return report_data

@router.get("/sales/download/csv")
def download_sales_csv(
    period: str = "day",
    date: Optional[str] = None,
    month: Optional[int] = None,
    year: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    start_month: Optional[int] = None,
    end_month: Optional[int] = None,
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_optional_query)
):
    from app.database import InvoiceItem, ProductService
    
    user_id = current_user.id
    query = db.query(Invoice).filter(Invoice.user_id == user_id)
    
    if period == "day_range" and start_date and end_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        query = query.filter(func.date(Invoice.date).between(start.date(), end.date()))
    elif period == "month_range" and start_month and end_month and year:
        query = query.filter(
            extract('year', Invoice.date) == year,
            extract('month', Invoice.date).between(start_month, end_month)
        )
    elif period == "year_range" and start_year and end_year:
        query = query.filter(extract('year', Invoice.date).between(start_year, end_year))
    elif period == "day" and date:
        target_date = datetime.strptime(date, "%Y-%m-%d")
        query = query.filter(func.date(Invoice.date) == target_date.date())
    elif period == "month" and month and year:
        query = query.filter(
            extract('month', Invoice.date) == month,
            extract('year', Invoice.date) == year
        )
    elif period == "year" and year:
        query = query.filter(extract('year', Invoice.date) == year)
    
    invoices = query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Invoice Number", "Date", "Customer Name", "Service Name", "Service Qty", "Product Name", "Product Qty", "Total Amount"])
    
    for inv in invoices:
        items = db.query(InvoiceItem).filter(InvoiceItem.invoice_id == inv.id).all()
        
        service_dict = {}
        product_dict = {}
        
        for item in items:
            product = db.query(ProductService).filter(ProductService.id == item.product_service_id).first()
            if product:
                if product.type == "service":
                    if product.name in service_dict:
                        service_dict[product.name]['qty'] += item.quantity
                        service_dict[product.name]['subtotal'] += item.subtotal
                    else:
                        service_dict[product.name] = {'qty': item.quantity, 'subtotal': item.subtotal}
                else:
                    if product.name in product_dict:
                        product_dict[product.name]['qty'] += item.quantity
                        product_dict[product.name]['subtotal'] += item.subtotal
                    else:
                        product_dict[product.name] = {'qty': item.quantity, 'subtotal': item.subtotal}
        
        product_names = ", ".join(product_dict.keys()) if product_dict else "N/A"
        product_qty = ", ".join([str(p['qty']) for p in product_dict.values()]) if product_dict else "N/A"
        
        if service_dict:
            for service_name, service_data in service_dict.items():
                writer.writerow([
                    inv.invoice_number,
                    inv.date.strftime("%Y-%m-%d"),
                    inv.customer_name,
                    service_name,
                    service_data['qty'],
                    product_names,
                    product_qty,
                    f"{service_data['subtotal']:.2f}"
                ])
        else:
            product_total = sum([p['subtotal'] for p in product_dict.values()]) if product_dict else 0
            writer.writerow([
                inv.invoice_number,
                inv.date.strftime("%Y-%m-%d"),
                inv.customer_name,
                "N/A",
                "N/A",
                product_names,
                product_qty,
                f"{product_total:.2f}"
            ])
    
    now = datetime.now()
    timestamp = now.strftime("%m%d%Y_%H%M")
    filename = f"sales_report_{period}_{timestamp}.csv"
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/sales/download/pdf")
def download_sales_pdf(
    period: str = "day",
    date: Optional[str] = None,
    month: Optional[int] = None,
    year: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    start_month: Optional[int] = None,
    end_month: Optional[int] = None,
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_optional_query)
):
    from reportlab.lib.pagesizes import letter, landscape
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from app.database import InvoiceItem, ProductService
    
    user_id = current_user.id
    query = db.query(Invoice).filter(Invoice.user_id == user_id)
    
    if period == "day_range" and start_date and end_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        query = query.filter(func.date(Invoice.date).between(start.date(), end.date()))
        period_text = f"Date Range: {start_date} to {end_date}"
    elif period == "month_range" and start_month and end_month and year:
        query = query.filter(
            extract('year', Invoice.date) == year,
            extract('month', Invoice.date).between(start_month, end_month)
        )
        period_text = f"Month Range: {start_month} to {end_month} ({year})"
    elif period == "year_range" and start_year and end_year:
        query = query.filter(extract('year', Invoice.date).between(start_year, end_year))
        period_text = f"Year Range: {start_year} to {end_year}"
    elif period == "day" and date:
        target_date = datetime.strptime(date, "%Y-%m-%d")
        query = query.filter(func.date(Invoice.date) == target_date.date())
        period_text = f"Day: {date}"
    elif period == "month" and month and year:
        query = query.filter(
            extract('month', Invoice.date) == month,
            extract('year', Invoice.date) == year
        )
        period_text = f"Month: {month}/{year}"
    elif period == "year" and year:
        query = query.filter(extract('year', Invoice.date) == year)
        period_text = f"Year: {year}"
    else:
        period_text = "All Time"
    
    invoices = query.all()
    total_sales = sum(inv.total_amount for inv in invoices)
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []
    styles = getSampleStyleSheet()
    
    title = Paragraph(f"<b>Sales Report - {period_text}</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    summary = Paragraph(f"<b>Total Sales:</b> PHP {total_sales:,.2f}<br/><b>Total Invoices:</b> {len(invoices)}", styles['Normal'])
    elements.append(summary)
    elements.append(Spacer(1, 0.3*inch))
    
    data = [["Invoice #", "Date", "Customer", "Service Name", "Service Qty", "Product Name", "Product Qty", "Amount"]]
    
    for inv in invoices:
        items = db.query(InvoiceItem).filter(InvoiceItem.invoice_id == inv.id).all()
        
        service_dict = {}
        product_dict = {}
        
        for item in items:
            product = db.query(ProductService).filter(ProductService.id == item.product_service_id).first()
            if product:
                if product.type == "service":
                    if product.name in service_dict:
                        service_dict[product.name]['qty'] += item.quantity
                        service_dict[product.name]['subtotal'] += item.subtotal
                    else:
                        service_dict[product.name] = {'qty': item.quantity, 'subtotal': item.subtotal}
                else:
                    if product.name in product_dict:
                        product_dict[product.name]['qty'] += item.quantity
                        product_dict[product.name]['subtotal'] += item.subtotal
                    else:
                        product_dict[product.name] = {'qty': item.quantity, 'subtotal': item.subtotal}
        
        product_names = ", ".join(product_dict.keys()) if product_dict else "N/A"
        product_qty = ", ".join([str(p['qty']) for p in product_dict.values()]) if product_dict else "N/A"
        
        if service_dict:
            for service_name, service_data in service_dict.items():
                data.append([
                    inv.invoice_number,
                    inv.date.strftime("%Y-%m-%d"),
                    inv.customer_name,
                    service_name,
                    str(service_data['qty']),
                    product_names,
                    product_qty,
                    f"PHP {service_data['subtotal']:,.2f}"
                ])
        else:
            product_total = sum([p['subtotal'] for p in product_dict.values()]) if product_dict else 0
            data.append([
                inv.invoice_number,
                inv.date.strftime("%Y-%m-%d"),
                inv.customer_name,
                "N/A",
                "N/A",
                product_names,
                product_qty,
                f"PHP {product_total:,.2f}"
            ])
    
    table = Table(data, colWidths=[1.3*inch, 1*inch, 1.2*inch, 1.5*inch, 0.8*inch, 1.5*inch, 0.8*inch, 1.1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    now = datetime.now()
    timestamp = now.strftime("%m%d%Y_%H%M")
    filename = f"sales_report_{period}_{timestamp}.pdf"
    
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
