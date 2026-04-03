"""
Setup demo accounts with proper multi-tenant business scoping.

This script:
1. Ensures owner@carwash.com (superadmin) has account_type='owner' and a business_number
2. Creates staff@carwash.com as a STAFF demo under the owner's business
3. Creates admin@carwash.com as an ADMIN demo under the owner's business
4. Seeds unique products, services, locations, invoices, orders per business
5. Creates a SECOND independent business to demonstrate data isolation

Run inside Docker:
  docker-compose exec web python commands/users/setup_demo_accounts.py
"""
import sys
import os
import random
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import (
    SessionLocal, User, Role, Permission, role_permissions,
    Location, ProductService, Invoice, InvoiceItem,
    Order, OrderItem, Reservation
)
from app.crud import create_user, get_password_hash
from sqlalchemy import text

OWNER_BUSINESS_NUMBER = "BXTK-001"
SECOND_BUSINESS_NUMBER = "WASH-002"


def ensure_roles(db):
    """Ensure all required roles exist and return them."""
    role_map = {}
    needed = {
        "superadmin": "Super Administrator - Full system control",
        "owner": "Business Owner",
        "admin": "Administrator",
        "user": "Staff member",
        "client": "Customer / Client",
        "demo_admin": "Demo admin with limited access",
    }
    for name, desc in needed.items():
        role = db.query(Role).filter(Role.name == name).first()
        if not role:
            role = Role(name=name, description=desc)
            db.add(role)
            db.commit()
            db.refresh(role)
            print(f"  ✅ Created role: {name}")
        role_map[name] = role
    return role_map


def setup_owner(db, roles):
    """Ensure owner@carwash.com exists as superadmin with business_number."""
    owner = db.query(User).filter(User.email == "owner@carwash.com").first()
    if not owner:
        owner = create_user(db, "owner@carwash.com", "owner123", is_demo=False)
        print("  ✅ Created owner@carwash.com")
    
    # Set business fields
    owner.account_type = "owner"
    owner.business_number = OWNER_BUSINESS_NUMBER
    
    # Ensure superadmin role
    superadmin_role = roles["superadmin"]
    if superadmin_role not in owner.roles:
        owner.roles.clear()
        owner.roles.append(superadmin_role)
    
    # Give superadmin ALL permissions
    all_perms = db.query(Permission).all()
    db.execute(role_permissions.delete().where(role_permissions.c.role_id == superadmin_role.id))
    for perm in all_perms:
        db.execute(role_permissions.insert().values(role_id=superadmin_role.id, permission_id=perm.id))
    
    db.commit()
    db.refresh(owner)
    print(f"  ✅ owner@carwash.com → superadmin, business={OWNER_BUSINESS_NUMBER}")
    return owner


def setup_staff_demo(db, roles, owner):
    """Create staff@carwash.com under the owner's business."""
    staff = db.query(User).filter(User.email == "staff@carwash.com").first()
    if not staff:
        staff = create_user(db, "staff@carwash.com", "staff123", is_demo=True)
        print("  ✅ Created staff@carwash.com")
    else:
        print("  ⚠️  staff@carwash.com already exists, updating...")

    staff.account_type = "staff"
    staff.business_number = OWNER_BUSINESS_NUMBER
    staff.is_demo = True
    
    # Clear and set role to 'user' (staff)
    staff.roles.clear()
    staff.roles.append(roles["user"])
    
    db.commit()
    db.refresh(staff)
    print(f"  ✅ staff@carwash.com → user (staff), business={OWNER_BUSINESS_NUMBER}")
    return staff


def setup_admin_demo(db, roles, owner):
    """Create admin@carwash.com under the owner's business."""
    admin = db.query(User).filter(User.email == "admin@carwash.com").first()
    if not admin:
        admin = create_user(db, "admin@carwash.com", "admin123", is_demo=True)
        print("  ✅ Created admin@carwash.com")
    else:
        print("  ⚠️  admin@carwash.com already exists, updating...")

    admin.account_type = "admin"
    admin.business_number = OWNER_BUSINESS_NUMBER
    admin.is_demo = True
    
    # Clear and set role to 'admin'
    admin.roles.clear()
    admin.roles.append(roles["admin"])
    
    # Give admin role proper permissions
    admin_role = roles["admin"]
    admin_perms = ["manage_products", "manage_locations", "view_locations",
                   "manage_invoices", "view_invoices", "view_reports", "manage_settings"]
    admin_role.permissions.clear()
    for perm_name in admin_perms:
        perm = db.query(Permission).filter(Permission.name == perm_name).first()
        if perm:
            admin_role.permissions.append(perm)
    
    db.commit()
    db.refresh(admin)
    print(f"  ✅ admin@carwash.com → admin, business={OWNER_BUSINESS_NUMBER}")
    return admin


def setup_client_demo(db, roles):
    """Ensure demo-client@carwash.com exists as a client under the owner's business."""
    client = db.query(User).filter(User.email == "demo-client@carwash.com").first()
    if not client:
        client = create_user(db, "demo-client@carwash.com", "demo123", is_demo=True)
        print("  ✅ Created demo-client@carwash.com")
    
    client.account_type = "client"
    client.business_number = OWNER_BUSINESS_NUMBER
    client.is_demo = True
    
    if roles["client"] not in client.roles:
        client.roles.clear()
        client.roles.append(roles["client"])
    
    db.commit()
    db.refresh(client)
    print(f"  ✅ demo-client@carwash.com → client, business={OWNER_BUSINESS_NUMBER}")
    return client


def setup_second_business(db, roles):
    """Create a second independent business to prove data isolation works."""
    owner2 = db.query(User).filter(User.email == "owner2@sparklewash.com").first()
    if not owner2:
        owner2 = create_user(db, "owner2@sparklewash.com", "owner123", is_demo=False)
        print("  ✅ Created owner2@sparklewash.com")
    
    owner2.account_type = "owner"
    owner2.business_number = SECOND_BUSINESS_NUMBER
    
    # Give owner role (admin-level, not superadmin)
    owner2.roles.clear()
    owner2.roles.append(roles["admin"])
    
    # Also give the 'owner' role
    if roles.get("owner"):
        owner2.roles.append(roles["owner"])
    
    db.commit()
    db.refresh(owner2)
    print(f"  ✅ owner2@sparklewash.com → owner, business={SECOND_BUSINESS_NUMBER}")
    return owner2


def setup_demo_limits(db, users):
    """Create/update demo_usage_limits table for demo users."""
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
    
    for user in users:
        if not user.is_demo:
            continue
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
    print("  ✅ Demo usage limits configured")


# ─── DATA SEEDING ──────────────────────────────────────────────

def seed_business_data(db, owner, business_name, business_number):
    """Seed locations, products, services, invoices, and orders for a specific business."""
    owner_id = owner.id
    print(f"\n  📦 Seeding data for {business_name} ({business_number})...")

    # ── Locations ──
    loc_data = {
        OWNER_BUSINESS_NUMBER: [
            ("BuxWash Main Station", "123 Rizal Avenue, Manila"),
            ("BuxWash Express Hub", "45 EDSA, Quezon City"),
        ],
        SECOND_BUSINESS_NUMBER: [
            ("SparkleWash Downtown", "789 Ayala Avenue, Makati"),
            ("SparkleWash Mall Branch", "SM Megamall, Mandaluyong"),
        ],
    }
    
    locations = []
    for name, address in loc_data.get(business_number, []):
        loc = db.query(Location).filter(Location.name == name, Location.user_id == owner_id).first()
        if not loc:
            loc = Location(name=name, address=address, user_id=owner_id, status="A")
            db.add(loc)
            db.commit()
            db.refresh(loc)
        locations.append(loc)
    print(f"    ✅ {len(locations)} locations")

    # ── Products & Services ──
    products_map = {
        OWNER_BUSINESS_NUMBER: {
            "services": [
                ("Premium Full Wash", 350.00, "Complete interior and exterior wash"),
                ("Express Exterior Wash", 150.00, "Quick exterior-only wash"),
                ("Deluxe Detailing", 800.00, "Full detailing service with wax"),
                ("Engine Bay Cleaning", 500.00, "Deep engine compartment cleaning"),
                ("Interior Deep Clean", 450.00, "Seats, carpets, and dashboard detail"),
                ("Hand Wax & Polish", 600.00, "Premium hand-applied carnauba wax"),
            ],
            "products": [
                ("Tire Black Gel", 89.00, "bottle", 100, "High-gloss tire dressing"),
                ("Microfiber Towel Pack", 199.00, "pack", 200, "Set of 5 premium towels"),
                ("Glass Rain Repellent", 149.00, "bottle", 50, "Windshield water beading spray"),
                ("Leather Conditioner", 249.00, "bottle", 75, "UV-protection leather care"),
                ("Car Freshener", 59.00, "piece", 300, "Long-lasting cabin freshener"),
            ],
        },
        SECOND_BUSINESS_NUMBER: {
            "services": [
                ("Basic Wash", 120.00, "Standard exterior soap wash"),
                ("Interior Vacuum", 200.00, "Full interior vacuum and wipe"),
                ("Ceramic Coating", 2500.00, "Professional ceramic paint protection"),
                ("Undercarriage Wash", 350.00, "Complete underbody wash and rinse"),
                ("Steam Cleaning", 700.00, "Chemical-free steam detail"),
            ],
            "products": [
                ("Dash Protectant", 120.00, "bottle", 60, "UV-shield dashboard spray"),
                ("Wheel Cleaner", 180.00, "bottle", 80, "Acid-free wheel cleaner"),
                ("Clay Bar Kit", 350.00, "kit", 30, "Paint decontamination kit"),
                ("Foam Cannon Soap", 250.00, "gallon", 40, "Thick-foam wash soap"),
            ],
        },
    }

    biz_items = products_map.get(business_number, {"services": [], "products": []})
    new_items = []

    for name, price, desc in biz_items["services"]:
        existing = db.query(ProductService).filter(
            ProductService.name == name, ProductService.user_id == owner_id
        ).first()
        if not existing:
            new_items.append(ProductService(
                name=name, price=price, type="service",
                user_id=owner_id, status="A", description=desc
            ))

    for name, price, unit, qty, desc in biz_items["products"]:
        existing = db.query(ProductService).filter(
            ProductService.name == name, ProductService.user_id == owner_id
        ).first()
        if not existing:
            new_items.append(ProductService(
                name=name, price=price, type="product",
                quantity=qty, quantity_unit=unit,
                user_id=owner_id, status="A", description=desc
            ))

    if new_items:
        db.add_all(new_items)
        db.commit()
    print(f"    ✅ {len(biz_items['services'])} services, {len(biz_items['products'])} products")

    # Fetch all products/services for this business
    all_items = db.query(ProductService).filter(
        ProductService.user_id == owner_id, ProductService.status == "A"
    ).all()
    all_services = [i for i in all_items if i.type == "service"]
    all_products_only = [i for i in all_items if i.type == "product"]

    if not locations:
        print("    ⚠️  No locations found, skipping invoices/orders/reservations")
        return

    loc = locations[0]

    # ── Invoices ──
    customers = {
        OWNER_BUSINESS_NUMBER: ["Juan Dela Cruz", "Maria Santos", "Pedro Reyes", "Ana Gonzalez", "Carlos Mendoza", "Liza Cruz", "Mark Tan"],
        SECOND_BUSINESS_NUMBER: ["James Lee", "Sarah Kim", "David Park", "Grace Lim", "Robert Chen", "Lisa Wang"],
    }
    customer_names = customers.get(business_number, ["Test Customer"])

    existing_inv_count = db.query(Invoice).filter(Invoice.user_id == owner_id).count()
    if existing_inv_count < 5:
        print(f"    📄 Generating invoices...")
        new_invoice_items = []
        for i in range(25):
            days_ago = random.randint(0, 60)
            inv_date = datetime.utcnow() - timedelta(days=days_ago, hours=random.randint(0, 23))
            inv_num = f"INV-{business_number[:4]}-{random.randint(10000, 99999)}"

            num_items = random.randint(1, 3)
            selected = random.sample(all_items, min(num_items, len(all_items)))
            total = sum(p.price * random.randint(1, 2) for p in selected)

            inv = Invoice(
                invoice_number=inv_num, date=inv_date,
                customer_name=random.choice(customer_names),
                total_amount=total, location_id=loc.id,
                user_id=owner_id, status="A"
            )
            db.add(inv)
            db.flush()

            for p in selected:
                qty = random.randint(1, 2)
                subtotal = p.price * qty
                new_invoice_items.append(InvoiceItem(
                    invoice_id=inv.id, product_service_id=p.id,
                    quantity=qty, unit_price=p.price, subtotal=subtotal
                ))

        db.add_all(new_invoice_items)
        db.commit()
        print(f"    ✅ 25 invoices")
    else:
        print(f"    ⚠️  Invoices already exist ({existing_inv_count}), skipping")

    # ── Orders ──
    # Find client users in this business
    biz_clients = db.query(User).filter(
        User.business_number == business_number,
        User.account_type == "client"
    ).all()
    client_id = biz_clients[0].id if biz_clients else owner_id

    existing_order_count = db.query(Order).filter(Order.client_id == client_id).count()
    if existing_order_count < 5:
        print(f"    📦 Generating orders...")
        statuses = ["completed", "completed", "completed", "pending", "accepted", "processing", "delayed", "cancelled"]
        payments = ["cash", "card", "card", "online", "gcash"]
        new_order_items = []

        for i in range(20):
            days_ago = random.randint(0, 45)
            order_date = datetime.utcnow() - timedelta(days=days_ago, hours=random.randint(0, 23))
            o_num = f"ORD-{business_number[:4]}-{random.randint(10000, 99999)}"

            num_items = random.randint(1, 3)
            selected = random.sample(all_items, min(num_items, len(all_items)))
            total = sum(p.price * random.randint(1, 2) for p in selected)

            order = Order(
                order_number=o_num, client_id=client_id,
                status=random.choice(statuses),
                total_amount=total,
                payment_method=random.choice(payments),
                created_at=order_date, updated_at=order_date
            )
            db.add(order)
            db.flush()

            for p in selected:
                qty = random.randint(1, 2)
                subtotal = p.price * qty
                new_order_items.append(OrderItem(
                    order_id=order.id, product_service_id=p.id,
                    quantity=qty, unit_price=p.price, subtotal=subtotal
                ))

        db.add_all(new_order_items)
        db.commit()
        print(f"    ✅ 20 orders")
    else:
        print(f"    ⚠️  Orders already exist ({existing_order_count}), skipping")

    # ── Reservations ──
    if all_services:
        existing_res_count = db.query(Reservation).filter(Reservation.client_id == client_id).count()
        if existing_res_count < 3:
            print(f"    📋 Generating reservations...")
            res_statuses = ["pending", "accepted", "in_progress", "completed", "completed", "delayed", "cancelled"]
            reservations = []
            for i in range(10):
                res_num = f"RES-{business_number[:4]}-{random.randint(4000, 9999)}"
                service = random.choice(all_services)
                res_loc = random.choice(locations)
                reservations.append(Reservation(
                    reservation_number=res_num, client_id=client_id,
                    service_id=service.id, location_id=res_loc.id,
                    vehicle_plate=f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))}-{random.randint(100,999)}",
                    status=random.choice(res_statuses),
                    queue_position=i + 1,
                    created_at=datetime.utcnow() - timedelta(hours=random.randint(1, 72))
                ))
            db.add_all(reservations)
            db.commit()
            print(f"    ✅ 10 reservations")
        else:
            print(f"    ⚠️  Reservations already exist ({existing_res_count}), skipping")


def cleanup_old_demos(db):
    """Update old demo accounts to be properly unlinked or reassigned."""
    # Fix demo-staff if it exists — it's now replaced by staff@carwash.com
    old_staff = db.query(User).filter(User.email == "demo-staff@carwash.com").first()
    if old_staff:
        old_staff.business_number = OWNER_BUSINESS_NUMBER
        old_staff.account_type = "staff"
        print("  ✅ Updated demo-staff@carwash.com → linked to owner's business")

    # Fix demo-admin if it exists — it's now replaced by admin@carwash.com
    old_admin = db.query(User).filter(User.email == "demo-admin@carwash.com").first()
    if old_admin:
        old_admin.business_number = OWNER_BUSINESS_NUMBER
        old_admin.account_type = "admin"
        print("  ✅ Updated demo-admin@carwash.com → linked to owner's business")
    
    db.commit()


def main():
    db = SessionLocal()
    try:
        print("\n" + "=" * 65)
        print("🚗 CAR WASH DEMO ACCOUNTS & DATA SETUP")
        print("=" * 65)

        # Step 1: Ensure roles
        print("\n📋 Step 1: Ensuring roles...")
        roles = ensure_roles(db)

        # Step 2: Setup accounts
        print("\n👤 Step 2: Setting up accounts...")
        owner = setup_owner(db, roles)
        staff = setup_staff_demo(db, roles, owner)
        admin = setup_admin_demo(db, roles, owner)
        client = setup_client_demo(db, roles)

        # Step 3: Cleanup old demo accounts
        print("\n🧹 Step 3: Cleaning up old demo accounts...")
        cleanup_old_demos(db)

        # Step 4: Setup second business
        print("\n🏢 Step 4: Creating second business (for data isolation testing)...")
        owner2 = setup_second_business(db, roles)
        
        # Create a client for the second business
        client2 = db.query(User).filter(User.email == "client@sparklewash.com").first()
        if not client2:
            client2 = create_user(db, "client@sparklewash.com", "client123", is_demo=False)
        client2.account_type = "client"
        client2.business_number = SECOND_BUSINESS_NUMBER
        if roles["client"] not in client2.roles:
            client2.roles.clear()
            client2.roles.append(roles["client"])
        db.commit()
        print(f"  ✅ client@sparklewash.com → client, business={SECOND_BUSINESS_NUMBER}")

        # Step 5: Demo limits
        print("\n⚙️  Step 5: Configuring demo limits...")
        setup_demo_limits(db, [staff, admin, client])

        # Step 6: Seed data for Business 1 (BuxWash)
        print("\n" + "-" * 65)
        print("📊 Step 6: Seeding data for Business 1 — BuxWash")
        seed_business_data(db, owner, "BuxWash", OWNER_BUSINESS_NUMBER)

        # Step 7: Seed data for Business 2 (SparkleWash)
        print("\n" + "-" * 65)
        print("📊 Step 7: Seeding data for Business 2 — SparkleWash")
        seed_business_data(db, owner2, "SparkleWash", SECOND_BUSINESS_NUMBER)

        # Summary
        print("\n" + "=" * 65)
        print("✅ SETUP COMPLETE!")
        print("=" * 65)
        print("""
╔══════════════════════════════════════════════════════════════╗
║  BUSINESS 1: BuxWash (BXTK-001)                             ║
╠══════════════════════════════════════════════════════════════╣
║  👑 Owner    : owner@carwash.com / owner123     (superadmin) ║
║  🔧 Admin    : admin@carwash.com / admin123     (admin)      ║
║  👷 Staff    : staff@carwash.com / staff123     (user/staff)  ║
║  🛒 Client   : demo-client@carwash.com / demo123 (client)    ║
╠══════════════════════════════════════════════════════════════╣
║  BUSINESS 2: SparkleWash (WASH-002) — Isolation Test         ║
╠══════════════════════════════════════════════════════════════╣
║  👑 Owner    : owner2@sparklewash.com / owner123 (admin)     ║
║  🛒 Client   : client@sparklewash.com / client123 (client)   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔒 Data Isolation: Each business sees ONLY its own data.    ║
║  🚫 Staff Sidebar: Settings tab hidden from staff accounts.  ║
╚══════════════════════════════════════════════════════════════╝
""")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
