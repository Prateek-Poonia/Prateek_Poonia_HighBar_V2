Task: Create a plan to analyze changes in marketing metrics.

Steps:
1. Think: Review summarized data and key metrics.
2. Analyze: Identify possible causes for metric changes.
3. Conclude: Recommend next steps for other agents.

Input (JSON):
{
  "summary_stats": {
    "impressions": 10000,
    "clicks": 500,
    "spend": 2000,
    "revenue": 3500
  },
  "metric": "ROAS",
  "time_period": "last_7_days"
}

Output (JSON):
{
  "plan": [
    "Check top-performing campaigns",
    "Generate hypotheses for metric drop",
    "Suggest creatives to test"
  ]
}

Retry: If plan seems incomplete, revisit data and refine steps.
