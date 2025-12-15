# 🏡 Airbnb Listing Strategy Optimizer (Boston)

A **prescriptive analytics application** that applies portfolio optimization techniques to help Airbnb hosts in Boston prioritize listings that **maximize expected revenue** while managing **demand risk and operational capacity constraints**.

---

## 🎯 The Problem

Airbnb hosts and small property managers operate under **limited capacity** — constrained by time, cleaning logistics, and management bandwidth. In competitive urban markets like Boston, listings vary widely in demand patterns, revenue potential, and uncertainty across neighborhoods, room types, and pricing levels.

In practice, hosts rely heavily on intuition when deciding:
- which listings to actively prioritize,
- how many listings to manage at once,
- and where to focus pricing and operational effort.

This often leads to inefficient strategies such as spreading effort too thin, prioritizing low-demand listings, or under-investing in high-revenue opportunities.

Despite these tradeoffs, listing prioritization is rarely treated as a structured decision problem. This project addresses that gap by framing Airbnb listing strategy as a **portfolio optimization problem**, where limited management capacity must be optimally allocated across competing listings.

---

## 💡 The Solution

The **Airbnb Listing Strategy Optimizer** reframes hosting decisions as a **prescriptive optimization problem**, inspired by classical portfolio construction.

Each Airbnb listing is treated as a decision unit with:
- an estimated **expected annual revenue**,
- a **demand uncertainty proxy** (risk),
- and an implicit operational cost represented through allocation constraints.

Using a constrained optimization framework, the model determines:
- which listings should be prioritized,
- how much relative focus to allocate to each listing,
- and how to balance revenue potential against demand uncertainty,

in order to **maximize expected revenue** while respecting real-world operational limits such as the maximum number of active listings a host can manage.

---

## 🚀 Live Demo

👉 **Try the app here:**  
(https://airbnb-boston-listing-optimizer-kprejpxwjbnanrn3qzj3az.streamlit.app/)

*(Deployed on Streamlit Cloud)*

** _Loom Video **_
(https://www.loom.com/share/dd4155834df9466bbd41552e3e07ef58)
---

## ⚙️ How It Works

1. **Load Airbnb market data**  
   The application loads a curated Boston Airbnb listings dataset (CSV) containing pricing, availability, and listing attributes.

2. **Feature engineering**  
   - Expected annual revenue is estimated using nightly price and availability.
   - Demand risk is approximated using availability-based uncertainty.
   - A covariance matrix is constructed to represent revenue volatility.

3. **Optimization engine runs**  
   A constrained optimization model selects the optimal allocation across listings, minimizing risk for a given revenue target while respecting capacity constraints.

4. **Actionable recommendations are returned**  
   The user receives:
   - a ranked list of recommended listings,
   - portfolio-level revenue and risk metrics,
   - and visual trade-offs between expected revenue and uncertainty.

---

## 🔍 The Analytics Behind It

- **Data**
  - Boston Airbnb listings dataset (CSV)
  - Pricing, availability, and listing metadata

- **Decision Variables**
  - Allocation weight for each listing (management focus)

- **Objective Function**
  - Maximize expected annual revenue while minimizing demand risk

- **Constraints**
  - Fully allocated management capacity  
  - Maximum number of active listings  
  - Non-negative allocation weights  

- **Optimization Technique**
  - Quadratic optimization using `scipy.optimize` (SLSQP solver)

---

## 📊 Example Output

The application produces:
- a table of **recommended listings** ranked by allocation weight,
- expected annual revenue and revenue risk metrics,
- risk contribution analysis by listing,
- an optional **Revenue–Risk Efficient Frontier** illustrating optimal trade-offs.

This allows hosts and managers to understand not just *which* listings to prioritize, but *why* those trade-offs are optimal given their constraints.

---

## 🛠️ Technology Stack

- **Frontend:** Streamlit  
- **Optimization:** SciPy (`scipy.optimize`)  
- **Data Processing:** Pandas, NumPy  
- **Visualization:** Plotly  
- **Data Source:** Static Airbnb CSV dataset (Boston)

---

## 🎓 About This Project

Built as a final project for  
**ISOM 839 – Prescriptive Analytics**  
at **Suffolk University**.

**Author:** Sagarika Patel  
**LinkedIn:** https://www.linkedin.com/in/sagarikapatel6/

---

## 🔮 Future Possibilities

Potential extensions include:
- neighborhood-level demand forecasting,
- seasonality-adjusted revenue estimation,
- multi-period optimization across months,
- dynamic pricing integration,
- scenario analysis for regulatory or market changes.

This project demonstrates how **prescriptive analytics** can be applied beyond finance to guide real-world operational decisions in platform-based marketplaces.
