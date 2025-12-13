"""
Data Layer: Load Airbnb listings and compute revenue & risk metrics
(Boston Airbnb Dataset)
"""

"""
Data Layer: Load Airbnb listings and compute revenue & risk metrics
(Boston Airbnb Dataset)
"""

import pandas as pd
import numpy as np


def load_airbnb_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    # Required columns check
    required_cols = {"price", "availability_365"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in dataset: {missing}")

    # Price cleaning
    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    df = df.dropna(subset=["price", "availability_365"])

    return df


def compute_expected_revenue(df: pd.DataFrame) -> np.ndarray:
    """
    Expected annual revenue = price × occupied nights
    """
    occupied_nights = 365 - df["availability_365"]
    expected_revenue = df["price"] * occupied_nights
    return expected_revenue.values


def compute_revenue_risk(df: pd.DataFrame) -> np.ndarray:
    """
    Risk proxy:
    Higher availability = lower demand = higher revenue uncertainty
    """
    risk = df["availability_365"] / 365
    return risk.values


def compute_covariance_matrix(expected_revenue: np.ndarray,
                              risk: np.ndarray) -> np.ndarray:
    """
    Construct a diagonal covariance matrix using a scaled risk proxy
    for numerical stability.
    """
    # Normalize revenue to avoid extreme variances
    revenue_scaled = expected_revenue / np.mean(expected_revenue)
    variance = (revenue_scaled * risk) ** 2
    return np.diag(variance)


def get_portfolio_statistics(weights, expected_revenue, cov_matrix):
    portfolio_return = weights @ expected_revenue
    portfolio_variance = weights @ cov_matrix @ weights
    portfolio_risk = np.sqrt(portfolio_variance)

    return {
        "return": portfolio_return,
        "risk": portfolio_risk,
        "variance": portfolio_variance,
        "sharpe_ratio": portfolio_return / portfolio_risk if portfolio_risk > 0 else 0
    }


def compute_risk_contribution(weights, cov_matrix):
    portfolio_risk = np.sqrt(weights @ cov_matrix @ weights)
    marginal = cov_matrix @ weights

    if portfolio_risk > 0:
        return weights * marginal / portfolio_risk
    else:
        return np.zeros_like(weights)
