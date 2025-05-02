date_range = st.date_input("Date Range", [min_uv_date, max_uv_date])

if len(date_range) == 2:
    start_date, end_date = date_range
    if start_date > end_date:
        st.warning("Start date must be before end date.")
    else:
        user_visit_df = user_visit_df[
            (user_visit_df["date"].dt.date >= start_date) &
            (user_visit_df["date"].dt.date <= end_date)
        ]
else:
    st.info("Please select both a start and end date to filter user logs.")
