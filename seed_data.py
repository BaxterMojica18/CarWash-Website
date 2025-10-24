from app.database import SessionLocal
from app import crud, database

db = SessionLocal()

# Create demo user
demo_user = crud.get_user_by_email(db, "demo@carwash.com")
if not demo_user:
    demo_user = crud.create_user(db, "demo@carwash.com", "demo123", is_demo=True)
    print("[OK] Demo user created")

# Create admin user
admin_user = crud.get_user_by_email(db, "admin@carwash.com")
if not admin_user:
    admin_user = crud.create_user(db, "admin@carwash.com", "admin123", is_demo=False)
    print("[OK] Admin user created")

# Create locations
if db.query(database.Location).count() == 0:
    locations = [
        {"name": "Main Street Bay", "address": "123 Main St, City"},
        {"name": "Downtown Bay", "address": "456 Downtown Ave, City"},
    ]
    for loc in locations:
        db_loc = database.Location(**loc)
        db.add(db_loc)
    db.commit()
    print("[OK] Locations created")

# Create products/services
if db.query(database.ProductService).count() == 0:
    products = [
        {"name": "Basic Wash", "price": 15.00, "description": "Exterior wash only", "type": "service"},
        {"name": "Premium Wash", "price": 30.00, "description": "Exterior + Interior", "type": "service"},
        {"name": "Deluxe Wash", "price": 50.00, "description": "Full detail service", "type": "service"},
        {"name": "Wax Treatment", "price": 20.00, "description": "Protective wax coating", "type": "product"},
    ]
    for prod in products:
        db_prod = database.ProductService(**prod)
        db.add(db_prod)
    db.commit()
    print("[OK] Products/Services created")

print("\n[OK] Database seeded successfully!")
print("\nDemo Login:")
print("  Email: demo@carwash.com")
print("  Password: demo123")
print("\nAdmin Login:")
print("  Email: admin@carwash.com")
print("  Password: admin123")

db.close()
