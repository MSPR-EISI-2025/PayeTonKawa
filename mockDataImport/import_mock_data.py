import os
import sys
import traceback
from datetime import datetime

print("🚀 Starting data import script...")

try:
    import requests
    import pymysql
    import random

    BASE_URL = "https://681b6c5e17018fe5057b864b.mockapi.io/api/v1"
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", 3306)),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "test"),
        "charset": "utf8mb4",
    }

    print("🔌 Connecting to database at", DB_CONFIG["host"], ":", DB_CONFIG["port"])
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SET NAMES utf8mb4 COLLATE utf8mb4_general_ci;")
    print("✅ Connected to DB!")

except Exception as e:
    print("❌ Exception occurred during setup:")
    traceback.print_exc()
    sys.exit(1)


def format_datetime(iso_string):
    try:
        return datetime.fromisoformat(iso_string.replace("Z", "")).strftime("%Y-%m-%d %H:%M:%S")
    except:
        return None

def fetch_data(endpoint):
    response = requests.get(f"{BASE_URL}/{endpoint}")
    response.raise_for_status()
    return response.json()

def create_tables(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id VARCHAR(255) PRIMARY KEY,
            createdAt DATETIME,
            name VARCHAR(255),
            username VARCHAR(255),
            firstName VARCHAR(255),
            lastName VARCHAR(255),
            address_postalCode VARCHAR(20),
            address_city VARCHAR(255),
            profile_firstName VARCHAR(255),
            profile_lastName VARCHAR(255),
            company_name VARCHAR(255)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id VARCHAR(255) PRIMARY KEY,
            createdAt DATETIME,
            name VARCHAR(255),
            price DECIMAL(10,2),
            description TEXT,
            color VARCHAR(50),
            stock VARCHAR(255)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id VARCHAR(255) PRIMARY KEY,
            createdAt DATETIME,
            customer_id VARCHAR(255),
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id VARCHAR(255),
            product_id VARCHAR(255),
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)



def insert_customers(cursor, customers):
    for c in customers:
        created_at = format_datetime(c["createdAt"])
        cursor.execute("""
            REPLACE INTO customers VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            c["id"], created_at, c["name"], c["username"],
            c["firstName"], c["lastName"],
            c.get("address", {}).get("postalCode"),
            c.get("address", {}).get("city"),
            c.get("profile", {}).get("firstName"),
            c.get("profile", {}).get("lastName"),
            c.get("company", {}).get("companyName")
        ))

def insert_orders(cursor, orders, customer_ids, product_ids):
    for o in orders:
        created_at = format_datetime(o["createdAt"])
        customer_id = random.choice(customer_ids)
        cursor.execute("""
            REPLACE INTO orders (id, createdAt, customer_id) VALUES (%s, %s, %s)
        """, (o["id"], created_at, customer_id))

        # Link 1 or 2 random products
        linked_products = random.sample(product_ids, k=random.choice([1, 2]))
        for product_id in linked_products:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id) VALUES (%s, %s)
            """, (o["id"], product_id))


def insert_products(cursor, products):
    for p in products:
        created_at = format_datetime(p["createdAt"])
        price = p.get("details", {}).get("price")
        try:
            price = float(price)
        except:
            price = 0.0
        cursor.execute("""
            REPLACE INTO products VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            p["id"], created_at, p["name"],
            price,
            p.get("details", {}).get("description"),
            p.get("details", {}).get("color"),
            p.get("stock")
        ))


def main():
    print("🚀 Starting data import script...")

    print("📦 Creating tables...")
    create_tables(cursor)
    print("✅ Tables created.")

    print("Fetching and inserting customers...")
    customers = fetch_data("customers")
    insert_customers(cursor, customers)
    customer_ids = [c["id"] for c in customers]

    print("Fetching and inserting products...")
    products = fetch_data("products")
    insert_products(cursor, products)
    product_ids = [p["id"] for p in products]

    print("Fetching and inserting orders...")
    orders = fetch_data("orders")
    insert_orders(cursor, orders, customer_ids, product_ids)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Data import completed.")

if __name__ == "__main__":
    print("🧪 TEST: main() is about to run.")
    main()