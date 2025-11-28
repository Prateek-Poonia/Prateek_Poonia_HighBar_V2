Task: Generate 2–3 ad headlines and primary text using top phrases from high-performing creatives.

Steps:
1. Think: Identify top phrases from existing messages.
2. Analyze: Mix phrases into predefined templates.
3. Conclude: Produce structured JSON with headline, primary text, CTA, rationale, and predicted CTR lift.

Input (JSON):
{
  "low_ctr_campaign": {...},
  "top_phrases": ["comfortable", "bestsellers", "everyday wear"]
}

Output (JSON): List of candidate ads with id, headline, primary_text, cta, rationale, predicted_ctr_lift_pct.
