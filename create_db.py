import psycopg2

print("Testing connection to PostgreSQL...")
try:
    # Connect to default postgres database first
    conn = psycopg2.connect(
        user="postgres",
        password="NewSecurePass2025!",
        host="localhost",
        port="5432",
        database="postgres"
    )
    print("[OK] Connected to PostgreSQL server!")
    
    # Create carwash_db database
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Check if database exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'carwash_db'")
    exists = cursor.fetchone()
    
    if not exists:
        print("Creating carwash_db database...")
        cursor.execute("CREATE DATABASE carwash_db")
        print("[OK] Database carwash_db created successfully!")
    else:
        print("[OK] Database carwash_db already exists")
    
    cursor.close()
    conn.close()
    
    # Now test connection to carwash_db
    print("\nTesting connection to carwash_db...")
    conn = psycopg2.connect(
        user="postgres",
        password="NewSecurePass2025!",
        host="localhost",
        port="5432",
        database="carwash_db"
    )
    print("[OK] Connected to carwash_db successfully!")
    conn.close()
    
except Exception as e:
    print(f"[ERROR] Connection failed: {e}")
    print("\nTroubleshooting tips:")
    print("1. Make sure PostgreSQL is installed and running")
    print("2. Check if the password is correct")
    print("3. Verify PostgreSQL is listening on port 5432")
    print("4. Check Windows Services for PostgreSQL")