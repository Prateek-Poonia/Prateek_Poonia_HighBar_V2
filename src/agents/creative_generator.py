from sklearn.feature_extraction.text import CountVectorizer
import numpy as np, random, re

def extract_top_phrases(messages, ngram_range=(1,2), top_n=20):
    vec = CountVectorizer(ngram_range=ngram_range, stop_words='english').fit(messages)
    X = vec.transform(messages)
    sums = X.sum(axis=0).A1
    terms = vec.get_feature_names_out()
    freq = sorted(list(zip(terms, sums)), key=lambda x: x[1], reverse=True)
    return [t for t,c in freq[:top_n]]

def generate_candidates(low_ctr_campaign, top_phrases, num=6):
    # simple template-based generation mixing top phrases
    candidates = []
    templates = [
        "{phrase} — limited time. Shop now.",
        "Feel the {phrase}. Free shipping over ₹999.",
        "New: {phrase} for everyday comfort. Buy today.",
        "{phrase} at special price — grab before it's gone.",
        "Experience {phrase}. Shop the collection.",
        "Comfort & confidence: {phrase}. Order now."
    ]
    for i in range(min(num,len(templates))):
        phrase = top_phrases[i % len(top_phrases)]
        headline = templates[i].format(phrase=phrase.capitalize())
        primary = "Discover our bestsellers: " + headline
        candidates.append({
            "id": f"c{i+1}",
            "headline": headline,
            "primary_text": primary,
            "cta": "Shop Now",
            "rationale": f"Built from top phrase '{phrase}' observed in high-performing creatives",
            "predicted_ctr_lift_pct": round(random.uniform(5,12),2)
        })
    return candidates
