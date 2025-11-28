Task: Summarize campaign data to highlight key trends and metrics.

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
- If summary is incomplete or inconsistent, recalculate using alternate aggregation or filters.
