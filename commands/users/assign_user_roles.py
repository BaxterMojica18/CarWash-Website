from app.database import SessionLocal, User, Role

db = SessionLocal()

# Assign admin role to admin user
admin_user = db.query(User).filter(User.email == "admin@carwash.com").first()
admin_role = db.query(Role).filter(Role.name == "admin").first()

if admin_user and admin_role:
    if admin_role not in admin_user.roles:
        admin_user.roles.append(admin_role)
        print(f"[OK] Assigned 'admin' role to {admin_user.email}")
    else:
        print(f"[INFO] {admin_user.email} already has 'admin' role")
else:
    print("[ERROR] Admin user or role not found")

# Assign staff role to demo user
demo_user = db.query(User).filter(User.email == "demo@carwash.com").first()
staff_role = db.query(Role).filter(Role.name == "staff").first()

if demo_user and staff_role:
    if staff_role not in demo_user.roles:
        demo_user.roles.append(staff_role)
        print(f"[OK] Assigned 'staff' role to {demo_user.email}")
    else:
        print(f"[INFO] {demo_user.email} already has 'staff' role")
else:
    print("[ERROR] Demo user or 'staff' role not found")

# Assign client role to client demo user
client_user = db.query(User).filter(User.email == "client@carwash.com").first()
client_role = db.query(Role).filter(Role.name == "client").first()

if client_user and client_role:
    if client_role not in client_user.roles:
        client_user.roles.append(client_role)
        print(f"[OK] Assigned 'client' role to {client_user.email}")
    else:
        print(f"[INFO] {client_user.email} already has 'client' role")
else:
    print("[ERROR] Client user or role not found")

db.commit()
db.close()

print("\n[OK] Role assignment complete!")
