import streamlit as st
import pandas as pd

st.set_page_config(page_title="OLA Ride Analytics Dashboard", layout="wide")

st.title("🚖 OLA Ride Analytics Dashboard")

# Load dataset
df = pd.read_csv("ola_clean_data.csv")

# Sidebar filters
st.sidebar.header("Filters")

vehicle_filter = st.sidebar.selectbox(
    "Vehicle Type",
    ["All"] + sorted(df["Vehicle_Type"].dropna().unique())
)

payment_filter = st.sidebar.selectbox(
    "Payment Method",
    ["All"] + sorted(df["Payment_Method"].dropna().unique())
)

# Apply filters
filtered_df = df.copy()

if vehicle_filter != "All":
    filtered_df = filtered_df[filtered_df["Vehicle_Type"] == vehicle_filter]

if payment_filter != "All":
    filtered_df = filtered_df[filtered_df["Payment_Method"] == payment_filter]


# KPI metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Rides", len(filtered_df))

col2.metric(
    "Total Revenue",
    round(filtered_df["Booking_Value"].sum(), 2)
)

col3.metric(
    "Average Rating",
    round(filtered_df["Customer_Rating"].mean(), 2)
)

st.divider()

# Ride volume
st.subheader("Ride Volume by Vehicle Type")

vehicle_counts = filtered_df["Vehicle_Type"].value_counts()

st.bar_chart(vehicle_counts)

# Payment distribution
st.subheader("Payment Method Distribution")

payment_counts = filtered_df["Payment_Method"].value_counts()

st.bar_chart(payment_counts)

# Dataset preview
st.subheader("Dataset Preview")

st.dataframe(filtered_df.head(50))