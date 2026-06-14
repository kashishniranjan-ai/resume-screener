"""
explainer.py - Skill gap analysis and explainability layer
Compares resume skills vs JD requirements semantically (not just keyword matching).
"""

import re
import numpy as np
from typing import List, Dict, Tuple
from src.embedder import embed_text, cosine_similarity

# --- Common skill taxonomy (expandable) ---
SKILL_CATEGORIES = {
    "Programming Languages": [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust",
        "Ruby", "Swift", "Kotlin", "PHP", "Scala", "R", "MATLAB"
    ],
    "ML / AI": [
        "machine learning", "deep learning", "neural network", "NLP", "computer vision",
        "PyTorch", "TensorFlow", "Keras", "scikit-learn", "transformers", "BERT",
        "GPT", "LLM", "reinforcement learning", "XGBoost", "LightGBM", "pandas", "numpy"
    ],
    "Web & Backend": [
        "React", "Angular", "Vue", "Node.js", "Django", "Flask", "FastAPI",
        "Spring Boot", "REST API", "GraphQL", "HTML", "CSS", "Next.js"
    ],
    "Cloud & DevOps": [
        "AWS", "GCP", "Azure", "Docker", "Kubernetes", "CI/CD", "Terraform",
        "Jenkins", "GitHub Actions", "Linux", "Bash", "Ansible"
    ],
    "Databases": [
        "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
        "DynamoDB", "Cassandra", "SQLite", "Oracle"
    ],
    "Data Engineering": [
        "Spark", "Hadoop", "Kafka", "Airflow", "ETL", "data pipeline",
        "dbt", "Snowflake", "BigQuery", "Databricks"
    ],
    "Soft Skills": [
        "leadership", "communication", "teamwork", "problem solving",
        "agile", "scrum", "project management", "mentoring"
    ]
}


def extract_skills_from_text(text: str) -> List[str]:
    """Extract skill mentions from text using keyword matching."""
    text_lower = text.lower()
    found = []
    for category, skills in SKILL_CATEGORIES.items():
        for skill in skills:
            if skill.lower() in text_lower:
                found.append(skill)
    return list(set(found))


def analyze_skill_gap(resume_text: str, jd_text: str) -> Dict:
    """
    Deep skill gap analysis:
    - Matched skills (in both resume and JD)
    - Missing skills (in JD but not resume) 
    - Bonus skills (in resume but not JD)
    - Semantic matches (similar meaning, different words)
    """
    resume_skills = set(extract_skills_from_text(resume_text))
    jd_skills = set(extract_skills_from_text(jd_text))

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills
    bonus = resume_skills - jd_skills

    # Semantic matching for missing skills
    semantic_matches = []
    truly_missing = []

    if missing:
        resume_emb = embed_text(resume_text)
        for skill in missing:
            skill_emb = embed_text(skill)
            sim = cosine_similarity(resume_emb, skill_emb)
            if sim > 0.30:  # Threshold for semantic similarity
                semantic_matches.append({
                    "skill": skill,
                    "similarity": round(sim * 100, 1),
                    "note": "Semantically related content found in resume"
                })
            else:
                truly_missing.append(skill)

    # Categorize matched skills
    matched_by_category = {}
    for skill in matched:
        for cat, skills in SKILL_CATEGORIES.items():
            if skill in skills:
                matched_by_category.setdefault(cat, []).append(skill)

    return {
        "matched_skills": sorted(matched),
        "missing_skills": sorted(truly_missing),
        "semantic_matches": sorted(semantic_matches, key=lambda x: -x['similarity']),
        "bonus_skills": sorted(bonus),
        "matched_by_category": matched_by_category,
        "match_rate": round(len(matched) / max(len(jd_skills), 1) * 100, 1),
        "total_jd_skills": len(jd_skills),
        "total_resume_skills": len(resume_skills)
    }


def get_key_requirements(jd_text: str, top_n: int = 5) -> List[str]:
    """
    Extract the top N most important requirements from a JD
    using sentence-level importance scoring.
    """
    sentences = [
        s.strip() for s in re.split(r'[.\n]', jd_text)
        if len(s.strip()) > 30
    ]
    if not sentences:
        return []

    # Score sentences by keyword density
    important_keywords = [
        'required', 'must', 'minimum', 'experience', 'proficient',
        'expertise', 'strong', 'essential', 'proven', 'demonstrated'
    ]

    scored = []
    for sent in sentences:
        score = sum(1 for kw in important_keywords if kw in sent.lower())
        scored.append((score, sent))

    scored.sort(reverse=True)
    return [s[1] for s in scored[:top_n]]


def generate_feedback(skill_gap: Dict, score: float) -> List[str]:
    """Generate human-readable feedback bullets based on analysis."""
    feedback = []

    if score >= 75:
        feedback.append("✅ Strong overall match — this candidate aligns well with the role.")
    elif score >= 55:
        feedback.append("⚠️ Moderate match — candidate covers core areas but has gaps.")
    else:
        feedback.append("❌ Weak match — significant skill gaps detected.")

    if skill_gap['matched_skills']:
        top_matched = ', '.join(skill_gap['matched_skills'][:5])
        feedback.append(f"🎯 Key matching skills: {top_matched}")

    if skill_gap['missing_skills']:
        top_missing = ', '.join(skill_gap['missing_skills'][:5])
        feedback.append(f"📌 Skills to look for: {top_missing}")

    if skill_gap['semantic_matches']:
        top_semantic = skill_gap['semantic_matches'][0]
        feedback.append(
            f"🔍 '{top_semantic['skill']}' not explicitly mentioned but semantically related content found."
        )

    if skill_gap['bonus_skills']:
        top_bonus = ', '.join(skill_gap['bonus_skills'][:3])
        feedback.append(f"⭐ Bonus skills beyond JD: {top_bonus}")

    return feedback
