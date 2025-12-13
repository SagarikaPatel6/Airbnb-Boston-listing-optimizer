"""
Streamlit App: Airbnb Listing Strategy Optimizer (Boston)

This app serves as the orchestration layer.
It loads Airbnb listing data, runs a prescriptive optimization model,
and recommends which listings to prioritize to maximize revenue
under operational capacity constraints.
"""

import streamlit as st
import pandas as pd
import numpy as np

from data import (
    load_airbnb_data,
    compute_expected_revenue,
    compute_revenue_risk,
    compute_covariance_matrix,
    get_portfolio_statistics,
    compute_risk_contribution
)

from optimizer_scipy import (
    optimize_portfolio,
    generate_efficient_frontier,
    find_minimum_variance_portfolio
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Airbnb Listing Strategy Optimizer (Boston)",
    page_icon="🏡",
    layout="wide"
)

# --------------------------------------------------
# APP HEADER
# --------------------------------------------------
st.title("🏡 Airbnb Listing Strategy Optimizer")
st.markdown(
    """
    **Prescriptive Analytics in Action**

    This application helps Airbnb hosts and small property managers in **Boston**
    decide **which listings to prioritize** in order to maximize expected annual revenue
    while managing demand uncertainty under limited operational capacity.
    """
)

# --------------------------------------------------
# SIDEBAR INPUTS
# --------------------------------------------------
st.sidebar.header("⚙️ Optimization Settings")

max_listings = st.sidebar.slider(
    "Maximum Active Listings",
    min_value=1,
    max_value=20,
    value=5,
    step=1,
    help="Operational capacity: how many listings can be actively managed"
)

risk_tolerance = st.sidebar.slider(
    "Risk Tolerance",
    min_value=0.1,
    max_value=1.0,
    value=0.5,
    step=0.05,
    help="Higher values allow more demand uncertainty for higher revenue"
)

optimize_button = st.sidebar.button("🚀 Optimize Listing Strategy", type="primary")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    return load_airbnb_data("data/listings.csv")

df = load_data()

# --------------------------------------------------
# SHOW RAW DATA PREVIEW
# --------------------------------------------------
st.subheader("📄 Boston Airbnb Listings (Sample)")
st.dataframe(
    df[['neighbourhood', 'room_type', 'price', 'availability_365']].head(20),
    use_container_width=True
)

# --------------------------------------------------
# RUN OPTIMIZATION
# --------------------------------------------------
if optimize_button:

    with st.spinner("Running optimization model..."):

        # Expected revenue (acts like expected returns)
        expected_returns = compute_expected_revenue(df)

        # Risk proxy
        risk = compute_revenue_risk(df)

        # Covariance matrix
        cov_matrix = compute_covariance_matrix(expected_returns, risk)

        # Capacity constraint → limits number of active listings
        min_weight = 0.0
        max_weight = 1.0 / max_listings

        # Target return = risk-adjusted revenue expectation
        target_return = np.percentile(expected_returns, int(risk_tolerance * 100))

        weights, result = optimize_portfolio(
            expected_returns,
            cov_matrix,
            target_return,
            min_weight,
            max_weight
        )

    if not result["success"]:
        st.error("Optimization failed. Try adjusting constraints.")
        st.stop()

    # --------------------------------------------------
    # PORTFOLIO STATS
    # --------------------------------------------------
    portfolio_stats = get_portfolio_statistics(
        weights,
        expected_returns,
        cov_matrix
    )

    st.subheader("📊 Optimization Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Expected Annual Revenue", f"${portfolio_stats['return']:,.0f}")
    col2.metric("Revenue Risk", f"{portfolio_stats['risk']:,.0f}")
    col3.metric("Active Listings", max_listings)

    # --------------------------------------------------
    # RECOMMENDED LISTINGS
    # --------------------------------------------------
    st.subheader("✅ Recommended Listings to Prioritize")

    results_df = df.copy()
    results_df["Allocation Weight"] = weights
    results_df = results_df[results_df["Allocation Weight"] > 0.001]
    results_df = results_df.sort_values("Allocation Weight", ascending=False)

    st.dataframe(
        results_df[
            [
                "neighbourhood",
                "room_type",
                "price",
                "availability_365",
                "Allocation Weight"
            ]
        ],
        use_container_width=True
    )

    # --------------------------------------------------
    # RISK CONTRIBUTION
    # --------------------------------------------------
    st.subheader("⚠️ Revenue Risk Contribution by Listing")

    risk_contrib = compute_risk_contribution(weights, cov_matrix)

    risk_df = results_df.copy()
    risk_df["Risk Contribution"] = risk_contrib[results_df.index]

    st.dataframe(
        risk_df[
            [
                "neighbourhood",
                "room_type",
                "Risk Contribution"
            ]
        ].sort_values("Risk Contribution", ascending=False),
        use_container_width=True
    )

    # --------------------------------------------------
    # EFFICIENT FRONTIER
    # --------------------------------------------------
    st.subheader("📈 Revenue–Risk Efficient Frontier")

    frontier = generate_efficient_frontier(
        expected_returns,
        cov_matrix,
        n_points=30,
        min_weight=min_weight,
        max_weight=max_weight
    )

    if frontier:
        frontier_df = pd.DataFrame(frontier)

        st.line_chart(
            frontier_df.set_index("risk")["return"],
            height=400
        )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")
st.caption(
    "Built for ISOM 839 – Prescriptive Analytics | "
    "Boston Airbnb Dataset | SciPy Optimization"
)
