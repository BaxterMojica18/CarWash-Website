import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import os
from urllib.parse import unquote

load_dotenv()

# Extract connection details from DATABASE_URL
db_url = os.getenv("DATABASE_URL")
# Format: postgresql://user:password@host:port/dbname

parts = db_url.replace("postgresql://", "").split("@")
user_pass = parts[0].split(":")
host_port_db = parts[1].split("/")
host_port = host_port_db[0].split(":")

user = unquote(user_pass[0])
password = unquote(user_pass[1]) if len(user_pass) > 1 else ""
host = host_port[0]
port = host_port[1]
dbname = host_port_db[1]

try:
    # Connect to PostgreSQL server (default postgres database)
    conn = psycopg2.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database="postgres"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Create database
    cursor.execute(f"CREATE DATABASE {dbname}")
    print(f"Database '{dbname}' created successfully!")
    
    cursor.close()
    conn.close()
except psycopg2.errors.DuplicateDatabase:
    print(f"Database '{dbname}' already exists.")
except Exception as e:
    print(f"Error: {e}")
