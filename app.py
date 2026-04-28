import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

# Title
st.title("🛒 E-commerce Sales Dashboard")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("ecom.csv") 
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")

region = st.sidebar.multiselect("Select Region", df["Region"].unique(), default=df["Region"].unique())
category = st.sidebar.multiselect("Select Category", df["Category"].unique(), default=df["Category"].unique())

df_filtered = df[(df["Region"].isin(region)) & (df["Category"].isin(category))]

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${df_filtered['Sales'].sum():,.2f}")
col2.metric("Total Profit", f"${df_filtered['Profit'].sum():,.2f}")
col3.metric("Total Orders", df_filtered.shape[0])

st.markdown("---")

# Sales by Category
fig1 = px.bar(df_filtered, x="Category", y="Sales", color="Category", title="Sales by Category")
st.plotly_chart(fig1, use_container_width=True)

# Profit by Region
fig2 = px.pie(df_filtered, names="Region", values="Profit", title="Profit by Region")
st.plotly_chart(fig2, use_container_width=True)

# Sales Trend
sales_trend = df_filtered.groupby("Order Date")["Sales"].sum().reset_index()
fig3 = px.line(sales_trend, x="Order Date", y="Sales", title="Sales Trend Over Time")
st.plotly_chart(fig3, use_container_width=True)

# Top Products
top_products = df_filtered.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10).reset_index()
fig4 = px.bar(top_products, x="Sales", y="Product Name", orientation="h", title="Top 10 Products")
st.plotly_chart(fig4, use_container_width=True)

# Data Table
st.subheader("Filtered Data")
st.dataframe(df_filtered)


