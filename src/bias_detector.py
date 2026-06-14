"""
bias_detector.py - Detect potentially biased language in job descriptions.
Flags gendered, ageist, or exclusionary terms that may reduce applicant diversity.
"""

from typing import Dict, List

# Gendered word lists (based on Gaucher et al. 2011 research)
MASCULINE_CODED = [
    "competitive", "dominant", "challenge", "lead", "ninja", "rockstar",
    "aggressive", "fearless", "independent", "outspoken", "driven",
    "strong", "decisive", "headstrong", "analytical", "confident",
    "assertive", "determined", "ambitious", "self-reliant"
]

FEMININE_CODED = [
    "collaborative", "connect", "support", "together", "interpersonal",
    "nurture", "trust", "community", "share", "cooperate",
    "empathy", "warm", "sensitive", "committed", "loyal"
]

AGE_BIASED = [
    "young", "recent graduate", "digital native", "fresh", "energetic",
    "up-and-coming", "entry-level only", "years of experience" # flagged only if combined with high number
]

EXCLUSIONARY = [
    "culture fit", "work hard play hard", "fraternity", "brotherhood",
    "beer fridge", "ping pong", "nerf gun", "hustle culture",
    "native speaker", "fluent only"
]

OVERUSED_JARGON = [
    "synergy", "bandwidth", "pivot", "disruption", "10x", "rockstar",
    "wizard", "guru", "ninja", "evangelist", "thought leader", "deep dive"
]


def detect_bias(jd_text: str) -> Dict:
    """
    Scan job description for biased or exclusionary language.
    Returns flagged terms by category with recommendations.
    """
    jd_lower = jd_text.lower()

    results = {
        "masculine_coded": [],
        "feminine_coded": [],
        "age_biased": [],
        "exclusionary": [],
        "overused_jargon": [],
        "bias_score": 0,
        "flags": [],
        "recommendations": []
    }

    for word in MASCULINE_CODED:
        if word in jd_lower:
            results["masculine_coded"].append(word)

    for word in FEMININE_CODED:
        if word in jd_lower:
            results["feminine_coded"].append(word)

    for word in AGE_BIASED:
        if word in jd_lower:
            results["age_biased"].append(word)

    for word in EXCLUSIONARY:
        if word in jd_lower:
            results["exclusionary"].append(word)

    for word in OVERUSED_JARGON:
        if word in jd_lower:
            results["overused_jargon"].append(word)

    # Bias scoring
    score = 0
    masc_count = len(results["masculine_coded"])
    fem_count = len(results["feminine_coded"])

    if masc_count > 3:
        score += 2
        results["flags"].append(
            f"⚠️ Masculine-coded language detected ({masc_count} terms): "
            f"{', '.join(results['masculine_coded'][:4])}. "
            "May discourage female applicants."
        )

    if fem_count > 3:
        score += 1
        results["flags"].append(
            f"ℹ️ Feminine-coded language detected ({fem_count} terms). "
            "Generally lower impact but worth noting."
        )

    gender_imbalance = abs(masc_count - fem_count)
    if gender_imbalance > 4:
        score += 2
        results["flags"].append(
            f"⚠️ Strong gender imbalance: {masc_count} masculine vs {fem_count} feminine coded words."
        )

    if results["age_biased"]:
        score += 2
        results["flags"].append(
            f"⚠️ Potentially ageist terms: {', '.join(results['age_biased'])}. "
            "May discourage experienced candidates."
        )

    if results["exclusionary"]:
        score += 3
        results["flags"].append(
            f"🚩 Exclusionary language: {', '.join(results['exclusionary'])}. "
            "Can alienate diverse candidates."
        )

    if results["overused_jargon"]:
        score += 1
        results["flags"].append(
            f"📝 Overused buzzwords: {', '.join(results['overused_jargon'])}. "
            "Makes JD feel less professional."
        )

    results["bias_score"] = score
    results["bias_level"] = _get_bias_level(score)
    results["recommendations"] = _get_recommendations(results)

    return results


def _get_bias_level(score: int) -> str:
    if score == 0:
        return "🟢 Low Bias"
    elif score <= 3:
        return "🟡 Moderate Bias"
    elif score <= 6:
        return "🟠 High Bias"
    else:
        return "🔴 Very High Bias"


def _get_recommendations(results: Dict) -> List[str]:
    recs = []

    if results["masculine_coded"]:
        recs.append(
            "Replace masculine-coded words like 'competitive', 'dominant', 'aggressive' "
            "with neutral terms like 'motivated', 'results-oriented', 'proactive'."
        )

    if results["exclusionary"]:
        recs.append(
            "Remove 'culture fit' language — replace with 'values alignment' and describe "
            "specific values instead."
        )

    if results["age_biased"]:
        recs.append(
            "Avoid 'recent graduate' or 'digital native' — specify the actual skills needed instead."
        )

    if results["overused_jargon"]:
        recs.append(
            "Replace buzzwords (ninja, rockstar, guru) with specific, measurable job requirements."
        )

    if not recs:
        recs.append("✅ Job description uses inclusive, professional language. No major changes needed.")

    return recs
