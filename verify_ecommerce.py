"""
Verification script to check if e-commerce features are properly set up
"""
from app.database import SessionLocal, engine
from app import database
from sqlalchemy import inspect
import sys

def check_tables():
    """Check if all required tables exist"""
    print("\n" + "="*60)
    print("Checking Database Tables...")
    print("="*60)
    
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    required_tables = ['cart_items', 'orders', 'order_items', 'reservations']
    missing_tables = []
    
    for table in required_tables:
        if table in existing_tables:
            print(f"✓ {table} - EXISTS")
        else:
            print(f"✗ {table} - MISSING")
            missing_tables.append(table)
    
    return len(missing_tables) == 0

def check_roles():
    """Check if client role exists"""
    print("\n" + "="*60)
    print("Checking Roles...")
    print("="*60)
    
    db = SessionLocal()
    try:
        roles = db.query(database.Role).all()
        role_names = [r.name for r in roles]
        
        required_roles = ['admin', 'owner', 'staff', 'client']
        missing_roles = []
        
        for role in required_roles:
            if role in role_names:
                print(f"✓ {role} - EXISTS")
            else:
                print(f"✗ {role} - MISSING")
                missing_roles.append(role)
        
        return len(missing_roles) == 0
    finally:
        db.close()

def check_permissions():
    """Check if new permissions exist"""
    print("\n" + "="*60)
    print("Checking Permissions...")
    print("="*60)
    
    db = SessionLocal()
    try:
        permissions = db.query(database.Permission).all()
        perm_names = [p.name for p in permissions]
        
        new_permissions = [
            'view_products', 'manage_cart', 'place_order', 
            'reserve_service', 'view_own_orders', 'manage_orders', 'manage_queue'
        ]
        missing_perms = []
        
        for perm in new_permissions:
            if perm in perm_names:
                print(f"✓ {perm} - EXISTS")
            else:
                print(f"✗ {perm} - MISSING")
                missing_perms.append(perm)
        
        return len(missing_perms) == 0
    finally:
        db.close()

def check_client_user():
    """Check if test client user exists"""
    print("\n" + "="*60)
    print("Checking Test Client User...")
    print("="*60)
    
    db = SessionLocal()
    try:
        from app import crud
        client = crud.get_user_by_email(db, "client@carwash.com")
        
        if client:
            print(f"✓ client@carwash.com - EXISTS")
            roles = [r.name for r in client.roles]
            if 'client' in roles:
                print(f"✓ Client role assigned")
                return True
            else:
                print(f"✗ Client role NOT assigned")
                return False
        else:
            print(f"✗ client@carwash.com - MISSING")
            return False
    finally:
        db.close()

def check_api_routers():
    """Check if new routers are registered"""
    print("\n" + "="*60)
    print("Checking API Routers...")
    print("="*60)
    
    try:
        from app.routers import cart, orders, reservations, client
        print("✓ cart router - IMPORTED")
        print("✓ orders router - IMPORTED")
        print("✓ reservations router - IMPORTED")
        print("✓ client router - IMPORTED")
        return True
    except ImportError as e:
        print(f"✗ Router import failed: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("E-COMMERCE FEATURE VERIFICATION")
    print("="*60)
    
    results = {
        "Tables": check_tables(),
        "Roles": check_roles(),
        "Permissions": check_permissions(),
        "Client User": check_client_user(),
        "API Routers": check_api_routers()
    }
    
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    all_passed = True
    for check, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{check}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("✓ ALL CHECKS PASSED!")
        print("="*60)
        print("\nYou can now:")
        print("1. Start the server: start_server.bat")
        print("2. Login as client: client@carwash.com / client123")
        print("3. Visit: http://localhost:8000/shop.html")
        print("="*60)
        return 0
    else:
        print("✗ SOME CHECKS FAILED")
        print("="*60)
        print("\nPlease run:")
        print("1. python add_ecommerce_tables.py")
        print("2. python seed_data.py")
        print("3. python create_client_user.py")
        print("="*60)
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        print("\nMake sure:")
        print("1. PostgreSQL is running")
        print("2. DATABASE_URL is correct in .env")
        print("3. Database exists")
        sys.exit(1)
