"""
Create demo users with limited permissions for testing
- demo-client: Client perspective (shopping, orders, reservations)
- demo-staff: Staff perspective (limited admin access)
- demo-admin: Admin perspective (limited to 1 product, 1 service, 10 orders, 10 reservations)
"""
from app.database import SessionLocal, User, Role, Permission
from app.crud import create_user
from sqlalchemy import text

def create_demo_accounts():
    db = SessionLocal()
    
    try:
        print("Creating demo accounts with limited permissions...")
        
        # Get or create roles
        client_role = db.query(Role).filter(Role.name == "client").first()
        if not client_role:
            client_role = Role(name="client", description="Client with shopping access")
            db.add(client_role)
            db.commit()
        
        user_role = db.query(Role).filter(Role.name == "user").first()
        demo_admin_role = db.query(Role).filter(Role.name == "demo_admin").first()
        if not demo_admin_role:
            demo_admin_role = Role(name="demo_admin", description="Demo admin with limited access")
            db.add(demo_admin_role)
            db.commit()
        
        # Create demo-client
        demo_client = db.query(User).filter(User.email == "demo-client@carwash.com").first()
        if not demo_client:
            demo_client = create_user(db, "demo-client@carwash.com", "demo123", is_demo=True)
            demo_client.roles.append(client_role)
            print("✅ Created demo-client@carwash.com (password: demo123)")
        else:
            print("⚠️  demo-client@carwash.com already exists")
        
        # Create demo-staff
        demo_staff = db.query(User).filter(User.email == "demo-staff@carwash.com").first()
        if not demo_staff:
            demo_staff = create_user(db, "demo-staff@carwash.com", "demo123", is_demo=True)
            demo_staff.roles.append(user_role)
            print("✅ Created demo-staff@carwash.com (password: demo123)")
        else:
            print("⚠️  demo-staff@carwash.com already exists")
        
        # Create demo-admin
        demo_admin = db.query(User).filter(User.email == "demo-admin@carwash.com").first()
        if not demo_admin:
            demo_admin = create_user(db, "demo-admin@carwash.com", "demo123", is_demo=True)
            demo_admin.roles.append(demo_admin_role)
            print("✅ Created demo-admin@carwash.com (password: demo123)")
        else:
            print("⚠️  demo-admin@carwash.com already exists")
        
        # Assign limited permissions to demo_admin role
        limited_perms = ["manage_invoices", "view_reports"]
        demo_admin_role.permissions.clear()
        for perm_name in limited_perms:
            perm = db.query(Permission).filter(Permission.name == perm_name).first()
            if perm:
                demo_admin_role.permissions.append(perm)
        
        db.commit()
        
        # Create usage limits table if not exists
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS demo_usage_limits (
                user_id INTEGER PRIMARY KEY REFERENCES users(id),
                products_created INTEGER DEFAULT 0,
                services_created INTEGER DEFAULT 0,
                orders_created INTEGER DEFAULT 0,
                reservations_created INTEGER DEFAULT 0,
                max_products INTEGER DEFAULT 1,
                max_services INTEGER DEFAULT 1,
                max_orders INTEGER DEFAULT 10,
                max_reservations INTEGER DEFAULT 10
            )
        """))
        db.commit()
        
        # Insert limits for demo users
        for user in [demo_client, demo_staff, demo_admin]:
            existing = db.execute(
                text("SELECT * FROM demo_usage_limits WHERE user_id = :uid"),
                {"uid": user.id}
            ).fetchone()
            
            if not existing:
                db.execute(text("""
                    INSERT INTO demo_usage_limits 
                    (user_id, products_created, services_created, orders_created, reservations_created,
                     max_products, max_services, max_orders, max_reservations)
                    VALUES (:uid, 0, 0, 0, 0, 1, 1, 10, 10)
                """), {"uid": user.id})
        
        db.commit()
        
        print("\n" + "="*60)
        print("DEMO ACCOUNTS CREATED SUCCESSFULLY!")
        print("="*60)
        print("\n📋 Demo Account Credentials:\n")
        print("1. CLIENT PERSPECTIVE:")
        print("   Email: demo-client@carwash.com")
        print("   Password: demo123")
        print("   Access: Shopping, Cart, Orders, Reservations")
        print("   Limits: 10 orders, 10 reservations\n")
        
        print("2. STAFF PERSPECTIVE:")
        print("   Email: demo-staff@carwash.com")
        print("   Password: demo123")
        print("   Access: Invoices, Reports (read-only)")
        print("   Limits: 10 orders, 10 reservations\n")
        
        print("3. ADMIN PERSPECTIVE (Limited):")
        print("   Email: demo-admin@carwash.com")
        print("   Password: demo123")
        print("   Access: Invoices, Reports")
        print("   Limits: 1 product, 1 service, 10 orders, 10 reservations\n")
        
        print("="*60)
        print("⚠️  NOTE: These are DEMO accounts with limited permissions")
        print("    Users can explore the system without breaking anything!")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_demo_accounts()
