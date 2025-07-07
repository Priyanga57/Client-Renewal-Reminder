import streamlit as st
import pandas as pd
from datetime import datetime

# ✅ Google Sheet (export as CSV)
sheet_url = "https://docs.google.com/spreadsheets/d/17_HyRiUA3UMSt6uOOS_vTa29YbeCIuSCbP6XjsuUdg8/export?format=csv"

# Set page configuration
st.set_page_config(page_title="📊 Client Renewal Dashboard", layout="wide")

# 🎨 Custom Styles
st.markdown("""
    <style>
    body {
        background-color: #191970;
    }
    .block-container {
        padding: 2rem 2rem 2rem 2rem;
        background-color: #212942 ;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .stMetricValue {
        font-size: 28px !important;
    }
    .stMetricLabel {
        color: #7f8c8d;
    }
    </style>
""", unsafe_allow_html=True)

# Load Data
df = pd.read_csv(sheet_url)

# Parse Date
df["Renewal Due Date"] = pd.to_datetime(df["Renewal Due Date"], errors='coerce')
today = pd.to_datetime(datetime.today().date())

# Title
st.title("🎯 Client Renewal Management Dashboard")
st.markdown("📌 **Live Dashboard to Track Renewals, Status & Automation**")

# Sidebar Filters
st.sidebar.header("🔍 Filter Clients")
service_filter = st.sidebar.multiselect("💼 Service Type", options=df["Service Type"].dropna().unique())
status_filter = st.sidebar.multiselect("📊 Status", options=df["Status"].dropna().unique())

# Apply filters
filtered_df = df.copy()
if service_filter:
    filtered_df = filtered_df[filtered_df["Service Type"].isin(service_filter)]
if status_filter:
    filtered_df = filtered_df[filtered_df["Status"].isin(status_filter)]

# Metrics
active_count = df[df["Status"] == "Active"].shape[0]
expiring_count = df[df["Status"] == "Expiring Soon"].shape[0]
expired_count = df[df["Status"] == "Expired"].shape[0]

st.markdown("---")
st.subheader("📈 Subscription Status Overview")
col1, col2, col3 = st.columns(3)
col1.metric("✅ Active", active_count)
col2.metric("⏳ Expiring Soon", expiring_count)
col3.metric("❌ Expired", expired_count)

# Expandable Detailed Lists by Status
st.markdown("---")
st.subheader("🧾 View Clients by Status")

with st.expander("✅ Active Clients"):
    active_df = df[df["Status"] == "Active"][["Client Name", "Service Type", "Renewal Due Date", "Contact Email"]]
    st.write(f"🔹 Total: {active_df.shape[0]}")
    st.dataframe(active_df, use_container_width=True)

with st.expander("⏳ Expiring Soon Clients"):
    expiring_df = df[df["Status"] == "Expiring Soon"][["Client Name", "Service Type", "Renewal Due Date", "Contact Email"]]
    st.write(f"🔸 Total: {expiring_df.shape[0]}")
    st.dataframe(expiring_df, use_container_width=True)

with st.expander("❌ Expired Clients"):
    expired_df = df[df["Status"] == "Expired"][["Client Name", "Service Type", "Renewal Due Date", "Contact Email"]]
    st.write(f"🔴 Total: {expired_df.shape[0]}")
    st.dataframe(expired_df, use_container_width=True)

# Full Filtered Table
st.markdown("---")
st.subheader("📋 Full Filtered Table View")
st.dataframe(filtered_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("✅ *Auto-updates when Google Sheet is edited*")
st.markdown("🔗 [Edit Google Sheet](https://docs.google.com/spreadsheets/d/17_HyRiUA3UMSt6uOOS_vTa29YbeCIuSCbP6XjsuUdg8/edit)")

