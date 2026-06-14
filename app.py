"""
app.py - Streamlit UI for AI Resume Screener
Run: streamlit run app.py
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from src.parser import extract_text_from_pdf, extract_text_from_txt, extract_contact_info
from src.scorer import score_resume, rank_resumes
from src.explainer import analyze_skill_gap, generate_feedback, get_key_requirements
from src.bias_detector import detect_bias

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .score-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    .score-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1a1a2e;
    }
    .tag {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    .tag-green { background: #d1fae5; color: #065f46; }
    .tag-red { background: #fee2e2; color: #991b1b; }
    .tag-yellow { background: #fef3c7; color: #92400e; }
    .tag-blue { background: #dbeafe; color: #1e40af; }
    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1a1a2e;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 0.4rem;
        margin: 1rem 0 0.8rem 0;
    }
    .rank-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.4rem 1rem;
    }
</style>
""", unsafe_allow_html=True)


# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🧠 AI Resume Screener</h1>
    <p style="font-size:1.1rem; opacity:0.85;">
        Semantic matching powered by Sentence-BERT · Skill gap analysis · Bias detection
    </p>
</div>
""", unsafe_allow_html=True)


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    mode = st.radio(
        "Screening Mode",
        ["Single Resume", "Batch Ranking"],
        help="Single: deep analysis of one resume. Batch: rank multiple resumes."
    )
    show_bias = st.toggle("🔍 Bias Detection", value=True)
    show_skill_gap = st.toggle("📊 Skill Gap Analysis", value=True)
    show_contact = st.toggle("📇 Contact Extraction", value=True)

    st.markdown("---")
    st.markdown("**How it works:**")
    st.markdown("""
    1. Upload resume(s) + paste JD
    2. SBERT encodes both semantically
    3. Cosine similarity = match score
    4. Skill gap shows what's missing
    5. Bias scan flags JD language
    """)
    st.markdown("---")
    st.markdown("Built with `sentence-transformers`, `pdfplumber`, `streamlit`")


# ─── Job Description Input ───────────────────────────────────────────────────
st.markdown("### 📋 Job Description")
jd_text = st.text_area(
    "Paste the full job description here",
    height=200,
    placeholder="Paste the job description here...\n\nExample: We are looking for a Senior ML Engineer with 3+ years of experience in PyTorch, Python, and NLP..."
)

st.markdown("---")

# ─── Mode: Single Resume ────────────────────────────────────────────────────
if mode == "Single Resume":
    st.markdown("### 📄 Upload Resume")
    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "Upload a PDF resume",
            type=["pdf"],
            help="PDF format only"
        )

    with col2:
        manual_text = st.text_area(
            "Or paste resume text directly",
            height=150,
            placeholder="Paste resume text here if you don't have a PDF..."
        )

    if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
        if not jd_text.strip():
            st.error("Please paste a job description first.")
        elif not uploaded_file and not manual_text.strip():
            st.error("Please upload a resume PDF or paste resume text.")
        else:
            with st.spinner("Analyzing... (first run loads the AI model ~30s)"):

                # Extract resume text
                try:
                    if uploaded_file:
                        resume_text = extract_text_from_pdf(file_bytes=uploaded_file.read())
                        resume_name = uploaded_file.name
                    else:
                        resume_text = extract_text_from_txt(manual_text)
                        resume_name = "Pasted Resume"

                    if len(resume_text) < 50:
                        st.error("Could not extract enough text from the resume. Try pasting text manually.")
                        st.stop()

                    # Score
                    score_result = score_resume(resume_text, jd_text)

                    # Optional analyses
                    skill_gap = analyze_skill_gap(resume_text, jd_text) if show_skill_gap else None
                    feedback = generate_feedback(skill_gap, score_result['overall_score']) if skill_gap else []
                    bias_result = detect_bias(jd_text) if show_bias else None
                    contact = extract_contact_info(resume_text) if show_contact else {}
                    key_reqs = get_key_requirements(jd_text)

                    st.success("Analysis complete!")

                except Exception as e:
                    st.error(f"Error during analysis: {e}")
                    st.stop()

            # ─── Results ────────────────────────────────────────────────────
            st.markdown("---")
            st.markdown(f"## 📊 Results for `{resume_name}`")

            # Score Cards
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""
                <div class="score-card">
                    <div style="font-size:0.9rem;color:#64748b;">Overall Match</div>
                    <div class="score-number">{score_result['overall_score']}%</div>
                    <div>{score_result['rank_label']}</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="score-card">
                    <div style="font-size:0.9rem;color:#64748b;">Semantic Score</div>
                    <div class="score-number">{score_result['semantic_score']}%</div>
                    <div style="font-size:0.8rem;color:#94a3b8;">Full-text similarity</div>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                st.markdown(f"""
                <div class="score-card">
                    <div style="font-size:0.9rem;color:#64748b;">Sentence Score</div>
                    <div class="score-number">{score_result['sentence_score']}%</div>
                    <div style="font-size:0.8rem;color:#94a3b8;">Sentence-level matching</div>
                </div>
                """, unsafe_allow_html=True)

            # Progress bar
            st.progress(score_result['overall_score'] / 100)

            tabs = st.tabs(["💬 Feedback", "🔧 Skill Gap", "🚩 Bias Report", "📇 Contact"])

            # Tab 1: Feedback
            with tabs[0]:
                st.markdown('<div class="section-header">AI Feedback</div>', unsafe_allow_html=True)
                for f in feedback:
                    st.markdown(f"- {f}")

                if key_reqs:
                    st.markdown('<div class="section-header">Key JD Requirements</div>', unsafe_allow_html=True)
                    for req in key_reqs:
                        st.markdown(f"→ {req}")

            # Tab 2: Skill Gap
            with tabs[1]:
                if skill_gap:
                    c1, c2 = st.columns(2)
                    with c1:
                        st.metric("Skills Match Rate", f"{skill_gap['match_rate']}%")
                        st.metric("JD Skills Found", skill_gap['total_jd_skills'])
                    with c2:
                        st.metric("Matched", len(skill_gap['matched_skills']))
                        st.metric("Missing", len(skill_gap['missing_skills']))

                    st.markdown('<div class="section-header">✅ Matched Skills</div>', unsafe_allow_html=True)
                    if skill_gap['matched_skills']:
                        tags = ' '.join([f'<span class="tag tag-green">{s}</span>' for s in skill_gap['matched_skills']])
                        st.markdown(tags, unsafe_allow_html=True)
                    else:
                        st.info("No direct skill matches found.")

                    st.markdown('<div class="section-header">❌ Missing Skills</div>', unsafe_allow_html=True)
                    if skill_gap['missing_skills']:
                        tags = ' '.join([f'<span class="tag tag-red">{s}</span>' for s in skill_gap['missing_skills']])
                        st.markdown(tags, unsafe_allow_html=True)
                    else:
                        st.success("No critical missing skills!")

                    if skill_gap['semantic_matches']:
                        st.markdown('<div class="section-header">🔍 Semantic Matches (implied skills)</div>', unsafe_allow_html=True)
                        for sm in skill_gap['semantic_matches']:
                            st.markdown(f"- **{sm['skill']}** — {sm['similarity']}% semantic similarity ({sm['note']})")

                    if skill_gap['bonus_skills']:
                        st.markdown('<div class="section-header">⭐ Bonus Skills (beyond JD)</div>', unsafe_allow_html=True)
                        tags = ' '.join([f'<span class="tag tag-blue">{s}</span>' for s in skill_gap['bonus_skills']])
                        st.markdown(tags, unsafe_allow_html=True)
                else:
                    st.info("Skill gap analysis disabled.")

            # Tab 3: Bias
            with tabs[2]:
                if bias_result:
                    st.markdown(f"**Bias Level:** {bias_result['bias_level']} (Score: {bias_result['bias_score']})")
                    if bias_result['flags']:
                        for flag in bias_result['flags']:
                            st.warning(flag)
                    else:
                        st.success("✅ No significant bias detected in the job description.")

                    if bias_result['recommendations']:
                        st.markdown('<div class="section-header">💡 Recommendations</div>', unsafe_allow_html=True)
                        for rec in bias_result['recommendations']:
                            st.info(rec)
                else:
                    st.info("Bias detection disabled.")

            # Tab 4: Contact
            with tabs[3]:
                if contact:
                    for k, v in contact.items():
                        st.markdown(f"**{k.title()}:** `{v}`")
                else:
                    st.info("No contact information found or extraction disabled.")


# ─── Mode: Batch Ranking ────────────────────────────────────────────────────
else:
    st.markdown("### 📂 Upload Multiple Resumes")
    uploaded_files = st.file_uploader(
        "Upload multiple PDF resumes",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload 2+ resumes to rank them"
    )

    if st.button("🏆 Rank All Resumes", type="primary", use_container_width=True):
        if not jd_text.strip():
            st.error("Please paste a job description first.")
        elif not uploaded_files or len(uploaded_files) < 2:
            st.error("Please upload at least 2 resumes for batch ranking.")
        else:
            with st.spinner(f"Ranking {len(uploaded_files)} resumes..."):
                resumes = []
                errors = []
                for f in uploaded_files:
                    try:
                        text = extract_text_from_pdf(file_bytes=f.read())
                        resumes.append({"name": f.name, "text": text})
                    except Exception as e:
                        errors.append(f"{f.name}: {e}")

                if errors:
                    for err in errors:
                        st.warning(f"Skipped — {err}")

                if len(resumes) < 2:
                    st.error("Not enough valid resumes to rank.")
                    st.stop()

                ranked = rank_resumes(resumes, jd_text)
                bias_result = detect_bias(jd_text) if show_bias else None

            st.markdown("---")
            st.markdown(f"## 🏆 Rankings — {len(ranked)} Resumes")

            # Show ranking table
            for r in ranked:
                medal = ["🥇", "🥈", "🥉"][r['rank'] - 1] if r['rank'] <= 3 else f"#{r['rank']}"
                st.markdown(f"""
                <div class="rank-card">
                    <span style="font-size:1.5rem;margin-right:1rem">{medal}</span>
                    <div style="flex:1">
                        <strong>{r['name']}</strong>
                        <span style="margin-left:1rem">{r['rank_label']}</span>
                    </div>
                    <div class="score-number" style="font-size:1.5rem">{r['overall_score']}%</div>
                </div>
                """, unsafe_allow_html=True)

            # Bias section
            if bias_result:
                st.markdown("---")
                st.markdown("### 🚩 JD Bias Report")
                st.markdown(f"**Bias Level:** {bias_result['bias_level']}")
                for flag in bias_result['flags']:
                    st.warning(flag)


# ─── Footer ─────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center style='color:#94a3b8;font-size:0.85rem'>"
    "AI Resume Screener · Powered by Sentence-BERT · Built with Streamlit"
    "</center>",
    unsafe_allow_html=True
)
