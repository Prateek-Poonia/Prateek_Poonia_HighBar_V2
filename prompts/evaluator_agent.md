<!-- Task: Evaluate ad creatives and give a performance score with reasoning.

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

Retry: If score < 0.6, re-evaluate using alternative metrics or criteria. -->
# Evaluator Agent – Specification (V2)

## Goal
Score ad creatives against expected metrics and produce actionable recommendations with clear reasoning and retry logic. The evaluator should produce structured JSON suitable for downstream Creative/Planner agents and human reviewers.

---

## 1. Think
- Read creative content and its observed metrics (CTR, ROAS, conversions, etc.).
- Read expected/target metrics for the campaign (e.g., CTR_target, ROAS_target).
- Consider contextual signals: sample size, time window, and any recent changes (creative rotation, budget shift).

---

## 2. Analyze
Compare observed vs expected performance using a reproducible scoring function.

### Key analysis rules
- Use at least two dimensions: relative CTR performance and relative ROAS performance.
- Weight metrics: by default, CTR_weight = 0.6, ROAS_weight = 0.4 (configurable).
- Penalize low sample sizes (sample_size < config.min_sample_size) by reducing confidence.
- If observed metrics are missing or invalid, apply fallback logic (e.g., use median or mark as insufficient_data).
- If score < config.retry_threshold, attempt a re-evaluation using alternate criteria (engagement proxies, historical baseline).

### Scoring function (deterministic)
1. Compute relative performance for each metric:
   - perf_ctr = observed_ctr / expected_ctr  (cap at 2.0)
   - perf_roas = observed_roas / expected_roas (cap at 2.0)
2. Normalize to 0..1:
   - norm_ctr = min(1.0, perf_ctr)
   - norm_roas = min(1.0, perf_roas)
3. Weighted score:
   - raw_score = (norm_ctr * CTR_weight) + (norm_roas * ROAS_weight)
4. Adjust for sample size:
   - sample_factor = min(1.0, log1p(sample_size) / log1p(config.sample_size))
   - final_score = raw_score * sample_factor
5. Map to 0.0–1.0 (already in that range); round to 2 decimals.

### Categorization + recommendations
- score ≥ 0.8 → "Strong" — Recommend scale / A/B minor tests
- 0.6 ≤ score < 0.8 → "Moderate" — Recommend iterate (copy tweak, CTA change)
- 0.4 ≤ score < 0.6 → "Weak" — Recommend rewrite headline or test new angle
- score < 0.4 → "Poor" — Pause & redesign creative

---

## 3. Conclude (Structured Output)

### Input JSON (expected)
{
  "creatives": [
    {"id": "c1", "headline": "...", "primary_text": "...", "cta": "...", "metrics": {"ctr": 0.04, "roas": 1.2, "sample_size": 500}},
    ...
  ],
  "expected_metrics": {"CTR": 0.05, "ROAS": 1.5},
  "config": {
    "ctr_weight": 0.6,
    "roas_weight": 0.4,
    "sample_size": 1000,
    "retry_threshold": 0.6,
    "min_sample_size": 50
  }
}

### Output JSON (per creative)
{
  "evaluations": [
    {
      "id": "c1",
      "score": 0.80,
      "category": "Moderate",
      "recommendation": "Use with minor headline and primary_text tweaks; test CTA 'Buy Now'.",
      "reasoning": "CTR is 0.04 (80% of target); ROAS is 1.2 (80% of target); sample size 500 reduces confidence.",
      "evidence": {
        "observed": {"ctr": 0.04, "roas": 1.2, "sample_size": 500},
        "expected": {"ctr": 0.05, "roas": 1.5},
        "perf": {"ctr_perf": 0.8, "roas_perf": 0.8}
      },
      "rechecked": false
    },
    ...
  ]
}

---

## Retry behavior
- If final_score < config.retry_threshold (default 0.6):
  - Re-evaluate using alternate criteria:
    • Use historical baseline (last 28 days median) instead of expected_metrics if available.  
    • Or compute combined engagement proxy (clicks/impressions * conversions/spend) and rescore.  
  - Set `rechecked: true` and include `retry_reason` in output.
- If sample_size < min_sample_size:
  - Mark `insufficient_data: true` and lower `final_score` by 20% (or return `insufficient_data` flag instead of recommendation depending on config.fail_on_low_sample).

---

## Edge cases & error handling
- Missing expected_metrics → treat expected as median of campaign (if available); otherwise mark `cannot_evaluate`.
- Observed metric zero or NaN → treat as 0.0; include a warning in `reasoning`.
- Divide-by-zero protected by capping and fallback rules.
- All exceptions must be caught and surfaced as structured `error` entries in output JSON.

---

## Example (from the spec)
Input:
{
  "creatives": [
    {"id":"c1","headline":"50% Off This Weekend!","primary_text":"Discover our bestsellers","cta":"Shop Now","metrics":{"ctr":0.06,"roas":1.8,"sample_size":1200}},
    {"id":"c2","headline":"Feel the Comfort Today","primary_text":"Experience comfort","cta":"Shop Now","metrics":{"ctr":0.03,"roas":1.1,"sample_size":400}}
  ],
  "expected_metrics":{"CTR":0.05,"ROAS":1.5},
  "config":{"ctr_weight":0.6,"roas_weight":0.4,"sample_size":1000,"retry_threshold":0.6,"min_sample_size":50}
}

Expected Output:
{
  "evaluations":[
    {
      "id":"c1",
      "score":0.98,
      "category":"Strong",
      "recommendation":"Scale. Run A/B with minor copy variations.",
      "reasoning":"CTR & ROAS both exceed targets; large sample size supports confidence.",
      "evidence": {...},
      "rechecked": false
    },
    {
      "id":"c2",
      "score":0.43,
      "category":"Weak",
      "recommendation":"Rewrite headline and test new angle; consider 'social proof' creative.",
      "reasoning":"CTR below target (0.03 vs 0.05) and ROAS below target; sample size small; triggers retry.",
      "evidence": {...},
      "rechecked": true,
      "retry_reason": "Initial score < retry_threshold; re-evaluated using engagement proxy."
    }
  ]
}

---

## Implementation notes (for devs)
- Provide a deterministic function `score_creative(cre, expected, config)` returning the evaluation dict above.
- Log per-creative inputs, intermediate perf metrics, and final result to per-run evaluator logs.
- Make weights, thresholds, and sample_size configurable in the top-level config.yaml.
- Include unit tests for boundary cases (zero metrics, tiny sample sizes, missing expected metrics).

---

## Outputs must be strictly JSON-serializable (no custom objects).
