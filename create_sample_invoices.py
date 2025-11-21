from app.database import SessionLocal, Invoice, InvoiceItem, User, Location, ProductService
from datetime import datetime, timedelta
import random

db = SessionLocal()

user = db.query(User).filter(User.email == "admin@carwash.com").first()
locations = db.query(Location).all()
products = db.query(ProductService).all()

customers = ["John Doe", "Jane Smith", "Bob Johnson", "Alice Williams", "Charlie Brown"]

for i in range(10):
    invoice_date = datetime.now() - timedelta(days=random.randint(0, 7))
    
    invoice = Invoice(
        invoice_number=f"INV-{invoice_date.strftime('%Y%m%d%H%M%S')}{i:03d}",
        date=invoice_date,
        customer_name=random.choice(customers),
        total_amount=0,
        location_id=random.choice(locations).id,
        user_id=user.id
    )
    db.add(invoice)
    db.flush()
    
    total = 0
    for _ in range(random.randint(1, 3)):
        product = random.choice(products)
        quantity = random.randint(1, 3)
        subtotal = product.price * quantity
        total += subtotal
        
        item = InvoiceItem(
            invoice_id=invoice.id,
            product_service_id=product.id,
            quantity=quantity,
            unit_price=product.price,
            subtotal=subtotal
        )
        db.add(item)
    
    invoice.total_amount = total

db.commit()
print("✓ Created 10 sample invoices")
db.close()
