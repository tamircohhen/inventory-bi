import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import streamlit as st
from sklearn.linear_model import LinearRegression
import numpy as np

# --- חיבור ל-DB ---
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

st.set_page_config(page_title="מערכת BI לניהול מלאי", layout="wide")

# --- שאילתות ---
@st.cache_data(ttl=300)
def q(sql, params=None):
    with engine.begin() as conn:
        return pd.read_sql(text(sql), conn, params=params)

# --- עיצוב CSS מותאם ---
st.markdown("""
<style>
    .block-container { max-width: 1300px; margin: auto; }
    h1 { color: #2c3e50; text-align: center; font-weight: bold; }
    h2 { color: #1f77b4; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

st.title("📊 מערכת BI לניהול מלאי")

# --- KPI ---
low_stock = q("""
SELECT p.name, i.quantity_in_stock, p.reorder_level
FROM products p
JOIN inventory i ON i.product_id = p.product_id
WHERE i.quantity_in_stock < p.reorder_level
ORDER BY i.quantity_in_stock ASC
""")

total_stock = q("SELECT SUM(quantity_in_stock) AS total FROM inventory;")["total"].iloc[0]
distinct_products = q("SELECT COUNT(*) AS c FROM products;")["c"].iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("📦 מוצרים מתחת לרף", len(low_stock))
col2.metric("🏭 סה״כ מלאי", int(total_stock))
col3.metric("🛒 מספר מוצרים", int(distinct_products))

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["📈 מכירות", "📦 מלאי", "🔮 תחזית", "📑 SQL חופשי"])

# --- טאב מכירות ---
with tab1:
    sales_monthly = q("""
    SELECT DATE_TRUNC('month', sale_date) AS month, SUM(quantity_sold) AS total_sold
    FROM sales
    GROUP BY 1
    ORDER BY 1;
    """)
    sales_monthly["month"] = pd.to_datetime(sales_monthly["month"])
    
    fig = px.line(sales_monthly, x="month", y="total_sold", markers=True, title="מכירות חודשיות")
    st.plotly_chart(fig, use_container_width=True)

    by_cat = q("""
    SELECT p.category, DATE_TRUNC('month', s.sale_date) AS month, SUM(s.quantity_sold) AS qty
    FROM sales s
    JOIN products p ON s.product_id = p.product_id
    GROUP BY p.category, month
    ORDER BY month;
    """)
    pivot = by_cat.pivot_table(index="month", columns="category", values="qty", aggfunc="sum").fillna(0)
    fig2 = px.area(pivot, title="פילוח מכירות לפי קטגוריה")
    st.plotly_chart(fig2, use_container_width=True)

# --- טאב מלאי ---
with tab2:
    inv_cat = q("""
    SELECT p.category, SUM(i.quantity_in_stock) AS qty
    FROM inventory i
    JOIN products p ON p.product_id = i.product_id
    GROUP BY p.category
    ORDER BY p.category;
    """)
    fig3 = px.bar(inv_cat, x="category", y="qty", text_auto=True, title="מלאי לפי קטגוריה")
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("מוצרים מתחת לרף")
    st.dataframe(low_stock, use_container_width=True)

# --- טאב תחזית ---
with tab3:
    st.subheader("חיזוי מכירות (Linear Regression)")
    X = np.arange(len(sales_monthly)).reshape(-1,1)
    y = sales_monthly["total_sold"].values
    model = LinearRegression().fit(X, y)
    future_x = np.arange(len(sales_monthly)+6).reshape(-1,1)
    pred = model.predict(future_x)

    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=sales_monthly["month"], y=y, mode="lines+markers", name="מכירות בפועל"))
    future_dates = pd.date_range(sales_monthly["month"].max(), periods=7, freq="M")
    fig4.add_trace(go.Scatter(x=future_dates, y=pred[-7:], mode="lines+markers", name="תחזית"))
    st.plotly_chart(fig4, use_container_width=True)

# --- טאב SQL חופשי ---
with tab4:
    sql_code = st.text_area("הדבק כאן SQL:", "SELECT * FROM products LIMIT 5;")
    if st.button("הרץ"):
        try:
            df = q(sql_code)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"שגיאה: {e}")
