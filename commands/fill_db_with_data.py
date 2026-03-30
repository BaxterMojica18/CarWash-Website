import sys
import os
import random
from datetime import datetime, timedelta

# Add parent directory to path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, ProductService, Order, OrderItem, Invoice, InvoiceItem, Reservation, Location, User

def fill_data():
    db = SessionLocal()
    try:
        owner = db.query(User).filter(User.email == 'owner@carwash.com').first()
        demo_client = db.query(User).filter(User.email == 'demo-client@carwash.com').first()
        owner_id = owner.id if owner else 1
        client_id = demo_client.id if demo_client else 1

        loc = db.query(Location).first()
        if not loc:
            loc = Location(name="Main Station", address="123 Wash Ave", user_id=owner_id, status="A")
            db.add(loc)
            db.commit()
            db.refresh(loc)

        print("Adding more Products and Services...")
        services_data = [
            ("Deluxe Wash", 45.00, "Full service inside and out"),
            ("Ultimate Detail", 150.00, "Complete detailing service"),
            ("Quick Wash", 10.00, "Express exterior wash"),
            ("Hand Wax", 40.00, "Premium hand applied wax"),
            ("Interior Vacuum", 15.00, "Deep interior vacuuming"),
            ("Engine Cleaning", 60.00, "Engine bay cleaning"),
        ]
        
        products_data = [
            ("Tire Shine", 8.99, "bottle", 100, "High gloss tire shine"),
            ("Glass Cleaner", 5.99, "bottle", 50, "Streak-free glass cleaner"),
            ("Microfiber Towel", 2.50, "piece", 200, "Soft cleaning towel"),
            ("Leather Conditioner", 14.99, "bottle", 30, "Premium leather care"),
            ("Carpet Cleaner", 11.99, "bottle", 40, "Deep stain remover"),
        ]

        new_items = []
        for name, price, desc in services_data:
            existing = db.query(ProductService).filter(ProductService.name == name).first()
            if not existing:
                new_items.append(ProductService(name=name, price=price, type="service", user_id=owner_id, status="A", description=desc))
                
        for name, price, unit, qty, desc in products_data:
            existing = db.query(ProductService).filter(ProductService.name == name).first()
            if not existing:
                new_items.append(ProductService(name=name, price=price, type="product", quantity=qty, quantity_unit=unit, user_id=owner_id, status="A", description=desc))
        
        if new_items:
            db.add_all(new_items)
            db.commit()
            
        all_products = db.query(ProductService).all()

        print("Generating 30 random orders...")
        statuses = ["completed", "completed", "pending", "accepted", "processing", "delayed", "cancelled"]
        payments = ["cash", "card", "card", "online"]
        
        new_order_items = []
        for i in range(30):
            days_ago = random.randint(0, 30)
            order_date = datetime.utcnow() - timedelta(days=days_ago, hours=random.randint(0, 23))
            o_num = f"ORD-{random.randint(10000, 99999)}"
            
            # Select 1-3 random products
            num_items = random.randint(1, 3)
            selected_products = random.sample(all_products, num_items)
            
            total = sum(p.price * random.randint(1, 2) for p in selected_products)
            
            order = Order(order_number=o_num, client_id=client_id, status=random.choice(statuses), 
                          total_amount=total, payment_method=random.choice(payments), 
                          created_at=order_date, updated_at=order_date)
            db.add(order)
            db.flush() # flush to get order ID
            
            for p in selected_products:
                qty = random.randint(1, 2)
                subtotal = p.price * qty
                new_order_items.append(OrderItem(order_id=order.id, product_service_id=p.id, quantity=qty, unit_price=p.price, subtotal=subtotal))
                
        db.add_all(new_order_items)
        db.commit()

        print("Generating 30 random invoices...")
        customers = ["John Doe", "Jane Smith", "Bob Johnson", "Alice Brown", "Charlie Davis", "Sam Wilson", "Tina Fey"]
        new_invoice_items = []
        for i in range(30):
            days_ago = random.randint(0, 30)
            inv_date = datetime.utcnow() - timedelta(days=days_ago, hours=random.randint(0, 23))
            inv_num = f"INV-{random.randint(10000, 99999)}"
            
            num_items = random.randint(1, 4)
            selected_products = random.sample(all_products, num_items)
            
            total = sum(p.price * random.randint(1, 2) for p in selected_products)
            
            inv = Invoice(invoice_number=inv_num, date=inv_date, customer_name=random.choice(customers), 
                          total_amount=total, location_id=loc.id, user_id=owner_id, status="A")
            db.add(inv)
            db.flush()
            
            for p in selected_products:
                qty = random.randint(1, 2)
                subtotal = p.price * qty
                new_invoice_items.append(InvoiceItem(invoice_id=inv.id, product_service_id=p.id, quantity=qty, unit_price=p.price, subtotal=subtotal))
                
        db.add_all(new_invoice_items)
        
        # Add a few more reservations to make queue interesting
        reservations = []
        res_statuses = ["pending", "accepted", "in_progress", "completed", "delayed", "cancelled"]
        for i in range(15):
            res_num = f"RES-{random.randint(4000, 9999)}"
            p_basic = random.choice([p for p in all_products if p.type == "service"])
            reservations.append(Reservation(reservation_number=res_num, client_id=client_id, service_id=p_basic.id, 
                                location_id=loc.id, vehicle_plate=f"XYZ-{random.randint(100,999)}", 
                                status=random.choice(res_statuses), queue_position=i+2, created_at=datetime.utcnow() - timedelta(hours=i)))
        db.add_all(reservations)
        
        db.commit()

        print("Successfully generated extensive sample data!")
        
    except Exception as e:
        print(f"Error adding more data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fill_data()
