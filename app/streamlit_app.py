import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import streamlit as st

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

st.set_page_config(page_title="ניהול מלאי", layout="wide")
st.title("דשבורד ניהול מלאי")

@st.cache_data(ttl=300)
def q(sql, params=None):
    with engine.begin() as conn:
        return pd.read_sql(text(sql), conn, params=params)

col1, col2, col3 = st.columns(3)

low_stock = q("""
SELECT p.product_id, p.name, p.category, i.quantity_in_stock, p.reorder_level
FROM products p
JOIN inventory i ON i.product_id = p.product_id
WHERE i.quantity_in_stock < p.reorder_level
ORDER BY i.quantity_in_stock ASC
LIMIT 20;
""")
col1.metric("מוצרים מתחת לרף הזמנה", len(low_stock))
total_stock = q("SELECT SUM(quantity_in_stock) AS total FROM inventory;")["total"].iloc[0]
col2.metric("סה״כ כמות במחסן", int(total_stock))
distinct_products = q("SELECT COUNT(*) AS c FROM products;")["c"].iloc[0]
col3.metric("מספר מוצרים", int(distinct_products))

st.subheader("מלאי נמוך")
st.dataframe(low_stock, use_container_width=True)

st.subheader("מכירות חודשיות")
sales_monthly = q("""
SELECT DATE_TRUNC('month', sale_date) AS month, SUM(quantity_sold) AS total_sold
FROM sales
GROUP BY 1
ORDER BY 1;
""")
sales_monthly = sales_monthly.rename(columns={"month":"חודש", "total_sold":"כמות"})
sales_monthly = sales_monthly.set_index("חודש")
st.line_chart(sales_monthly)

st.subheader("מכירות לפי קטגוריה")
by_cat = q("""
SELECT p.category, DATE_TRUNC('month', s.sale_date) AS month, SUM(s.quantity_sold) AS qty
FROM sales s
JOIN products p ON p.product_id = s.product_id
GROUP BY p.category, month
ORDER BY month;
""")
pivot = by_cat.pivot_table(index="month", columns="category", values="qty", aggfunc="sum").fillna(0)
st.area_chart(pivot)

st.subheader("פילוח מלאי לפי קטגוריה")
inv_cat = q("""
SELECT p.category, SUM(i.quantity_in_stock) AS qty
FROM inventory i
JOIN products p ON p.product_id = i.product_id
GROUP BY p.category
ORDER BY p.category;
""")
st.bar_chart(inv_cat.set_index("category"))

st.caption("רענון נתונים כל חמש דקות")
