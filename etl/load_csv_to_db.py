import os
import random
from datetime import date, timedelta
from dotenv import load_dotenv
from faker import Faker
import pandas as pd
from sqlalchemy import create_engine, text

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_pre_ping=True,
)

fake = Faker()
Faker.seed(42)
random.seed(42)

with engine.begin() as conn:
    conn.execute(text(open("sql/schema.sql", "r", encoding="utf-8").read()))

categories = ["אלקטרוניקה", "מזון", "טואלטיקה", "ביגוד", "משרד"]
products = []
for i in range(100):
    products.append({
        "name": f"מוצר {i+1}",
        "category": random.choice(categories),
        "price": round(random.uniform(5, 500), 2),
        "reorder_level": random.randint(5, 40)
    })
df_products = pd.DataFrame(products)

with engine.begin() as conn:
    df_products.to_sql("products", conn, if_exists="append", index=False)

inv_rows = []
with engine.begin() as conn:
    prod_ids = pd.read_sql("SELECT product_id FROM products", conn)["product_id"].tolist()
for pid in prod_ids:
    inv_rows.append({
        "product_id": pid,
        "quantity_in_stock": random.randint(0, 200),
        "warehouse_location": f"A{random.randint(1,10)}-R{random.randint(1,20)}"
    })
df_inv = pd.DataFrame(inv_rows)

customers = [{"name": fake.name()} for _ in range(200)]
df_customers = pd.DataFrame(customers)

suppliers = [{"name": fake.company(), "contact_info": fake.phone_number()} for _ in range(10)]
df_suppliers = pd.DataFrame(suppliers)

with engine.begin() as conn:
    df_inv.to_sql("inventory", conn, if_exists="append", index=False)
    df_customers.to_sql("customers", conn, if_exists="append", index=False)
    df_suppliers.to_sql("suppliers", conn, if_exists="append", index=False)

sales_rows = []
start = date.today() - timedelta(days=365)
with engine.begin() as conn:
    prod_ids = pd.read_sql("SELECT product_id FROM products", conn)["product_id"].tolist()
    cust_ids = pd.read_sql("SELECT customer_id FROM customers", conn)["customer_id"].tolist()

for _ in range(5000):
    d = start + timedelta(days=random.randint(0, 365))
    sales_rows.append({
        "product_id": random.choice(prod_ids),
        "customer_id": random.choice(cust_ids),
        "quantity_sold": random.randint(1, 8),
        "sale_date": d
    })
df_sales = pd.DataFrame(sales_rows)

order_rows = []
with engine.begin() as conn:
    sup_ids = pd.read_sql("SELECT supplier_id FROM suppliers", conn)["supplier_id"].tolist()
for _ in range(400):
    order_rows.append({
        "supplier_id": random.choice(sup_ids),
        "product_id": random.choice(prod_ids),
        "order_date": start + timedelta(days=random.randint(0, 365)),
        "quantity_ordered": random.randint(10, 150),
        "status": random.choice(["pending", "shipped", "received"])
    })
df_orders = pd.DataFrame(order_rows)

with engine.begin() as conn:
    df_sales.to_sql("sales", conn, if_exists="append", index=False)
    df_orders.to_sql("orders", conn, if_exists="append", index=False)

print("Done seeding data.")
