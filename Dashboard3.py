with tab2:
    st.header("Prompt Templates Usage")

    try:
        template_usage_df = fetch_template_usage_data(logger)
        user_visit_df = fetch_user_visit_data(logger)

        # Date selector for filtering user_visit_df
        st.subheader("Select Date Range for User Logs")
        min_date = user_visit_df["date"].min().date() if not user_visit_df.empty else datetime.today().date()
        max_date = user_visit_df["date"].max().date() if not user_visit_df.empty else datetime.today().date()
        start_date, end_date = st.date_input("Date Range", [min_date, max_date])

        if not user_visit_df.empty:
            user_visit_df = user_visit_df[
                (user_visit_df["date"].dt.date >= start_date) & (user_visit_df["date"].dt.date <= end_date)
            ]

        # Create two columns for the charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Template Usage")
            if not template_usage_df.empty:
                display_template_usage_bar_chart(template_usage_df)
                display_most_recent_template(template_usage_df)

                # Add total templates copied
                total_copies = template_usage_df["copy_count"].sum()
                st.metric("Total Templates Copied", total_copies)
            else:
                st.warning("No template usage data available.")

        with col2:
            st.subheader("User Analytics")
            if not user_visit_df.empty:
                display_user_visits_chart(user_visit_df)
                display_user_stats(user_visit_df)
            else:
                st.warning("No user visit data available.")

        # Display detailed tables
        st.subheader("Detailed Data")
        tab1, tab2 = st.tabs(["Template Usage Details", "User Visit Details"])

        with tab1:
            if not template_usage_df.empty:
                st.dataframe(template_usage_df, use_container_width=True)
            else:
                st.warning("No template usage data available.")

        with tab2:
            if not user_visit_df.empty:
                st.caption(f"Showing records from **{start_date.strftime('%Y-%m-%d')}** to **{end_date.strftime('%Y-%m-%d')}**")
                st.dataframe(user_visit_df, use_container_width=True)
            else:
                st.warning("No user visit data available.")

    except Exception as e:
        st.error(f"An error occurred while processing data: {e}")
        logger.error(f"An error occurred while processing data: {e}")
