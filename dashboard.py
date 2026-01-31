import streamlit as st
import pandas as pd

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="📊 Client Renewal Dashboard",
    layout="wide"
)

# ================= LOAD DATA =================
SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "17_HyRiUA3UMSt6uOOS_vTa29YbeCIuSCbP6XjsuUdg8"
    "/export?format=csv"
)

@st.cache_data(show_spinner=False)
def load_data(url):
    return pd.read_csv(url)

try:
    df = load_data(SHEET_URL)
except Exception as e:
    st.error("❌ Failed to load Google Sheet")
    st.write(e)
    st.stop()

# ================= VALIDATION =================
REQUIRED_COLUMNS = ["Service Type", "Status"]
missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]

if missing_cols:
    st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
    st.stop()

# ================= STYLING =================
st.markdown("""
<style>
.block-container {
    padding: 2rem;
    background-color: #1f2633;
    border-radius: 14px;
}
.stMetricValue {
    font-size: 30px !important;
}
.stMetricLabel {
    color: #aab2bd;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.title("🎯 Client Renewal Management Dashboard")
st.markdown("📌 **Live tracking of onboarding, renewals, and AMC status**")

# ================= FILTERS =================
st.sidebar.header("🔍 Filter Options")

service_filter = st.sidebar.multiselect(
    "💼 Service Type",
    options=sorted(df["Service Type"].dropna().unique())
)

status_filter = st.sidebar.multiselect(
    "📊 Status",
    options=sorted(df["Status"].dropna().unique())
)

filtered_df = df.copy()

if service_filter:
    filtered_df = filtered_df[filtered_df["Service Type"].isin(service_filter)]

if status_filter:
    filtered_df = filtered_df[filtered_df["Status"].isin(status_filter)]

# ================= METRICS =================
st.markdown("---")
st.subheader("📈 Overview Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("✅ Active", (filtered_df["Status"] == "Active").sum())
col2.metric("⏳ Expiring Soon", (filtered_df["Status"] == "Expiring Soon").sum())
col3.metric("❌ Expired", (filtered_df["Status"] == "Expired").sum())

# ================= TABLE =================
st.markdown("---")
st.subheader("📋 Client Records")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# ================= FOOTER =================
st.markdown("---")
st.info("""
💡 **Usage Tips**
- Update records directly in the Google Sheet  
- Dashboard refreshes automatically  
- Use filters for quick insights  
- Share this dashboard with stakeholders  
""")
