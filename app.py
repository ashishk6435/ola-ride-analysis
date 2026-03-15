import streamlit as st
import pandas as pd
import pyodbc

st.set_page_config(page_title="OLA Ride Analytics Dashboard", layout="wide")

st.title("🚖 OLA Ride Analytics Dashboard")

# ---------------------------
# SQL CONNECTION
# ---------------------------

conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=MSI\SQLEXPRESS01;"
    "DATABASE=ola;"
    "Trusted_Connection=yes;"
)

def run_query(query):
    return pd.read_sql(query, conn)


# ---------------------------
# SIDEBAR
# ---------------------------

menu = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "SQL Analysis", "Power BI Dashboard"]
)


vehicle_types = run_query("SELECT DISTINCT Vehicle_Type FROM ola_clean_data")

vehicle_filter = st.sidebar.selectbox(
    "Filter by Vehicle Type",
    ["All"] + vehicle_types["Vehicle_Type"].tolist()
)


payment_methods = run_query("SELECT DISTINCT Payment_Method FROM ola_clean_data")

payment_filter = st.sidebar.selectbox(
    "Filter by Payment Method",
    ["All"] + payment_methods["Payment_Method"].tolist()
)


# ---------------------------
# FILTER CONDITION
# ---------------------------

filter_condition = "WHERE 1=1"

if vehicle_filter != "All":
    filter_condition += f" AND Vehicle_Type = '{vehicle_filter}'"

if payment_filter != "All":
    filter_condition += f" AND Payment_Method = '{payment_filter}'"



# ===========================
# DASHBOARD
# ===========================

if menu == "Dashboard":

    st.header("📊 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    rides_query = f"""
    SELECT COUNT(*) as Total_Rides
    FROM ola_clean_data
    {filter_condition}
    """

    rides = run_query(rides_query).iloc[0][0]

    col1.metric("Total Rides", rides)


    revenue_query = f"""
    SELECT SUM(Booking_Value) as Revenue
    FROM ola_clean_data
    {filter_condition}
    """

    revenue = run_query(revenue_query).iloc[0][0]

    col2.metric("Total Revenue", round(revenue,2))


    rating_query = f"""
    SELECT AVG(Customer_Rating) as Avg_Rating
    FROM ola_clean_data
    {filter_condition}
    """

    rating = run_query(rating_query).iloc[0][0]

    col3.metric("Avg Customer Rating", round(rating,2))


    cancel_query = f"""
    SELECT COUNT(*) as Cancelled
    FROM ola_clean_data
    {filter_condition}
    AND Booking_Status = 'Canceled'
    """

    cancelled = run_query(cancel_query).iloc[0][0]

    col4.metric("Cancelled Rides", cancelled)


    st.divider()


    # Ride Volume
    st.subheader("Ride Volume Over Time")

    volume_query = f"""
    SELECT Date, COUNT(*) as Total_Rides
    FROM ola_clean_data
    {filter_condition}
    GROUP BY Date
    ORDER BY Date
    """

    df_volume = run_query(volume_query)

    st.line_chart(df_volume.set_index("Date"))


    # Vehicle distribution
    st.subheader("Vehicle Type Distribution")

    vehicle_query = f"""
    SELECT Vehicle_Type, COUNT(*) as Total
    FROM ola_clean_data
    {filter_condition}
    GROUP BY Vehicle_Type
    """

    df_vehicle = run_query(vehicle_query)

    st.bar_chart(df_vehicle.set_index("Vehicle_Type"))



# ===========================
# SQL ANALYSIS
# ===========================

elif menu == "SQL Analysis":

    st.header("SQL Query Insights")

    query = """
    SELECT TOP 20 *
    FROM ola_clean_data
    """

    df = run_query(query)

    st.dataframe(df)



    st.subheader("Top 5 Customers by Rides")

    top_customer_query = """
    SELECT TOP 5 Customer_ID,
           COUNT(Booking_ID) as Total_Rides
    FROM ola_clean_data
    GROUP BY Customer_ID
    ORDER BY Total_Rides DESC
    """

    df_customers = run_query(top_customer_query)

    st.bar_chart(df_customers.set_index("Customer_ID"))



    st.subheader("Average Ride Distance by Vehicle")

    distance_query = """
    SELECT Vehicle_Type,
           AVG(Ride_Distance) as Avg_Ride_Distance
    FROM ola_clean_data
    GROUP BY Vehicle_Type
    """

    df_distance = run_query(distance_query)

    st.bar_chart(df_distance.set_index("Vehicle_Type"))



# ===========================
# POWER BI
# ===========================

elif menu == "Power BI Dashboard":

    st.header("📈 Power BI Dashboard")

    powerbi_url = "https://app.powerbi.com/groups/me/reports/d3113084-9a03-4bea-940c-0f7af4d1108a/55324bb53baec4314514?experience=power-bi"

    st.components.v1.iframe(powerbi_url, width=1200, height=700)