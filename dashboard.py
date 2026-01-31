import streamlit as st
import pandas as pd

# === PAGE CONFIG ===
st.set_page_config(page_title="📊 Client Renewal Dashboard", layout="wide")

# === LOAD DATA ===
sheet_url = "https://docs.google.com/spreadsheets/d/17_HyRiUA3UMSt6uOOS_vTa29YbeCIuSCbP6XjsuUdg8/export?format=csv"

try:
    df = pd.read_csv(sheet_url)
except Exception as e:
    st.error("❌ Unable to load Google Sheet")
    st.write(e)
    st.stop()

# === BASIC VALIDATION ===
required_cols = ["Service Type", "Status"]
for col in required_cols:
    if col not in df.columns:
        st.error(f"❌ Missing column: {col}")
        st.stop()

# === STYLE ===
st.markdown("""
<style>
.block-container {
    padding: 2rem;
    background-color: #212942;
    border-radius: 15px;
}
.stMetricValue {
    font-size: 28px !important;
}
</style>
""", unsafe_allow_html=True)

# === HEADER ===
st.title("🎯 Client Renewal Management Dashboard")
st.markdown("📌 **Live tracking of onboarding, renewals, and AMC status.**")

# === FILTERS ===
st.sidebar.header("🔍 Filter Options")

service_filter = st.sidebar.multiselect(
    "💼 Service Type",
    options=df["Service Type"].dropna().unique()
)

status_filter = st.sidebar.multiselect(
    "📊 Status",
    options=df["Status"].dropna().unique()
)

filtered_df = df.copy()

if service_filter:
    filtered_df = filtered_df[filtered_df["Service Type"].isin(service_filter)]

if status_filter:
    filtered_df = filtered_df[filtered_df["Status"].isin(status_filter)]

# === METRICS ===
st.markdown("---")
st.subheader("📈 Overview Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("✅ Active", (filtered_df["Status"] == "Active").sum())
col2.metric("⏳ Expiring Soon", (filtered_df["Status"] == "Expiring Soon").sum())
col3.metric("❌ Expired", (filtered_df["Status"] == "Expired").sum())

# === TABLE ===
st.markdown("---")
st.subheader("📋 Client Records")

st.dataframe(filtered_df, use_container_width=True)

# === FOOTER ===
st.markdown("---")
st.info("""
💡 Update data directly in Google Sheets  
🔄 Dashboard refreshes automatically  
📊 Share with stakeholders for live insights
""")
