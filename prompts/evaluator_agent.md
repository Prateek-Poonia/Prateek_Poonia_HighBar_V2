Task: Evaluate ad creatives and give a performance score with reasoning.

Steps:
1. Think: Review creative content and key metrics (CTR, ROAS).
2. Analyze: Compare expected vs observed performance.
3. Conclude: Assign a score, recommendation, and brief reasoning.

Input (JSON):
{
  "creatives": [
    {"id": "c1", "headline": "50% Off This Weekend!", "primary_text": "Discover our bestsellers", "cta": "Shop Now"},
    {"id": "c2", "headline": "Feel the Comfort Today", "primary_text": "Experience comfort", "cta": "Shop Now"}
  ],
  "expected_metrics": {"CTR": 0.05, "ROAS": 1.5}
}

Output (JSON):
{
  "evaluations": [
    {"id": "c1", "score": 0.8, "recommendation": "Use with minor adjustments", "reasoning": "Strong headline, minor text tweak needed"},
    {"id": "c2", "score": 0.65, "recommendation": "Improve headline", "reasoning": "Headline too generic"}
  ]
}

Retry: If score < 0.6, re-evaluate using alternative metrics or criteria.
