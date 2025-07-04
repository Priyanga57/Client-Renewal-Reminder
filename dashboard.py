import streamlit as st
import pandas as pd

# === PAGE CONFIG ===
st.set_page_config(page_title="📊 Client Renewal Dashboard", layout="wide")

# === LOAD DATA FROM GOOGLE SHEET ===
sheet_url = "https://docs.google.com/spreadsheets/d/17_HyRiUA3UMSt6uOOS_vTa29YbeCIuSCbP6XjsuUdg8/export?format=csv"
try:
    df = pd.read_csv(sheet_url)
except Exception as e:
    st.error(f"❌ Failed to load data: {e}")
    st.stop()

# === STYLE ===
st.markdown("""
    <style>
        body {
            background-color: #212942;
        }
        .block-container {
            padding: 2rem;
            background-color: #191970;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }
        .stMetricValue {
            font-size: 28px !important;
        }
        .stMetricLabel {
            color: #7f8c8d;
        }
        .dataframe th, .dataframe td {
            padding: 0.5rem;
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

# === HEADER ===
st.title("🎯 Client Renewal Management Dashboard")
st.markdown("📌 **Live tracking of onboarding, renewals, and AMC status.**")

# === FILTERS ===
st.sidebar.header("🔍 Filter Options")
service_filter = st.sidebar.multiselect("💼 Service Type", df["Service Type"].unique())
status_filter = st.sidebar.multiselect("📊 Status", df["Status"].unique())

filtered_df = df.copy()
if service_filter:
    filtered_df = filtered_df[filtered_df["Service Type"].isin(service_filter)]
if status_filter:
    filtered_df = filtered_df[filtered_df["Status"].isin(status_filter)]

# === METRICS ===
st.markdown("---")
st.subheader("📈 Overview Metrics")

active = df[df["Status"] == "Active"].shape[0]
expiring = df[df["Status"] == "Expiring Soon"].shape[0]
expired = df[df["Status"] == "Expired"].shape[0]

col1, col2, col3 = st.columns(3)
col1.metric("✅ Active", active)
col2.metric("⏳ Expiring Soon", expiring)
col3.metric("❌ Expired", expired)

# === CLIENT DATA TABLE ===
st.markdown("---")
st.subheader("📋 Client Records")

st.dataframe(
    filtered_df.style.set_properties(**{
        'background-color': '#ADD8E6',
        'color': '#2c3e50',
        'border-color': '#dfe6e9'
    }),
    use_container_width=True
)

# === FOOTER ===
st.markdown("---")
st.markdown("""
💡 **Tips**:
- Update data directly in this [Google Sheet](https://docs.google.com/spreadsheets/d/17_HyRiUA3UMSt6uOOS_vTa29YbeCIuSCbP6XjsuUdg8/edit?usp=sharing)
- All changes reflect **live** on this dashboard.
- Share this dashboard with your boss for live insights and filtering.
""")
