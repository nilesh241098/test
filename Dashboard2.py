import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.header("Prompt Templates Usage")

# Date range input
st.subheader("Select Date Range")
default_start = datetime.today() - timedelta(days=30)
default_end = datetime.today()

start_date, end_date = st.date_input(
    "Filter logs between:",
    value=(default_start, default_end),
    max_value=datetime.today()
)

try:
    template_usage_df = fetch_template_usage_data(logger)
    user_visit_df = fetch_user_visit_data(logger)

    # Handle timestamp parsing and filtering
    if not template_usage_df.empty:
        template_usage_df['last_copied'] = pd.to_datetime(template_usage_df['last_copied'], errors='coerce')

        start_datetime = pd.to_datetime(start_date)
        end_datetime = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

        filtered_df = template_usage_df[
            (template_usage_df['last_copied'] >= start_datetime) &
            (template_usage_df['last_copied'] <= end_datetime)
        ]
    else:
        filtered_df = pd.DataFrame()

    # Metric display
    st.metric("Total Templates Copied", int(filtered_df['copy_count'].sum() if 'copy_count' in filtered_df.columns else 0))

    # Split into two chart columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Template Usage")
        if not filtered_df.empty:
            display_template_usage_bar_chart(filtered_df)
            display_most_recent_template(filtered_df)
        else:
            st.warning("No template usage data available for selected range.")

    with col2:
        st.subheader("User Analytics")
        if not user_visit_df.empty:
            display_user_visits_chart(user_visit_df)
            display_user_stats(user_visit_df)
        else:
            st.warning("No user visit data available.")

    # Data Table Tabs
    st.subheader("Detailed Data")
    tab1, tab2 = st.tabs(["Template Usage Details", "User Visit Details"])

    with tab1:
        if not filtered_df.empty:
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.warning("No template usage data available.")

    with tab2:
        if not user_visit_df.empty:
            st.dataframe(user_visit_df, use_container_width=True)
        else:
            st.warning("No user visit data available.")

except Exception as e:
    st.error(f"Error loading data: {e}")
