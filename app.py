import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Retail BI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Helper Function: Load Data ---
@st.cache_data
def load_data(query):
    # db is expected to be in the parent directory if running from dashboard/, or same dir if from root
    db_path = 'retail_dw.db' if os.path.exists('retail_dw.db') else '../retail_dw.db'
    if not os.path.exists(db_path):
        st.error(f"Database not found at {db_path}. Please run `etl_pipeline.py` first.")
        return pd.DataFrame()
    
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# --- UI Styling ---
st.markdown(
    """
    <style>
    .metric-card {
        background-color: #1e1e2f;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #4CAF50;
    }
    .metric-label {
        font-size: 16px;
        color: #cccccc;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Retail Data Analytics")
st.markdown("Dashboard uniquely generated for your **Retail Sales Data Set**.")

# --- Fetch Initial Base Data ---
base_query = 'SELECT * FROM Sales_Analytics'
try:
    df = load_data(base_query)
except Exception as e:
    st.error("Could not load data. Run `etl_pipeline.py` first.")
    st.stop()

if df.empty:
    st.stop()

# --- Filters ---
st.sidebar.header("Dashboard Filters")

# Gender Filter
genders = df['Gender'].unique().tolist()
selected_gender = st.sidebar.selectbox("Select Gender", ["All"] + genders)

# Age Group Filter
age_groups = df['Age Group'].unique().tolist()
selected_age_group = st.sidebar.selectbox("Select Age Group", ["All"] + age_groups)

# Category Filter
categories = df['Product Category'].unique().tolist()
selected_category = st.sidebar.selectbox("Select Category", ["All"] + categories)

# --- Apply Filters ---
filtered_df = df.copy()

if selected_gender != "All":
    filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]

if selected_age_group != "All":
    filtered_df = filtered_df[filtered_df['Age Group'] == selected_age_group]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df['Product Category'] == selected_category]

# --- KPIs ---
total_revenue = filtered_df['Total Amount'].sum()
total_items = filtered_df['Quantity'].sum()
total_transactions = len(filtered_df)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Total Revenue</div><div class="metric-value">${total_revenue:,.2f}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Items Sold</div><div class="metric-value">{total_items:,}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Transactions</div><div class="metric-value">{total_transactions:,}</div></div>', unsafe_allow_html=True)

st.divider()

# --- Visualizations ---
st.subheader("Sales Trends")

# 1. Sales Trend over Time
trend_df = filtered_df.groupby('Date')['Total Amount'].sum().reset_index()
if not trend_df.empty:
    fig_line = px.line(trend_df, x="Date", y="Total Amount", title="Revenue Over Time",
                       line_shape="spline", render_mode="svg", color_discrete_sequence=['#00BFFF'])
    col_trend, = st.columns(1)
    col_trend.plotly_chart(fig_line, use_container_width=True)

col1, col2 = st.columns(2)

# 2. Revenue by Category
with col1:
    st.subheader("Revenue by Category")
    cat_df = filtered_df.groupby('Product Category')['Total Amount'].sum().reset_index()
    if not cat_df.empty:
        fig_pie = px.pie(cat_df, values='Total Amount', names='Product Category', hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig_pie, use_container_width=True)

# 3. Revenue by Gender & Age Group
with col2:
    st.subheader("Revenue by Demographics")
    demo_df = filtered_df.groupby(['Age Group', 'Gender'])['Total Amount'].sum().reset_index()
    if not demo_df.empty:
        fig_bar = px.bar(demo_df, x='Age Group', y='Total Amount', color='Gender', barmode='group',
                         title="Revenue per Age Group by Gender",
                         color_discrete_sequence=['#ff9999', '#66b3ff'])
        st.plotly_chart(fig_bar, use_container_width=True)


# --- Detailed Data View ---
st.subheader("Dataset View")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
