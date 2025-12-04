<!-- Task: Create a plan to analyze changes in marketing metrics.

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

Retry: If plan seems incomplete, revisit data and refine steps. -->
# Planner Agent – Specification (V2)

## Goal
Create a structured, actionable plan for analyzing changes in key marketing metrics (CTR, CPC, CPM, ROAS, CVR, Spend, etc.) and outline next steps for downstream agents such as Insight Agent, Evaluator Agent, and Creative Generator.

The planner should act as a high-level strategist.

---

## 1. Think
- Read the full `summary_stats` object.
- Understand which metric (CTR, ROAS, etc.) the user wants to analyze.
- Identify the time period (e.g., last_7_days, last_30_days).
- Evaluate whether the data is sufficient for analysis (impressions, clicks, revenue, spend).

---

## 2. Analyze
Based on the provided metric:

### If the metric decreased:
- Identify potential causes (e.g., CTR drop → weak creatives, CPC increase; ROAS drop → revenue down or spend inefficient).
- Look at related metrics:  
  • ROAS → check revenue, spend, CVR  
  • CTR → check impressions, engagement, creative performance  
  • CPC/CPM → check spend and bids  
- Identify which campaigns/creatives might contribute to the issue (if provided: top_ads, low_performing_ads, creative_summary, etc.).

### If the metric increased:
- Identify which improvements likely drove the increase.
- Suggest scaling opportunities.

### General planning logic:
- Identify which downstream agents should work next:  
  • **Insight Agent** → to explain causes  
  • **Evaluator Agent** → to diagnose creative-level issues  
  • **Creative Generator** → to create new ad variations  
  • **Data Agent** → to refine or resummarize data  

---

## 3. Conclude (Structured Output)

### Input (expected)
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

### Output (structured plan)
{
  "plan": [
    "Analyze ROAS components: check whether spend increased faster than revenue.",
    "Review top-performing and low-performing campaigns to identify which drove the ROAS change.",
    "Generate hypotheses explaining possible ROAS drop for the Insight Agent.",
    "Flag creatives with low CTR or weak conversion patterns for the Evaluator Agent.",
    "Identify 2–3 creatives or angles for the Creative Generator to test.",
    "Prepare refined summary for deeper analysis if data appears incomplete."
  ],
  "next_agents": ["InsightAgent", "EvaluatorAgent", "CreativeGenerator"]
}

---

## Retry Logic
If the produced plan is:

- too short  
- missing causal steps  
- missing agent handoff steps  
- missing analysis steps  

Then re-run and regenerate a more detailed plan.

Set:
"rechecked": true  
"retry_reason": "Initial plan lacked sufficient strategic steps."

---

## Edge Cases & Error Handling
- If required summary fields are missing → output `"insufficient_data": true` with a minimal plan.
- If metric is not recognized (not CTR/ROAS/CPC/CPM/CVR/etc.) → output an `"unsupported_metric"` error.
- If values are zero or NaN → flag `"anomalies_detected"` and recommend resummarizing data.

---

## All outputs must be JSON-serializable.
