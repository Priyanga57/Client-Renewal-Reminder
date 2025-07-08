import streamlit as st
import pandas as pd
from config import GOOGLE_SHEET_CSV_URL
from renewal_checker import run_renewal_check  # ✅ Make sure this function exists

# 🎨 Page Setup
st.set_page_config(page_title="📊 Client Renewal Dashboard", layout="wide")

# 💾 Load Google Sheet
@st.cache_data(ttl=300)
def load_data():
    return pd.read_csv(GOOGLE_SHEET_CSV_URL)

df = load_data()
today = pd.to_datetime("today").date()

# 🧹 Clean
df["Status"] = df["Status"].fillna("Unknown")
df["Client Name"] = df["Client Name"].fillna("Unnamed Client")
df["Service Type"] = df["Service Type"].fillna("Unknown")
df["Renewal Due Date"] = pd.to_datetime(df["Renewal Due Date"], errors="coerce")

# 🎯 Sidebar Filters
st.sidebar.header("🔍 Filter Options")
statuses = sorted(df["Status"].dropna().unique())
services = sorted(df["Service Type"].dropna().unique())
clients = sorted(df["Client Name"].dropna().unique())

selected_status = st.sidebar.multiselect("📊 Status", statuses, default=statuses)
selected_service = st.sidebar.multiselect("💼 Service Type", services)
selected_client = st.sidebar.selectbox("👤 Select Client", ["All"] + clients)

# 🎛️ Filter Logic
filtered_df = df.copy()
if selected_status:
    filtered_df = filtered_df[filtered_df["Status"].isin(selected_status)]
if selected_service:
    filtered_df = filtered_df[filtered_df["Service Type"].isin(selected_service)]
if selected_client != "All":
    filtered_df = filtered_df[filtered_df["Client Name"] == selected_client]

# 📢 Header
st.title("📊 Client Renewal Dashboard")
st.caption(f"Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 📈 Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("✅ Active", df[df["Status"] == "Active"].shape[0])
col2.metric("⏳ Expiring Soon", df[df["Status"] == "Expiring Soon"].shape[0])
col3.metric("❌ Expired", df[df["Status"] == "Expired"].shape[0])
col4.metric("🔁 Transformed", df[df["Status"] == "Transform"].shape[0])

# ✉️ Email Trigger Button
with st.expander("✉️ Manual Email Trigger"):
    if st.button("📨 Run Renewal Checker and Send Emails"):
        result = run_renewal_check()
        st.success("✅ Emails sent and statuses updated!")
        st.text(result)

# 📄 Client-Specific View
if selected_client != "All":
    st.subheader(f"📄 Services for `{selected_client}`")
    st.dataframe(df[df["Client Name"] == selected_client], use_container_width=True)

# 📊 Client Progress Chart
st.markdown("### 📈 Client Status Distribution")
client_status_count = df.groupby(["Client Name", "Status"]).size().unstack(fill_value=0)
st.bar_chart(client_status_count)

# 🗓️ Renewal Heatmap Calendar
st.markdown("### 📅 Renewal Heatmap")
calendar_df = df[df["Renewal Due Date"].notna()]
calendar_df = calendar_df.groupby(calendar_df["Renewal Due Date"].dt.date).size().reset_index(name="Renewals")
calendar_df = calendar_df.sort_values("Renewal Due Date")

if not calendar_df.empty:
    import altair as alt
    calendar_chart = alt.Chart(calendar_df).mark_bar().encode(
        x=alt.X("Renewal Due Date:T", title="Date"),
        y=alt.Y("Renewals:Q", title="Renewals Count"),
        tooltip=["Renewal Due Date", "Renewals"]
    ).properties(width=800, height=300)
    st.altair_chart(calendar_chart, use_container_width=True)
else:
    st.info("No upcoming renewals found.")

# 📋 Filtered Table
st.markdown("---")
st.subheader("📋 Filtered Client Records")
st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

# ℹ️ Tips
with st.expander("💡 Tips & Usage"):
    st.markdown("""
    - ✅ Click on clients to view their services.
    - ✉️ Use the email button to manually run reminders.
    - 📅 Use the calendar chart to plan workload.
    - This updates live from your Google Sheet.
    """)

# 📌 Footer
st.markdown("---")
st.markdown("Made with ❤️ by Priyanga | Powered by Streamlit & Google Sheets")
