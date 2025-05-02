from datetime import timedelta, date

# --- User Visit Date Filter ---
st.subheader("Select Date Range for User Logs")

if not user_visit_df.empty:
    user_visit_df["date"] = pd.to_datetime(user_visit_df["date"])
    min_uv_date = user_visit_df["date"].min().date()
    max_uv_date = user_visit_df["date"].max().date()

    # Preset options
    date_option = st.selectbox("Quick Select", ["Custom", "Last Week", "Last Month"])

    today = date.today()

    if date_option == "Last Week":
        start_date = today - timedelta(days=7)
        end_date = today
    elif date_option == "Last Month":
        start_date = today - timedelta(days=30)
        end_date = today
    else:
        date_range = st.date_input("Date Range", [min_uv_date, max_uv_date])
        if len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date, end_date = None, None
            st.info("Please select both a start and end date to filter user logs.")

    if start_date and end_date:
        if start_date > end_date:
            st.warning("Start date must be before end date.")
        else:
            user_visit_df = user_visit_df[
                (user_visit_df["date"].dt.date >= start_date) & 
                (user_visit_df["date"].dt.date <= end_date)
            ]
