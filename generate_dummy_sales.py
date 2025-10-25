from app.database import SessionLocal, Invoice, InvoiceItem, ProductService, Location, User
from datetime import datetime, timedelta
import random

def generate_dummy_sales():
    db = SessionLocal()
    
    try:
        # Get demo user
        user = db.query(User).filter(User.email == "demo@carwash.com").first()
        if not user:
            print("Demo user not found. Please run seed_data.py first.")
            return
        
        # Get or create location
        location = db.query(Location).filter(Location.user_id == user.id).first()
        if not location:
            location = Location(name="Main Bay", address="123 Main St", user_id=user.id)
            db.add(location)
            db.commit()
            db.refresh(location)
        
        # Get or create products
        products = db.query(ProductService).filter(ProductService.user_id == user.id).all()
        if not products:
            products = [
                ProductService(name="Basic Wash", price=500.00, type="Wash", user_id=user.id),
                ProductService(name="Premium Wash", price=800.00, type="Wash", user_id=user.id),
                ProductService(name="Wax Service", price=600.00, type="Wax", user_id=user.id),
                ProductService(name="Interior Detail", price=1200.00, type="Detail", user_id=user.id),
                ProductService(name="Full Detail", price=2000.00, type="Detail", user_id=user.id),
            ]
            for p in products:
                db.add(p)
            db.commit()
            for p in products:
                db.refresh(p)
        
        # Generate invoices for the last 30 days
        customers = ["John Doe", "Jane Smith", "Bob Johnson", "Alice Williams", "Charlie Brown", 
                    "Diana Prince", "Eve Adams", "Frank Miller", "Grace Lee", "Henry Ford"]
        
        # Get the highest invoice number to avoid duplicates
        last_invoice = db.query(Invoice).order_by(Invoice.id.desc()).first()
        invoice_count = (last_invoice.id + 1) if last_invoice else 1
        
        today = datetime.now()
        
        for days_ago in range(30):
            date = today - timedelta(days=days_ago)
            # Generate 2-5 invoices per day
            num_invoices = random.randint(2, 5)
            
            for i in range(num_invoices):
                invoice_number = f"INV-{date.strftime('%Y%m%d')}-{invoice_count:05d}"
                customer = random.choice(customers)
                
                # Create invoice
                invoice = Invoice(
                    invoice_number=invoice_number,
                    date=date.replace(hour=random.randint(8, 18), minute=random.randint(0, 59)),
                    customer_name=customer,
                    total_amount=0,
                    location_id=location.id,
                    user_id=user.id
                )
                db.add(invoice)
                db.commit()
                db.refresh(invoice)
                
                # Add 1-3 items to invoice
                num_items = random.randint(1, 3)
                total = 0
                
                for _ in range(num_items):
                    product = random.choice(products)
                    quantity = 1
                    unit_price = product.price
                    subtotal = quantity * unit_price
                    total += subtotal
                    
                    item = InvoiceItem(
                        invoice_id=invoice.id,
                        product_service_id=product.id,
                        quantity=quantity,
                        unit_price=unit_price,
                        subtotal=subtotal
                    )
                    db.add(item)
                
                # Update invoice total
                invoice.total_amount = total
                db.commit()
                
                invoice_count += 1
        
        total_generated = invoice_count - ((last_invoice.id + 1) if last_invoice else 1)
        print(f"Generated {total_generated} dummy invoices with items!")
        print(f"Date range: {(today - timedelta(days=29)).strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    generate_dummy_sales()
