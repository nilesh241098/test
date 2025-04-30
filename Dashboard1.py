import streamlit as st
from datetime import datetime, timedelta

# Initial header
st.header("Prompt Templates Usage")

# Date range selector
st.subheader("Select Date Range")
default_start = datetime.today() - timedelta(days=30)
default_end = datetime.today()

start_date, end_date = st.date_input(
    "Filter logs between:",
    value=(default_start, default_end),
    max_value=datetime.today()
)

# Fetch data
try:
    template_usage_df = fetch_template_usage_data(logger)
    user_visit_df = fetch_user_visit_data(logger)

    # Convert date column to datetime if needed
    if not template_usage_df.empty and "timestamp" in template_usage_df.columns:
        template_usage_df["timestamp"] = pd.to_datetime(template_usage_df["timestamp"])
        template_usage_df = template_usage_df[
            (template_usage_df["timestamp"] >= pd.to_datetime(start_date)) &
            (template_usage_df["timestamp"] <= pd.to_datetime(end_date))
        ]

    # Display overall metric
    st.metric("Total Templates Copied", int(template_usage_df['copy_count'].sum() if 'copy_count' in template_usage_df.columns else 0))

    # Layout for charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Template Usage")
        if not template_usage_df.empty:
            display_template_usage_bar_chart(template_usage_df)
            display_most_recent_template(template_usage_df)
        else:
            st.warning("No template usage data available for selected range.")

    with col2:
        st.subheader("User Analytics")
        if not user_visit_df.empty:
            display_user_visits_chart(user_visit_df)
            display_user_stats(user_visit_df)
        else:
            st.warning("No user visit data available.")

    # Detailed Data Tabs
    st.subheader("Detailed Data")
    tab1, tab2 = st.tabs(["Template Usage Details", "User Visit Details"])

    with tab1:
        if not template_usage_df.empty:
            st.dataframe(template_usage_df, use_container_width=True)
        else:
            st.warning("No template usage data available.")

    with tab2:
        if not user_visit_df.empty:
            st.dataframe(user_visit_df, use_container_width=True)
        else:
            st.warning("No user visit data available.")

except Exception as e:
    st.error(f"Error loading data: {e}")
