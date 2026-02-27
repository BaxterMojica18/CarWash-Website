import psycopg2
import subprocess

print("Checking PostgreSQL service...")
try:
    # Check if PostgreSQL service is running
    result = subprocess.run(['sc', 'query', 'postgresql-x64-15'], 
                          capture_output=True, text=True, shell=True)
    if 'RUNNING' in result.stdout:
        print("✅ PostgreSQL service is running")
    else:
        print("❌ PostgreSQL service is not running")
        print("Starting PostgreSQL service...")
        subprocess.run(['net', 'start', 'postgresql-x64-15'], shell=True)
except Exception as e:
    print(f"Service check failed: {e}")

print("\nTesting connection to postgres database...")
try:
    # Connect to default postgres database first
    conn = psycopg2.connect(
        user="postgres",
        password="NewSecurePass2025!",
        host="localhost",
        port="5432",
        database="postgres"
    )
    print("✅ Connected to PostgreSQL server!")
    
    # Create carwash_db database
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Check if database exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'carwash_db'")
    exists = cursor.fetchone()
    
    if not exists:
        print("Creating carwash_db database...")
        cursor.execute("CREATE DATABASE carwash_db")
        print("✅ Database carwash_db created successfully!")
    else:
        print("✅ Database carwash_db already exists")
    
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
    print("✅ Connected to carwash_db successfully!")
    conn.close()
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nTroubleshooting tips:")
    print("1. Make sure PostgreSQL is installed and running")
    print("2. Check if the password is correct")
    print("3. Verify PostgreSQL is listening on port 5432")
    print("4. Check Windows Services for PostgreSQL")