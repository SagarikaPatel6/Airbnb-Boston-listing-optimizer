# OPT-Interview-Maximizer
A Gurobi-based prescriptive analytics tool that optimizes OPT job application strategy to maximize interview likelihood under time constraints.

## 🎯 The Problem

OPT students face a uniquely constrained job search environment. In addition to competitive hiring markets, they operate under strict time limits, visa-related uncertainty, and limited weekly capacity to apply, customize resumes, and conduct outreach.

Most job seekers rely on intuition when deciding where to apply and how much effort to invest in each opportunity. This often leads to inefficient strategies — over-applying with low effort, under-investing in high-potential roles, or exhausting time on companies that are not OPT-friendly.

Despite the importance of these tradeoffs, job application strategy is rarely treated as a structured decision problem. This project addresses that gap by framing the OPT job search as a **portfolio optimization problem**, where limited time must be allocated across competing opportunities to maximize expected interviews.

## 💡 The Solution

The OPT Interview Maximizer reframes job searching as a **prescriptive optimization problem** inspired by classical portfolio construction.

Each job posting is treated as an asset with:
- an estimated probability of securing an interview,
- an expected value proxy (role fit and salary),
- and a time cost required to apply and perform follow-up actions.

Using a mixed-integer optimization model built in **Gurobi**, the system selects:
- which jobs to apply to,
- which applications deserve extra effort (resume tailoring, referrals, follow-ups),
- and how to allocate weekly time across these actions,

in order to **maximize expected interviews** while respecting real-world constraints such as time availability, application limits, and OPT-friendly employer requirements.


## 🚀 Live Demo

**[Try it here →](YOUR_STREAMLIT_URL)**

![Screenshot of the OPT Interview Maximizer app](screenshot.png)

## ⚙️ How It Works

1. **User defines constraints**  
   The user specifies weekly hours available, maximum applications, and OPT-friendly requirements.

2. **System evaluates job opportunities**  
   Each job is scored using estimated interview probability, match quality, salary proxy, and effort cost.

3. **Optimization engine runs**  
   A Gurobi-based mixed-integer program selects the optimal combination of job applications and effort actions.

4. **Actionable plan is returned**  
   The user receives a clear weekly application plan, including which jobs to apply to and where to invest additional effort.

### The Analytics Behind It

- **Data**
  - Curated job posting dataset (CSV)
  - Estimated interview probabilities
  - Effort action costs and probability uplifts

- **Decision Variables**
  - Apply or not apply to each job
  - Whether to tailor, seek referrals, or follow up

- **Objective Function**
  - Maximize expected interviews (with optional value and risk adjustments)

- **Constraints**
  - Weekly time budget
  - Maximum number of applications
  - OPT-friendly employer minimum
  - Logical dependencies between actions

## 📊 Example Output

The output includes:
- a prioritized list of recommended job applications,
- the specific actions to take for each role,
- estimated interview probabilities,
- total time usage vs budget.

This allows users to understand not just *what* to do, but *why* certain tradeoffs were made.

## 🛠️ Technology Stack

- **Frontend:** Streamlit  
- **Optimization:** Gurobi (Mixed-Integer Programming)  
- **Data Processing:** Pandas, NumPy  
- **Data:** Curated CSV datasets (jobs and actions)

## 🎓 About This Project

Built as a final project for **ISOM 839 – Prescriptive Analytics**  
at **Suffolk University**.

**Author:** Sagarika Patel  
**LinkedIn:** https://www.linkedin.com/in/sagarikapatel6/  

## 🔮 Future Possibilities

Potential extensions include:
- learning interview probabilities from historical outcomes,
- multi-week planning horizons,
- dynamic updates as deadlines approach,
- integration with job boards or LinkedIn APIs,
- personalization based on resume versions.

This project demonstrates how prescriptive analytics can guide high-stakes personal decisions under constraints.



