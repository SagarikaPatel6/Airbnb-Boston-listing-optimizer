"""
Streamlit App: Airbnb Listing Strategy Optimizer (Boston)

Demo-optimized version:
- Limits optimization universe for fast execution
- Caches heavy computations
- Disables expensive frontier by default

Purpose: Demonstrate prescriptive analytics clearly and reliably.
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
    generate_efficient_frontier
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
    **Prescriptive Analytics Demo**

    This application demonstrates how portfolio techniques
    can be applied to **Airbnb listing strategy in Boston** — helping hosts
    prioritize listings to maximize expected revenue while managing demand risk
    under limited operational capacity.
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
    help="Operational capacity constraint"
)

risk_tolerance = st.sidebar.slider(
    "Risk Tolerance",
    min_value=0.1,
    max_value=1.0,
    value=0.5,
    step=0.05,
    help="Higher values allow higher demand uncertainty"
)

show_frontier = st.sidebar.checkbox(
    "Show Revenue–Risk Frontier (slow)",
    value=False
)

optimize_button = st.sidebar.button(
    "🚀 Optimize Listing Strategy",
    type="primary"
)

# --------------------------------------------------
# LOAD DATA (CACHED)
# --------------------------------------------------
@st.cache_data
def load_data():
    return load_airbnb_data("data/listings.csv")

df = load_data()

# --------------------------------------------------
# DEMO MODE: LIMIT OPTIMIZATION SIZE
# --------------------------------------------------
MAX_LISTINGS_OPT = 100  # critical for speed

df["expected_revenue"] = df["price"] * (365 - df["availability_365"])

df_opt = (
    df.sort_values("expected_revenue", ascending=False)
      .head(MAX_LISTINGS_OPT)
      .reset_index(drop=True)
)

# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------
st.subheader("📄 Boston Airbnb Listings (Sample)")
st.dataframe(
    df_opt[
        ["neighbourhood", "room_type", "price", "availability_365"]
    ].head(20),
    use_container_width=True
)

# --------------------------------------------------
# CACHE HEAVY METRICS
# --------------------------------------------------
@st.cache_data
def compute_metrics(df):
    expected_returns = compute_expected_revenue(df)
    risk = compute_revenue_risk(df)
    cov_matrix = compute_covariance_matrix(expected_returns, risk)
    return expected_returns, risk, cov_matrix

# --------------------------------------------------
# RUN OPTIMIZATION
# --------------------------------------------------
if optimize_button:

    st.markdown("## 🚀 Optimization Results")
    st.success("Optimization complete. Recommended listings are shown below.")

    with st.spinner("Running optimization model..."):

        expected_returns, risk, cov_matrix = compute_metrics(df_opt)

        # Capacity constraint translated into allocation bounds
        min_weight = 0.0
        max_weight = 1.0 / max_listings

        # Risk-adjusted revenue target (percentile-based)
        target_return = np.percentile(
            expected_returns,
            int(risk_tolerance * 100)
        )

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
    # PORTFOLIO STATISTICS
    # --------------------------------------------------
    portfolio_stats = get_portfolio_statistics(
        weights,
        expected_returns,
        cov_matrix
    )

    st.subheader("📊 Optimization Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Expected Annual Revenue",
        f"${portfolio_stats['return']:,.0f}"
    )
    col2.metric(
        "Revenue Risk",
        f"{portfolio_stats['risk']:,.0f}"
    )
    col3.metric(
        "Active Listings",
        max_listings
    )

    # --------------------------------------------------
    # OPTIMIZED LISTINGS
    # --------------------------------------------------
    st.subheader("✅ Optimized Listing Recommendations")
    st.caption("Only listings with non-zero allocation selected by the optimizer are shown below.")

    results_df = df_opt.copy()

    # Convert weights to percentages for clarity
    results_df["Allocation %"] = (weights * 100).round(2)

    # Keep only selected listings
    results_df = (
        results_df[results_df["Allocation %"] > 0.01]
        .sort_values("Allocation %", ascending=False)
    )

    st.info(
        f"Out of {len(df_opt)} candidate listings, "
        f"{len(results_df)} were selected by the optimization model "
        f"under the current capacity constraint."
    )

    st.dataframe(
        results_df[
            [
                "neighbourhood",
                "room_type",
                "price",
                "availability_365",
                "Allocation %"
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
            ["neighbourhood", "room_type", "Risk Contribution"]
        ].sort_values(
            "Risk Contribution",
            ascending=False
        ),
        use_container_width=True
    )

    # --------------------------------------------------
    # OPTIONAL: EFFICIENT FRONTIER
    # --------------------------------------------------
    if show_frontier:

        st.subheader("📈 Revenue–Risk Efficient Frontier")

        frontier = generate_efficient_frontier(
            expected_returns,
            cov_matrix,
            n_points=20,
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
    "Boston Airbnb Dataset | SciPy Optimization | Demo Mode"
)
