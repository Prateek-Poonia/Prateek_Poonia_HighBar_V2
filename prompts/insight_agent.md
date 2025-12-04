<!-- Task: Generate insights explaining why a marketing metric changed.

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

Retry: If insights seem incomplete, review data and regenerate key points. -->
# Insight Agent – Specification (V2)

## Goal
Explain why key marketing metrics (CTR, CPC, ROAS, CVR, CPM, Spend) changed by identifying causes, patterns, anomalies, and relationships in the summarized campaign + creative data. Output must be structured and insight-focused, not descriptive.

---

## 1. Think
- Review the full `data_summary`:
  • Account-level metrics (CTR, ROAS, CPC, CPM, Spend)
  • Week-over-week or day-over-day deltas
  • Creative performance rankings
  • Campaign-level and ad-set-level patterns
- Understand direction of change: Did the metric increase, decrease, or stay flat?
- Check whether changes correlate with changes in spend, impressions, budgets, or creative rotation.

---

## 2. Analyze
Identify core drivers behind metric shifts. The agent should examine:

### A. Performance Patterns
- Compare current values vs previous period values (baseline if provided).
- If CTR dropped:
  → Check engagement decline, new creatives added, or underperforming formats.
- If ROAS dropped:
  → Check CPC increase, CVR drop, or inefficient audience segments.

### B. Anomalies
Flag abnormalities:
- Sudden spikes or drops in impressions, clicks, spend, or revenue.
- Creatives with CTR or ROAS far below campaign average.
- Budget shifts or distribution anomalies.

### C. Causal Reasoning
Generate 2–3 crisp insights explaining:
- *What* changed  
- *Why* it changed  
- *Where* (which campaign/creative)  
- *Impact* (direction of effect)

Insights must be:
✓ Explanatory  
✓ Actionable  
✓ Quantitative when possible  
✓ Based on reasoning and patterns, not vague statements  

---

## 3. Conclude (Structured Output)

### Input JSON (expected)
{
  "data_summary": {
    "CTR": 0.05,
    "CTR_change": -0.02,
    "ROAS": 1.4,
    "ROAS_change": -0.10,
    "top_ads": ["AdSet1", "AdSet3"],
    "low_performing_ads": ["AdSet4"],
    "spend_change": 0.12,
    "cpc_change": 0.18,
    "creative_summary": [...],
    "campaign_summary": [...]
  }
}

### Output JSON (structured insights)
{
  "insights": [
    "CTR declined by 2% primarily due to lower engagement on carousel creatives and increased CPC (+18%).",
    "ROAS dropped by 10% because revenue did not scale with higher spend (+12%) and low-performing AdSet4 dragged down average returns.",
    "Top-performing creatives (AdSet1, AdSet3) continue to contribute most clicks, stabilizing overall CTR despite weak new creatives."
  ],
  "evidence": {
    "ctr_change": -0.02,
    "roas_change": -0.10,
    "spend_change": 0.12,
    "cpc_change": 0.18,
    "top_ads": ["AdSet1", "AdSet3"],
    "low_performing_ads": ["AdSet4"]
  }
}

---

## Retry Logic
If generated insights appear incomplete, vague, or repetitive:

- Re-run the analysis and extract:
  • baseline comparisons  
  • creative-level anomalies  
  • spend–performance mismatches  
  • audience/placement issues (if available)  

- Ensure at least:
  → 1 insight explaining *why the metric changed*  
  → 1 insight referencing *a specific campaign/ad group or creative*  
  → 1 insight referencing *data evidence (change %, creatives, etc.)*

Include:
"rechecked": true
and optionally:
"retry_reason": "Initial insights lacked causal clarity."

---

## Edge Cases & Error Handling
- Missing change metrics → compute inferred change from past period if provided.
- Missing baseline → output insights but add `baseline_missing: true`.
- NaN or zero metrics → treat as anomalies and flag in insights.
- Data_summary incomplete → return `"insufficient_data": true` with minimal insights.

---

## Output must be strictly JSON-serializable.
