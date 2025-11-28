Task: Generate insights explaining why a marketing metric changed.

Steps:
1. Think: Review summarized campaign and creative data.
2. Analyze: Identify patterns, anomalies, or causes for changes.
3. Conclude: Provide 2–3 key insights in structured JSON.

Input (JSON):
{
  "data_summary": {
    "CTR": 0.05,
    "ROAS_change": -0.1,
    "top_ads": ["AdSet1", "AdSet3"]
  }
}

Output (JSON):
{
  "insights": [
    "CTR dropped due to low engagement on carousel ads",
    "ROAS decreased last week",
    "Top-performing creatives remain consistent"
  ]
}

Retry: If insights seem incomplete, review data and regenerate key points.
