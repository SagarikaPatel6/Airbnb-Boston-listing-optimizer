"""
Streamlit App: OPT Interview Maximizer

This app serves as the orchestration layer.
It collects user inputs, calls the optimization engine,
and displays optimized job application recommendations.
"""

import streamlit as st
import pandas as pd

from optimizer import optimize_opt_interview_plan

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="OPT Interview Maximizer",
    layout="wide"
)

# --------------------------------------------------
# APP HEADER
# --------------------------------------------------
st.title("🎯 OPT Interview Maximizer")
st.markdown(
    """
    A prescriptive analytics tool that helps OPT students
    allocate job application effort to **maximize interview chances**
    under time and application constraints.
    """
)

# --------------------------------------------------
# SIDEBAR INPUTS
# --------------------------------------------------
st.sidebar.header("🔧 Optimization Settings")

query = st.sidebar.text_input(
    "Job role keyword",
    value="data analyst"
)

location = st.sidebar.text_input(
    "Location",
    value="United States"
)

weekly_hours = st.sidebar.slider(
    "Weekly time available (hours)",
    min_value=5.0,
    max_value=40.0,
    value=12.0,
    step=1.0
)

max_applications = st.sidebar.slider(
    "Maximum applications per week",
    min_value=1,
    max_value=20,
    value=8,
    step=1
)

time_per_application = st.sidebar.slider(
    "Time per application (hours)",
    min_value=0.5,
    max_value=3.0,
    value=1.0,
    step=0.25
)

# --------------------------------------------------
# RUN OPTIMIZATION
# --------------------------------------------------
if st.button("🚀 Optimize My Applications"):

    with st.spinner("Fetching jobs and optimizing..."):

        results_df, summary = optimize_opt_interview_plan(
            query=query,
            location=location,
            weekly_hours=weekly_hours,
            max_applications=max_applications,
            time_per_application=time_per_application
        )

    # --------------------------------------------------
    # RESULTS SUMMARY
    # --------------------------------------------------
    st.subheader("📊 Optimization Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Jobs Considered", summary["jobs_considered"])
    col2.metric("Jobs Selected", summary["jobs_selected"])
    col3.metric("Time Used (hrs)", summary["time_used_hours"])
    col4.metric("Expected Interviews", summary["expected_interviews"])

    # --------------------------------------------------
    # RESULTS TABLE
    # --------------------------------------------------
    st.subheader("✅ Recommended Applications")

    if results_df.empty:
        st.warning("No jobs selected. Try adjusting constraints.")
    else:
        st.dataframe(
            results_df,
            use_container_width=True
        )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")
st.caption(
    "Built for ISOM 839 – Prescriptive Analytics | "
    "Uses real job market data and Gurobi optimization"
)

