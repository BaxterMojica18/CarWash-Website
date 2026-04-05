from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqladmin import Admin, ModelView
from app.database import create_tables, engine, User, Location, ProductService, Invoice, Order, Reservation
from app.routers import auth, settings, invoices, reports, cart, orders, reservations, client, dashboard, payment_methods, payments
from app.email_service import send_email
import os
from starlette.middleware.base import BaseHTTPMiddleware

class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if request.url.path.endswith(('.html', '.css', '.js')):
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        return response

app = FastAPI(
    title="Car Wash Manager API",
    description="Backend API for dashboard, invoicing, and settings.",
    version="1.0.2",
    docs_url="/docs",
    redoc_url="/redoc",
)

# SQLAdmin setup
admin = Admin(app, engine)

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.is_demo]
    
class LocationAdmin(ModelView, model=Location):
    column_list = [Location.id, Location.name, Location.address, Location.status]
    
class ProductServiceAdmin(ModelView, model=ProductService):
    column_list = [ProductService.id, ProductService.name, ProductService.price, ProductService.type]
    
class InvoiceAdmin(ModelView, model=Invoice):
    column_list = [Invoice.id, Invoice.invoice_number, Invoice.customer_name, Invoice.total_amount, Invoice.date]
    
class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.order_number, Order.status, Order.total_amount, Order.created_at]
    
class ReservationAdmin(ModelView, model=Reservation):
    column_list = [Reservation.id, Reservation.reservation_number, Reservation.status, Reservation.vehicle_plate]

admin.add_view(UserAdmin)
admin.add_view(LocationAdmin)
admin.add_view(ProductServiceAdmin)
admin.add_view(InvoiceAdmin)
admin.add_view(OrderAdmin)
admin.add_view(ReservationAdmin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:5500",
        "https://car-wash-website-khaki.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(NoCacheMiddleware)

try:
    create_tables()
    print("Database tables ensured.")
except Exception as e:
    print(f"Warning: Could not initialize database tables: {e}")
    print("Server will continue running. Check database connection.")

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])
app.include_router(invoices.router, prefix="/api/invoices", tags=["Invoices"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(cart.router, prefix="/api/cart", tags=["Cart"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])
app.include_router(reservations.router, prefix="/api/reservations", tags=["Reservations"])
app.include_router(client.router, prefix="/api/client", tags=["Client"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(payment_methods.router, prefix="/api/payment-methods", tags=["Payment Methods"])
app.include_router(payments.router, prefix="/api/payments", tags=["Stripe Payments"])

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "API is running"}


@app.post("/api/contact-sales")
async def contact_sales(request: Request):
    from pydantic import BaseModel
    data = await request.json()
    name = data.get("name", "")
    email = data.get("email", "")
    business = data.get("business", "")
    phone = data.get("phone", "")
    message = data.get("message", "")

    html = f"""
    <div style="font-family:'Segoe UI',sans-serif;max-width:600px;margin:0 auto;background:#f5f5f5;padding:30px;">
        <div style="background:linear-gradient(135deg,#667eea,#764ba2);padding:25px;border-radius:12px 12px 0 0;text-align:center;">
            <h1 style="color:white;margin:0;font-size:22px;">💼 New One-Time Payment Inquiry</h1>
        </div>
        <div style="background:white;padding:30px;border-radius:0 0 12px 12px;box-shadow:0 4px 20px rgba(0,0,0,0.1);">
            <table style="width:100%;border-collapse:collapse;">
                <tr><td style="padding:10px 0;border-bottom:1px solid #eee;font-weight:600;color:#555;width:140px;">Name</td><td style="padding:10px 0;border-bottom:1px solid #eee;color:#2c3e50;">{name}</td></tr>
                <tr><td style="padding:10px 0;border-bottom:1px solid #eee;font-weight:600;color:#555;">Email</td><td style="padding:10px 0;border-bottom:1px solid #eee;"><a href="mailto:{email}" style="color:#667eea;">{email}</a></td></tr>
                <tr><td style="padding:10px 0;border-bottom:1px solid #eee;font-weight:600;color:#555;">Business</td><td style="padding:10px 0;border-bottom:1px solid #eee;color:#2c3e50;">{business}</td></tr>
                <tr><td style="padding:10px 0;border-bottom:1px solid #eee;font-weight:600;color:#555;">Phone</td><td style="padding:10px 0;border-bottom:1px solid #eee;color:#2c3e50;">{phone}</td></tr>
                <tr><td style="padding:10px 0;font-weight:600;color:#555;vertical-align:top;">Message</td><td style="padding:10px 0;color:#2c3e50;">{message or 'No message provided.'}</td></tr>
            </table>
            <div style="margin-top:20px;padding:15px;background:#f0f4ff;border-radius:8px;border-left:4px solid #667eea;">
                <p style="margin:0;font-size:13px;color:#667eea;">Reply directly to <strong>{email}</strong> to follow up with this lead.</p>
            </div>
        </div>
        <p style="text-align:center;color:#aaa;font-size:12px;margin-top:15px;">&copy; CarWash Management System</p>
    </div>
    """

    send_email(
        "baxterdavid.mojica@gmail.com",
        f"💼 New Sales Inquiry from {name} — {business}",
        html,
        f"New inquiry from {name} ({email})\nBusiness: {business}\nPhone: {phone}\nMessage: {message}"
    )
    return {"message": "Thank you! We'll be in touch shortly."}

# Serve frontend static files BEFORE catch-all routes
app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")

@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")

@app.get("/{page}.html")
def read_page(page: str):
    file_path = f"frontend/{page}.html"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "Page not found"}
