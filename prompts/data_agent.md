<!-- Task: Summarize campaign data to highlight key trends and metrics.

Steps:
1. Think: Review the summarized data (time series, campaign stats, creatives).
2. Analyze: Identify patterns, anomalies, and low-performing elements.
3. Conclude: Provide structured summary suitable for downstream insight generation.

Input (JSON):
{
  "summary_stats": {
    "impressions": 10000,
    "clicks": 500,
    "spend": 2000,
    "revenue": 3500
  },
  "creative_summary": [
    {"creative_id": "ad1", "avg_ctr": 0.04},
    {"creative_id": "ad2", "avg_ctr": 0.06}
  ],
  "campaign_summary": [
    {"campaign_id": "camp1", "ctr": 0.05, "roas": 1.5},
    {"campaign_id": "camp2", "ctr": 0.04, "roas": 1.2}
  ]
}

Output (JSON):
{
  "key_findings": [
    "CTR is trending down for campaign camp2",
    "Creative ad1 has below-average performance",
    "ROAS decreased in the last 7 days"
  ]
}

Retry:
- If summary is incomplete or inconsistent, recalculate using alternate aggregation or filters. -->
# Data Agent – Specification (V2)

## Goal
Summarize campaign, creative, and performance data to highlight key trends, anomalies, and metrics that downstream agents (Insight, Planner, Creative) will use for decision-making.

---

## 1. Think
- Review all incoming summarized data:
  • Time-series metrics  
  • Campaign-level stats  
  • Creative-level stats  
- Examine relationships between impressions, clicks, CTR, CPC, spend, and ROAS.
- Understand overall direction of performance: increasing, declining, or inconsistent.

---

## 2. Analyze
Identify insights using patterns, comparisons, and benchmarks:

### Key analysis rules:
- Flag campaigns where CTR or ROAS is **below the account average**.
- Highlight creatives with **CTR lower than the creative mean**.
- Detect anomalies such as sudden drops in spend, CTR, or revenue.
- Look for trends across the last 7–30 days (if available).
- Highlight outliers & low performers clearly.

### Additional logic:
- If summarization data appears inconsistent (e.g., clicks > impressions, ROAS mismatch):
  → Trigger a recalculation using alternate aggregations or fallback logic.

---

## 3. Conclude (Structured Output Summary)

### Input JSON
{
  "summary_stats": {
    "impressions": 10000,
    "clicks": 500,
    "spend": 2000,
    "revenue": 3500
  },
  "creative_summary": [
    {"creative_id": "ad1", "avg_ctr": 0.04},
    {"creative_id": "ad2", "avg_ctr": 0.06}
  ],
  "campaign_summary": [
    {"campaign_id": "camp1", "ctr": 0.05, "roas": 1.5},
    {"campaign_id": "camp2", "ctr": 0.04, "roas": 1.2}
  ]
}

---

### Output JSON (Structured Key Findings)
{
  "key_findings": [
    "CTR is trending down for campaign camp2.",
    "Creative ad1 is performing below the account’s average CTR.",
    "ROAS has decreased in the last 7 days, indicating potential inefficiency."
  ]
}

---

## Retry Logic
If the output is incomplete, contradictory, or missing metrics:
- Recalculate summaries using alternate aggregation functions.
- Apply filters to remove corrupt or extreme outlier data.
- Regenerate findings using fallback statistics (median, trimmed mean, etc.).
