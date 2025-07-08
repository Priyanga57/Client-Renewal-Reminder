# dashboard.py

import streamlit as st
import pandas as pd
from config import GOOGLE_SHEET_CSV_URL

# 🎨 Page Settings
st.set_page_config(page_title="📊 Client Renewal Dashboard", layout="wide")

# 💡 Load data
@st.cache_data
def load_data():
    return pd.read_csv(GOOGLE_SHEET_CSV_URL)

df = load_data()

# 🧹 Clean and sort data
df["Status"] = df["Status"].fillna("Unknown")
df["Client Name"] = df["Client Name"].fillna("Unnamed Client")
df["Service Type"] = df["Service Type"].fillna("Unknown")

# 🎨 Sidebar Filters
st.sidebar.header("🔍 Filter Options")
statuses = sorted(df["Status"].dropna().unique().tolist())
services = sorted(df["Service Type"].dropna().unique().tolist())
clients = sorted(df["Client Name"].dropna().unique().tolist())

selected_status = st.sidebar.multiselect("📊 Status", statuses, default=statuses)
selected_service = st.sidebar.multiselect("💼 Service Type", services)
selected_client = st.sidebar.selectbox("👤 Select a Client", ["All"] + clients)

# 🎯 Apply Filters
filtered_df = df.copy()

if selected_status:
    filtered_df = filtered_df[filtered_df["Status"].isin(selected_status)]
if selected_service:
    filtered_df = filtered_df[filtered_df["Service Type"].isin(selected_service)]
if selected_client != "All":
    filtered_df = filtered_df[filtered_df["Client Name"] == selected_client]

# 🧮 Metrics Section
st.title("📊 Client Renewal Dashboard")
st.markdown("📌 Monitor client renewals and status from live Google Sheets data.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("✅ Active", df[df["Status"] == "Active"].shape[0])
col2.metric("⏳ Expiring Soon", df[df["Status"] == "Expiring Soon"].shape[0])
col3.metric("❌ Expired", df[df["Status"] == "Expired"].shape[0])
col4.metric("🔁 Transformed", df[df["Status"] == "Transform"].shape[0])

# 🧾 Selected Client Details
if selected_client != "All":
    st.subheader(f"📄 Detailed View for: `{selected_client}`")
    client_df = df[df["Client Name"] == selected_client]
    st.dataframe(client_df, use_container_width=True)

# 📋 Filtered Table View
st.markdown("---")
st.subheader("📋 Filtered Client Records")
st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

# ℹ️ Tips
st.markdown("""
---
💡 **Tips**:
- Use the sidebar filters to refine your view.
- This dashboard reflects real-time Google Sheets data.
- Selecting a client reveals their associated services.
""")
