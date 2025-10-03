import os
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import streamlit as st

# --- הגדרות בסיס ---
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

st.set_page_config(page_title="מערכת ניהול מלאי", layout="wide")

# --- פונקציית עזר לשאילתות ---
@st.cache_data(ttl=300)
def q(sql, params=None):
    with engine.begin() as conn:
        return pd.read_sql(text(sql), conn, params=params)

# --- עיצוב מותאם ---
st.markdown("""
<style>
    .block-container { max-width: 1200px; margin: auto; }
    h1 { color: #1f77b4; text-align: center; font-family: Arial Black; }
    h2 { color: #2c3e50; }
</style>
""", unsafe_allow_html=True)

st.title("📊 דשבורד ניהול מלאי")

# --- KPI ראשיים ---
low_stock = q("""
SELECT p.product_id, p.name, p.category, i.quantity_in_stock, p.reorder_level
FROM products p
JOIN inventory i ON i.product_id = p.product_id
WHERE i.quantity_in_stock < p.reorder_level
ORDER BY i.quantity_in_stock ASC
LIMIT 20;
""")

total_stock = q("SELECT SUM(quantity_in_stock) AS total FROM inventory;")["total"].iloc[0]
distinct_products = q("SELECT COUNT(*) AS c FROM products;")["c"].iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("📦 מוצרים מתחת לרף", len(low_stock))
col2.metric("🏭 סה״כ מלאי במחסן", int(total_stock))
col3.metric("🛒 מספר מוצרים", int(distinct_products))

# --- טאבים ---
tab1, tab2, tab3 = st.tabs(["📈 מכירות", "📦 מלאי", "📑 שאילתה חופשית"])

# טאב מכירות
with tab1:
    st.subheader("מכירות חודשיות")
    sales_monthly = q("""
    SELECT DATE_TRUNC('month', sale_date) AS month, SUM(quantity_sold) AS total_sold
    FROM sales
    GROUP BY 1
    ORDER BY 1;
    """)
    sales_monthly = sales_monthly.rename(columns={"month": "חודש", "total_sold": "כמות"})
    fig = px.line(sales_monthly, x="חודש", y="כמות", markers=True, title="מכירות חודשיות")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("מכירות לפי קטגוריה")
    by_cat = q("""
    SELECT p.category, DATE_TRUNC('month', s.sale_date) AS month, SUM(s.quantity_sold) AS qty
    FROM sales s
    JOIN products p ON p.product_id = s.product_id
    GROUP BY p.category, month
    ORDER BY month;
    """)
    pivot = by_cat.pivot_table(index="month", columns="category", values="qty", aggfunc="sum").fillna(0)
    fig2 = px.area(pivot, title="פילוח מכירות לפי קטגוריה")
    st.plotly_chart(fig2, use_container_width=True)

# טאב מלאי
with tab2:
    st.subheader("מלאי נמוך")
    st.dataframe(low_stock, use_container_width=True)

    st.subheader("פילוח מלאי לפי קטגוריה")
    inv_cat = q("""
    SELECT p.category, SUM(i.quantity_in_stock) AS qty
    FROM inventory i
    JOIN products p ON p.product_id = i.product_id
    GROUP BY p.category
    ORDER BY p.category;
    """)
    fig3 = px.bar(inv_cat, x="category", y="qty", title="מלאי לפי קטגוריה", text_auto=True)
    st.plotly_chart(fig3, use_container_width=True)

# טאב שאילתה חופשית
with tab3:
    st.subheader("הרץ שאילתה חופשית")
    sql_code = st.text_area("הדבק כאן SQL:", "SELECT * FROM products LIMIT 5;")
    if st.button("הרץ"):
        try:
            df = q(sql_code)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"שגיאה: {e}")

st.caption("🕒 רענון נתונים כל 5 דקות")
