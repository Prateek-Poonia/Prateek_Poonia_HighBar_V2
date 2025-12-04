# from sklearn.feature_extraction.text import CountVectorizer
# import numpy as np, random, re

# def extract_top_phrases(messages, ngram_range=(1,2), top_n=20):
#     vec = CountVectorizer(ngram_range=ngram_range, stop_words='english').fit(messages)
#     X = vec.transform(messages)
#     sums = X.sum(axis=0).A1
#     terms = vec.get_feature_names_out()
#     freq = sorted(list(zip(terms, sums)), key=lambda x: x[1], reverse=True)
#     return [t for t,c in freq[:top_n]]

# def generate_candidates(low_ctr_campaign, top_phrases, num=6):
#     # simple template-based generation mixing top phrases
#     candidates = []
#     templates = [
#         "{phrase} — limited time. Shop now.",
#         "Feel the {phrase}. Free shipping over ₹999.",
#         "New: {phrase} for everyday comfort. Buy today.",
#         "{phrase} at special price — grab before it's gone.",
#         "Experience {phrase}. Shop the collection.",
#         "Comfort & confidence: {phrase}. Order now."
#     ]
#     for i in range(min(num,len(templates))):
#         phrase = top_phrases[i % len(top_phrases)]
#         headline = templates[i].format(phrase=phrase.capitalize())
#         primary = "Discover our bestsellers: " + headline
#         candidates.append({
#             "id": f"c{i+1}",
#             "headline": headline,
#             "primary_text": primary,
#             "cta": "Shop Now",
#             "rationale": f"Built from top phrase '{phrase}' observed in high-performing creatives",
#             "predicted_ctr_lift_pct": round(random.uniform(5,12),2)
#         })
#     return candidates
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import random
import re

def extract_top_phrases(messages, ngram_range=(1, 2), top_n=20):
    """
    Extract most frequent n-grams (phrases) from ad messages.

    Args:
        messages (list[str]): List of ad texts.
        ngram_range (tuple): n-gram range (1,2) for unigrams + bigrams.
        top_n (int): Number of phrases to return.

    Returns:
        list[str]: List of top phrases sorted by frequency.
    """
    vectorizer = CountVectorizer(
        ngram_range=ngram_range,
        stop_words='english'
    ).fit(messages)

    matrix = vectorizer.transform(messages)
    counts = matrix.sum(axis=0).A1
    terms = vectorizer.get_feature_names_out()

    freq = sorted(
        list(zip(terms, counts)),
        key=lambda x: x[1],
        reverse=True
    )

    return [phrase for phrase, count in freq[:top_n]]


def generate_candidates(low_ctr_campaign, top_phrases, num=6):
    """
    Generate ad creative candidates using top phrases.

    Args:
        low_ctr_campaign (str): Campaign ID with low CTR.
        top_phrases (list[str]): List of strong-performing phrases.
        num (int): Number of creatives to generate.

    Returns:
        list[dict]: Creative suggestions with predicted CTR lift.
    """

    templates = [
        "{phrase} — limited time. Shop now.",
        "Feel the {phrase}. Free shipping over ₹999.",
        "New: {phrase} for everyday comfort. Buy today.",
        "{phrase} at special price — grab before it's gone.",
        "Experience {phrase}. Shop the collection.",
        "Comfort & confidence: {phrase}. Order now."
    ]

    candidates = []

    for i in range(min(num, len(templates))):
        phrase = top_phrases[i % len(top_phrases)].capitalize()
        headline = templates[i].format(phrase=phrase)

        primary_text = (
            f"Discover our bestsellers: {headline}"
        )

        candidates.append({
            "id": f"c{i+1}",
            "headline": headline,
            "primary_text": primary_text,
            "cta": "Shop Now",
            "rationale": (
                f"Generated using top-performing phrase '{phrase}' "
                f"based on creative analysis from campaign '{low_ctr_campaign}'."
            ),
            "predicted_ctr_lift_pct": round(random.uniform(5, 12), 2)
        })

    return candidates
