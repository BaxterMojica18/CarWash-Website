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

# Assign user role to demo user
demo_user = db.query(User).filter(User.email == "demo@carwash.com").first()
user_role = db.query(Role).filter(Role.name == "user").first()

if demo_user and user_role:
    if user_role not in demo_user.roles:
        demo_user.roles.append(user_role)
        print(f"[OK] Assigned 'user' role to {demo_user.email}")
    else:
        print(f"[INFO] {demo_user.email} already has 'user' role")
else:
    print("[ERROR] Demo user or role not found")

db.commit()
db.close()

print("\n[OK] Role assignment complete!")
