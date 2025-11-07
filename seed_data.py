from app.database import SessionLocal
from app import crud, database

db = SessionLocal()

# Create roles and permissions
roles_data = [
    {"name": "admin", "description": "Full system access"},
    {"name": "owner", "description": "Business owner access"},
    {"name": "staff", "description": "Limited staff access"}
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
    {"name": "view_reports", "description": "View sales reports"}
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

all_permissions = db.query(database.Permission).all()
staff_permissions = db.query(database.Permission).filter(
    database.Permission.name.in_(["add_invoice", "view_reports"])
).all()

if admin_role:
    admin_role.permissions = all_permissions
if owner_role:
    owner_role.permissions = all_permissions
if staff_role:
    staff_role.permissions = staff_permissions
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

print("\n[OK] Database seeded successfully!")
print("\nDemo Login:")
print("  Email: demo@carwash.com")
print("  Password: demo123")
print("\nAdmin Login:")
print("  Email: admin@carwash.com")
print("  Password: admin123")

db.close()
