# Kasparro Agentic FB Analyst – Automated Ads Insights & Creative Generator

An agentic AI system that analyzes Facebook Ads performance, identifies why key metrics (ROAS, CTR, CPA) changed, and generates optimized creative recommendations automatically.

---

## Quick Start

# clone the repo
git clone https://github.com/<your-username>/kasparro-agentic-fb-analyst.git
cd kasparro-agentic-fb-analyst

# create a virtual env. and activate it
python -m venv venv
venv\Scripts\activate

# install dependecies
pip install -r requirements.txt

# run the code
python run.py "Why did ROAS fall last week?"


# Diagram
                ┌────────────────────┐
                │   User Query       │
                └─────────┬──────────┘
                          ▼
                ┌────────────────────┐
                │     Planner Agent  │
                └─────────┬──────────┘
                          ▼
        ┌──────────────────────────────────┐
        │   Data Agent → Loads + analyzes  │
        │   synthetic or real FB data      │
        └──────────────────────────────────┘
                          ▼
        ┌──────────────────────────────────┐
        │ Insight Agent → Generates        │
        │ hypotheses + metric diagnostics  │
        └──────────────────────────────────┘
                          ▼
        ┌──────────────────────────────────┐
        │ Evaluator Agent → Validates      │
        │ hypotheses with real data        │
        └──────────────────────────────────┘
                          ▼
        ┌──────────────────────────────────┐
        │ Creative Generator → Produces    │
        │ 6 optimized creatives per campaign│
        └──────────────────────────────────┘
                          ▼
                ┌────────────────────┐
                │  Final Report      │
                │ (reports/report.md)│
                └────────────────────┘


# Example output
# Automated Ads Analysis Report
Query: Why did ROAS fall last week?

## Summary
Top hypotheses and validation:
- Audience fatigue: conclusion=inconclusive confidence=0.0016297738170014953
- Platform / country shift: conclusion=inconclusive confidence=0.0

## Creative Recommendations
- Campaign MEN  Signture  Soft: 6 candidate creatives
- Campaign MEN BOL COLORS DROP: 6 candidate creatives
- Campaign MEN BOLD  OLORS DROP: 6 candidate creatives
- Campaign MEN BOLD COL RS DROP: 6 candidate creatives
- Campaign MEN PREMIUM MOD-L: 6 candidate creatives
- Campaign Me   Premium  Modal: 6 candidate creatives
- Campaign Men  Bold  Coors  Drop: 6 candidate creatives
- Campaign Men -|  Athleisure  Cooling: 6 candidate creatives
- Campaign Men B-ld Colors Drop: 6 candidate creatives
- Campaign Men BoldColors Drop: 6 candidate creatives
- Campaign Men Pr-mium Modal: 6 candidate creatives
- Campaign Men Premiu- Modal: 6 candidate creatives
- Campaign Men Premium -odal: 6 candidate creatives
- Campaign WOEN  Cotton  Classics: 6 candidate creatives
- Campaign WOEN FIT & LIFT: 6 candidate creatives
- Campaign WOMEN  Seamless  Everyday: 6 candidate creatives
- Campaign WOMEN Seamless Everydy: 6 candidate creatives
- Campaign WOMEN Semless Everyday: 6 candidate creatives
- Campaign WOMEN_Cot-on_Classics: 6 candidate creatives
- Campaign WOMN_Cotton_Classics: 6 candidate creatives
- Campaign Wmen | Studio Sports: 6 candidate creatives
- Campaign Wom-n Fit & Lift: 6 candidate creatives
- Campaign Women Seamless Eve yday: 6 candidate creatives
- Campaign Women-Studio S orts: 6 candidate creatives
- Campaign Women-Studio Spo-ts: 6 candidate creatives
- Campaign women su-mer invisible: 6 candidate creatives
- Campaign women | studio spo ts: 6 candidate creatives
