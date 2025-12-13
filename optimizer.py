"""
Optimization Engine: OPT Interview Portfolio Optimizer using Gurobi

This module consumes interview-related metrics from the data layer
and formulates a prescriptive optimization model to maximize
expected interviews under time and application constraints.

Requires Gurobi (academic license supported).
"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict

try:
    import gurobipy as gp
    from gurobipy import GRB
    GUROBI_AVAILABLE = True
except ImportError:
    GUROBI_AVAILABLE = False

# --- Data layer imports (analogous to expected_returns in stock optimizer) ---
from data.job_data_layer import (
    fetch_job_data,
    compute_base_interview_probability,
    compute_expected_interview_value
)


def optimize_opt_interview_plan(
    query: str = "data analyst",
    location: str = "United States",
    weekly_hours: float = 12.0,
    max_applications: int = 8,
    time_per_application: float = 1.0
) -> Tuple[pd.DataFrame, Dict]:
    """
    Optimize OPT job application strategy using Gurobi.

    Objective:
        Maximize expected interviews.

    Constraints:
        - Weekly time budget
        - Maximum number of applications

    Args:
        query: Job search keyword
        location: Job location
        weekly_hours: Weekly time available for applications
        max_applications: Maximum number of applications allowed
        time_per_application: Time cost per application (hours)

    Returns:
        (result_df, summary_dict)
    """

    if not GUROBI_AVAILABLE:
        raise ImportError("Gurobi is not installed. Install with: pip install gurobipy")

    # ======================================================
    # DATA LAYER (mirrors expected_returns computation)
    # ======================================================
    jobs_df = fetch_job_data(
        query=query,
        location=location,
        results=50
    )

    base_prob = compute_base_interview_probability(jobs_df)

    expected_value = compute_expected_interview_value(
        base_prob,
        jobs_df["salary_k"].values
    )

    n_jobs = len(jobs_df)

    # ======================================================
    # OPTIMIZATION MODEL
    # ======================================================
    model = gp.Model("OPT_Interview_Optimizer")
    model.setParam("OutputFlag", 0)

    # Decision variable: apply to job i or not
    apply = model.addVars(n_jobs, vtype=GRB.BINARY, name="apply")

    # Constraint 1: Maximum number of applications
    model.addConstr(
        gp.quicksum(apply[i] for i in range(n_jobs)) <= max_applications,
        name="max_applications"
    )

    # Constraint 2: Weekly time budget
    model.addConstr(
        gp.quicksum(time_per_application * apply[i] for i in range(n_jobs)) <= weekly_hours,
        name="weekly_time_budget"
    )

    # Objective: maximize expected interviews
    model.setObjective(
        gp.quicksum(expected_value[i] * apply[i] for i in range(n_jobs)),
        GRB.MAXIMIZE
    )

    # Solve
    model.optimize()

    # ======================================================
    # RESULTS
    # ======================================================
    selected = []
    total_expected_interviews = 0.0
    total_time_used = 0.0

    if model.status == GRB.OPTIMAL:
        for i in range(n_jobs):
            if apply[i].X > 0.5:
                selected.append({
                    "company": jobs_df.iloc[i]["company"],
                    "role": jobs_df.iloc[i]["role"],
                    "location": jobs_df.iloc[i]["location"],
                    "salary_k": jobs_df.iloc[i]["salary_k"],
                    "base_interview_prob": round(base_prob[i], 3),
                    "expected_interview_value": round(expected_value[i], 3),
                })

                total_expected_interviews += base_prob[i]
                total_time_used += time_per_application

    result_df = pd.DataFrame(selected).sort_values(
        by="expected_interview_value",
        ascending=False
    )

    summary = {
        "jobs_considered": n_jobs,
        "jobs_selected": len(result_df),
        "weekly_hours_budget": weekly_hours,
        "time_used_hours": round(total_time_used, 2),
        "expected_interviews": round(total_expected_interviews, 3),
    }

    return result_df, summary
