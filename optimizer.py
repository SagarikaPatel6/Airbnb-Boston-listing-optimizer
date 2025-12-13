"""
Optimization Engine: Airbnb Listing Strategy Optimizer (Boston)

This module formulates a prescriptive optimization problem where
Airbnb listings are treated as decision units (analogous to assets).

Objective:
    Minimize revenue risk for a given expected revenue target.

This mirrors classical portfolio optimization and is solved using
scipy.optimize (cloud-deployable, no license required).
"""

import numpy as np
from scipy.optimize import minimize
from typing import Tuple, Dict


def optimize_portfolio(
    expected_returns: np.ndarray,
    cov_matrix: np.ndarray,
    target_return: float,
    min_weight: float = 0.0,
    max_weight: float = 1.0
) -> Tuple[np.ndarray, Dict]:
    """
    Optimize Airbnb listing allocation.

    Decision Variables:
        w_i = allocation weight for listing i

    Objective:
        Minimize portfolio variance (revenue risk)

    Constraints:
        - Sum of weights = 1
        - Expected revenue >= target_return
        - min_weight <= w_i <= max_weight

    Args:
        expected_returns: Expected annual revenue per listing
        cov_matrix: Revenue covariance matrix
        target_return: Minimum expected revenue threshold
        min_weight: Minimum allocation weight per listing
        max_weight: Maximum allocation weight per listing

    Returns:
        (optimal_weights, result_dict)
    """

    n = len(expected_returns)

    # Objective: minimize revenue variance
    def portfolio_variance(weights):
        return weights @ cov_matrix @ weights

    # Constraint: fully allocated management capacity
    constraint_sum = {
        "type": "eq",
        "fun": lambda w: np.sum(w) - 1.0
    }

    # Constraint: minimum expected revenue
    constraint_return = {
        "type": "ineq",
        "fun": lambda w: w @ expected_returns - target_return
    }

    constraints = [constraint_sum, constraint_return]

    # Bounds: operational limits per listing
    bounds = [(min_weight, max_weight) for _ in range(n)]

    # Initial guess: equal allocation
    x0 = np.ones(n) / n

    result = minimize(
        portfolio_variance,
        x0,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"maxiter": 1000}
    )

    if result.success:
        portfolio_return = result.x @ expected_returns
        portfolio_risk = np.sqrt(result.x @ cov_matrix @ result.x)
    else:
        portfolio_return = None
        portfolio_risk = None

    result_dict = {
        "success": result.success,
        "message": result.message,
        "portfolio_return": portfolio_return,
        "portfolio_risk": portfolio_risk,
        "objective_value": result.fun
    }

    return result.x, result_dict


def generate_efficient_frontier(
    expected_returns: np.ndarray,
    cov_matrix: np.ndarray,
    n_points: int = 30,
    min_weight: float = 0.0,
    max_weight: float = 1.0
) -> list:
    """
    Generate the Revenue–Risk Efficient Frontier for Airbnb listings.
    """

    min_ret = expected_returns.min()
    max_ret = expected_returns.max()

    target_returns = np.linspace(min_ret, max_ret, n_points)

    frontier = []

    for tr in target_returns:
        weights, result = optimize_portfolio(
            expected_returns,
            cov_matrix,
            tr,
            min_weight,
            max_weight
        )

        if result["success"]:
            frontier.append({
                "return": result["portfolio_return"],
                "risk": result["portfolio_risk"],
                "weights": weights
            })

    return frontier


def find_minimum_variance_portfolio(
    expected_returns: np.ndarray,
    cov_matrix: np.ndarray,
    min_weight: float = 0.0,
    max_weight: float = 1.0
) -> Tuple[np.ndarray, Dict]:
    """
    Find the global minimum-risk Airbnb listing allocation
    (no revenue constraint).
    """

    n = len(expected_returns)

    def portfolio_variance(weights):
        return weights @ cov_matrix @ weights

    constraint_sum = {
        "type": "eq",
        "fun": lambda w: np.sum(w) - 1.0
    }

    bounds = [(min_weight, max_weight) for _ in range(n)]
    x0 = np.ones(n) / n

    result = minimize(
        portfolio_variance,
        x0,
        method="SLSQP",
        bounds=bounds,
        constraints=[constraint_sum],
        options={"maxiter": 1000}
    )

    if result.success:
        portfolio_return = result.x @ expected_returns
        portfolio_risk = np.sqrt(result.x @ cov_matrix @ result.x)
    else:
        portfolio_return = None
        portfolio_risk = None

    result_dict = {
        "success": result.success,
        "message": result.message,
        "portfolio_return": portfolio_return,
        "portfolio_risk": portfolio_risk,
        "objective_value": result.fun
    }

    return result.x, result_dict
