<!-- Task: Generate 2–3 ad headlines and primary text using top phrases from high-performing creatives.

Steps:
1. Think: Identify top phrases from existing messages.
2. Analyze: Mix phrases into predefined templates.
3. Conclude: Produce structured JSON with headline, primary text, CTA, rationale, and predicted CTR lift.

Input (JSON):
{
  "low_ctr_campaign": {...},
  "top_phrases": ["comfortable", "bestsellers", "everyday wear"]
}

Output (JSON): List of candidate ads with id, headline, primary_text, cta, rationale, predicted_ctr_lift_pct. -->
# Creative Generator – Specification (V2)

## Goal
Generate 2–3 optimized ad creatives (headline + primary text) using insights from high-performing phrases to improve CTR in low-performing campaigns.

---

## 1. Think
- Identify top-performing phrases from the provided list.
- Classify phrases into categories:
  • Functional (comfort, durability)  
  • Emotional (confidence, feel-good)  
  • Social proof (bestseller, trending)  
- Understand the campaign context (e.g., low CTR) to guide messaging.
- Select 2–3 strongest phrases to use in new creatives.

---

## 2. Analyze
Use predefined templates to mix the selected phrases into new ad variations.

### Headline Templates
- "Experience {benefit} with our {product}"
- "Your new go-to for {use-case}"
- "Why everyone loves our {product}: {phrase}"
- "{phrase}: Upgrade Your Everyday Wear"

### Primary Text Templates
- "Discover our {product}, crafted for {benefit}. Perfect for {use-case}. {phrase}"
- "Loved by thousands — our {product} delivers {benefit}. Try it today."
- "Upgrade your everyday wear with {phrase}. Comfort meets style."

### Rules
- Combine 2–3 top phrases per creative.
- Keep tone consistent and benefit-focused.
- Headlines should be 12–15 words max.
- CTA must be one of: "Shop Now", "Learn More", "Buy Now".
- Produce strictly structured JSON output.

---

## 3. Conclude (Structured Output)

### Input JSON
{
  "low_ctr_campaign": { "campaign_id": "...", "ctr": 0.34, "spend": 1200 },
  "top_phrases": ["comfortable", "bestsellers", "everyday wear"]
}

---

## Output JSON (List of Generated Creatives)
Each creative object must include:
- id: unique creative identifier
- headline: generated ad headline
- primary_text: generated ad body
- cta: recommended call to action
- rationale: why this creative is expected to perform better
- predicted_ctr_lift_pct: estimated CTR improvement percentage

### Example Output
[
  {
    "id": "creative_01",
    "headline": "Your New Everyday Wear Bestseller",
    "primary_text": "Experience truly comfortable everyday wear. Our bestsellers are crafted to feel great all day.",
    "cta": "Shop Now",
    "rationale": "Uses top phrases (comfortable, everyday wear, bestsellers) and adds benefit-driven messaging to improve CTR.",
    "predicted_ctr_lift_pct": 14.2
  },
  {
    "id": "creative_02",
    "headline": "Comfort You Can Feel All Day",
    "primary_text": "Our comfortable and stylish bestsellers are designed for effortless everyday wear.",
    "cta": "Learn More",
    "rationale": "Focuses on emotional and functional benefits; uses two strongest performing phrases.",
    "predicted_ctr_lift_pct": 11.6
  }
]
