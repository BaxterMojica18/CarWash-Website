from app.database import SessionLocal
from app import crud, database
from datetime import datetime, timedelta
import random

db = SessionLocal()

# Create roles and permissions
roles_data = [
    {"name": "admin", "description": "Full system access"},
    {"name": "owner", "description": "Business owner access"},
    {"name": "staff", "description": "Limited staff access"},
    {"name": "client", "description": "Customer access"}
]

for role_data in roles_data:
    role = db.query(database.Role).filter(database.Role.name == role_data["name"]).first()
    if not role:
        role = database.Role(**role_data)
        db.add(role)
db.commit()
print("[OK] Roles created")

# Create permissions
permissions_data = [
    {"name": "manage_users", "description": "Manage users and roles"},
    {"name": "add_invoice", "description": "Add invoices"},
    {"name": "edit_invoice", "description": "Edit invoices"},
    {"name": "delete_invoice", "description": "Delete invoices"},
    {"name": "add_product", "description": "Add products"},
    {"name": "edit_product", "description": "Edit products"},
    {"name": "delete_product", "description": "Delete products"},
    {"name": "add_service", "description": "Add services"},
    {"name": "edit_service", "description": "Edit services"},
    {"name": "delete_service", "description": "Delete services"},
    {"name": "edit_theme", "description": "Edit theme options"},
    {"name": "add_bay", "description": "Add washing bays"},
    {"name": "edit_bay", "description": "Edit washing bays"},
    {"name": "delete_bay", "description": "Delete washing bays"},
    {"name": "view_reports", "description": "View sales reports"},
    {"name": "view_products", "description": "View products and services"},
    {"name": "manage_cart", "description": "Manage shopping cart"},
    {"name": "place_order", "description": "Place product orders"},
    {"name": "reserve_service", "description": "Reserve car wash services"},
    {"name": "view_own_orders", "description": "View own orders and reservations"},
    {"name": "manage_orders", "description": "Manage all orders"},
    {"name": "manage_queue", "description": "Manage service queue"}
]

for perm_data in permissions_data:
    perm = db.query(database.Permission).filter(database.Permission.name == perm_data["name"]).first()
    if not perm:
        perm = database.Permission(**perm_data)
        db.add(perm)
db.commit()
print("[OK] Permissions created")

# Assign permissions to roles
admin_role = db.query(database.Role).filter(database.Role.name == "admin").first()
owner_role = db.query(database.Role).filter(database.Role.name == "owner").first()
staff_role = db.query(database.Role).filter(database.Role.name == "staff").first()
client_role = db.query(database.Role).filter(database.Role.name == "client").first()

all_permissions = db.query(database.Permission).all()
staff_permissions = db.query(database.Permission).filter(
    database.Permission.name.in_(["add_invoice", "view_reports"])
).all()
client_permissions = db.query(database.Permission).filter(
    database.Permission.name.in_(["view_products", "manage_cart", "place_order", "reserve_service", "view_own_orders"])
).all()

if admin_role:
    admin_role.permissions = all_permissions
if owner_role:
    owner_role.permissions = all_permissions
if staff_role:
    staff_role.permissions = staff_permissions
if client_role:
    client_role.permissions = client_permissions
db.commit()
print("[OK] Permissions assigned to roles")

# Create demo user
demo_user = crud.get_user_by_email(db, "demo@carwash.com")
if not demo_user:
    demo_user = crud.create_user(db, "demo@carwash.com", "demo123", is_demo=True)
    print("[OK] Demo user created")

if admin_role and admin_role not in demo_user.roles:
    demo_user.roles.append(admin_role)
    db.commit()
    print("[OK] Demo user assigned admin role")

# Create admin user
admin_user = crud.get_user_by_email(db, "admin@carwash.com")
if not admin_user:
    admin_user = crud.create_user(db, "admin@carwash.com", "admin123", is_demo=False)
    print("[OK] Admin user created")

if admin_role and admin_role not in admin_user.roles:
    admin_user.roles.append(admin_role)
    db.commit()
    print("[OK] Admin user assigned admin role")

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

# Create sample invoices
if db.query(database.Invoice).count() == 0:
    customers = ["John Doe", "Jane Smith", "Bob Johnson", "Alice Williams", "Charlie Brown"]
    locations = db.query(database.Location).all()
    products = db.query(database.ProductService).all()
    
    for i in range(10):
        invoice_date = datetime.now() - timedelta(days=random.randint(0, 7))
        
        invoice = database.Invoice(
            invoice_number=f"INV-{invoice_date.strftime('%Y%m%d%H%M%S')}-{i}",
            date=invoice_date,
            customer_name=random.choice(customers),
            total_amount=0,
            location_id=random.choice(locations).id,
            user_id=admin_user.id,
            status="A"
        )
        db.add(invoice)
        db.flush()
        
        total = 0
        for _ in range(random.randint(1, 3)):
            product = random.choice(products)
            quantity = random.randint(1, 3)
            subtotal = product.price * quantity
            total += subtotal
            
            item = database.InvoiceItem(
                invoice_id=invoice.id,
                product_service_id=product.id,
                quantity=quantity,
                unit_price=product.price,
                subtotal=subtotal
            )
            db.add(item)
        
        invoice.total_amount = total
    
    db.commit()
    print("[OK] Sample invoices created")

print("\n[OK] Database seeded successfully!")
print("\nDemo Login:")
print("  Email: demo@carwash.com")
print("  Password: demo123")
print("\nAdmin Login:")
print("  Email: admin@carwash.com")
print("  Password: admin123")

db.close()
