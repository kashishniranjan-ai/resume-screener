"""
scorer.py - Score and rank resumes against a job description using semantic similarity
"""

import numpy as np
from typing import List, Dict
from src.embedder import embed_text, cosine_similarity, batch_similarity


def score_resume(resume_text: str, jd_text: str) -> Dict:
    """
    Score a single resume against a job description.

    Returns:
        dict with overall_score, section_scores, and rank_label
    """
    # Full-text semantic similarity
    resume_emb = embed_text(resume_text)
    jd_emb = embed_text(jd_text)
    overall = cosine_similarity(resume_emb, jd_emb)

    # Sentence-level scoring for deeper context
    jd_sentences = [s.strip() for s in jd_text.replace('\n', '. ').split('.') if len(s.strip()) > 20]
    if jd_sentences:
        resume_chunks = chunk_text(resume_text, chunk_size=200)
        if resume_chunks:
            resume_chunk_embs = embed_text(resume_chunks)
            jd_sent_embs = embed_text(jd_sentences)
            # Max-pooled sentence similarity
            sim_matrix = resume_chunk_embs @ jd_sent_embs.T
            sentence_score = float(np.mean(np.max(sim_matrix, axis=0)))
        else:
            sentence_score = overall
    else:
        sentence_score = overall

    # Weighted final score
    final_score = 0.55 * overall + 0.45 * sentence_score

    return {
        "overall_score": round(final_score * 100, 2),
        "semantic_score": round(overall * 100, 2),
        "sentence_score": round(sentence_score * 100, 2),
        "rank_label": get_rank_label(final_score),
        "raw_score": final_score
    }


def rank_resumes(resumes: List[Dict], jd_text: str) -> List[Dict]:
    """
    Score and rank multiple resumes against a JD.

    Args:
        resumes: list of dicts with keys 'name' and 'text'
        jd_text: job description text

    Returns:
        Sorted list of results (highest score first)
    """
    jd_emb = embed_text(jd_text)
    resume_texts = [r['text'] for r in resumes]
    resume_embs = embed_text(resume_texts)

    scores = batch_similarity(jd_emb, resume_embs)

    results = []
    for i, resume in enumerate(resumes):
        base_score = float(scores[i])
        results.append({
            "name": resume['name'],
            "overall_score": round(base_score * 100, 2),
            "rank_label": get_rank_label(base_score),
            "raw_score": base_score
        })

    results.sort(key=lambda x: x['raw_score'], reverse=True)
    for i, r in enumerate(results):
        r['rank'] = i + 1

    return results


def get_rank_label(score: float) -> str:
    """Convert numeric score to human-readable label."""
    if score >= 0.75:
        return "🟢 Excellent Match"
    elif score >= 0.60:
        return "🟡 Good Match"
    elif score >= 0.45:
        return "🟠 Partial Match"
    else:
        return "🔴 Low Match"


def chunk_text(text: str, chunk_size: int = 200) -> List[str]:
    """Split text into chunks of roughly chunk_size characters."""
    words = text.split()
    chunks = []
    current = []
    current_len = 0
    for word in words:
        current.append(word)
        current_len += len(word) + 1
        if current_len >= chunk_size:
            chunks.append(' '.join(current))
            current = []
            current_len = 0
    if current:
        chunks.append(' '.join(current))
    return chunks
