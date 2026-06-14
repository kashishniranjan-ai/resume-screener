# 🧠 AI Resume Screener


An AI-powered Resume Screening System using Sentence-BERT and Streamlit.

## 🚀 Live Demo

https://resume-screener-dpop9rya4wytftwaayqvd4.streamlit.app/

## Features

- Resume PDF upload
- Semantic matching using Sentence-BERT
- Match score calculation
- Skill gap analysis
- Bias detection
- Streamlit web app

## Tech Stack

- Python
- Streamlit
- Sentence Transformers
- Scikit-learn
- PyTorch

> **Semantic resume screening powered by Sentence-BERT** — goes beyond keyword matching to understand meaning, identify skill gaps, and detect bias in job descriptions.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?logo=streamlit)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow?logo=huggingface)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Demo

![Demo Screenshot](assets/demo.png)

### What makes this different from basic screeners?

| Feature | Keyword Matching | **This Project** |
|---|---|---|
| "built REST APIs" vs "developed web services" | ❌ Different | ✅ Same (semantic) |
| "5 years Python" vs "expert Python developer" | ❌ Miss | ✅ Match |
| Skill gap analysis | ❌ None | ✅ Categorized |
| Bias detection | ❌ None | ✅ Built-in |
| Explainability | ❌ Black box | ✅ Feedback + reasons |

---

## ✨ Features

### 🎯 Semantic Matching (SBERT)
- Uses **`all-MiniLM-L6-v2`** from Sentence Transformers
- Encodes full resume + JD into dense vector embeddings
- Cosine similarity gives a meaningful match score (0-100%)
- Catches synonyms, paraphrases, and contextually similar content

### 📊 Skill Gap Analysis
- Extracts 100+ skills across 7 categories (ML, Cloud, Web, Data, etc.)
- Shows **matched**, **missing**, and **bonus** skills
- **Semantic matching**: finds implied skills even when not explicitly mentioned
- Match rate percentage per job description

### 🚩 Bias Detection
- Flags **masculine-coded** language (based on Gaucher et al. 2011 research)
- Detects **ageist** terms ("digital native", "recent graduate")
- Catches **exclusionary** language ("culture fit", "work hard play hard")
- Scores JD bias level: Low → Moderate → High → Very High
- Actionable recommendations to improve JD inclusivity

### 🏆 Batch Ranking
- Upload 2–20 resumes simultaneously
- Ranks all candidates against the JD
- Gold/Silver/Bronze medals for top candidates

### 📇 Contact Extraction
- Auto-extracts email, phone, LinkedIn, GitHub from resumes

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Semantic Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| PDF Parsing | `pdfplumber` |
| UI | `Streamlit` |
| Deep Learning | `PyTorch` + `HuggingFace Transformers` |
| Similarity | Cosine similarity (numpy) |

---

## 📁 Project Structure

```
resume-screener/
├── app.py                    # Streamlit UI (main entry point)
├── requirements.txt          # Dependencies
├── generate_samples.py       # Generate test resumes
├── src/
│   ├── __init__.py
│   ├── parser.py             # PDF text extraction & cleaning
│   ├── embedder.py           # SBERT embedding & cosine similarity
│   ├── scorer.py             # Resume scoring & batch ranking
│   ├── explainer.py          # Skill gap analysis & feedback
│   └── bias_detector.py      # JD bias detection
├── sample_resumes/           # Test data (generated)
└── assets/
    └── demo.png
```

---

## ⚡ Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/resume-screener.git
cd resume-screener
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```
> ⚠️ First install downloads the SBERT model (~90MB). Subsequent runs are instant.

### 3. Run the app
```bash
streamlit run app.py
```

### 4. Generate sample data (optional)
```bash
python generate_samples.py
```

---

## 🎮 How to Use

### Single Resume Mode
1. Paste a **Job Description** in the text area
2. Upload a **PDF resume** (or paste text)
3. Click **Analyze Resume**
4. View: Match Score → Skill Gap → Bias Report → Contact Info

### Batch Ranking Mode
1. Switch to **Batch Ranking** in the sidebar
2. Paste a **Job Description**
3. Upload **2+ PDF resumes**
4. Click **Rank All Resumes** → see ranked leaderboard

---

## 🧠 How the Scoring Works

```
Overall Score = 0.55 × (full-text cosine similarity)
              + 0.45 × (sentence-level max-pool similarity)
```

**Why sentence-level?**  
Full-text similarity can miss specific requirements buried in the JD. Sentence-level scoring checks whether each JD requirement has a corresponding section in the resume — giving a more fine-grained match.

**Semantic Skill Matching:**  
Instead of checking `if "Python" in resume`, we embed both the skill name and the resume and check if cosine similarity > 0.30 — catching cases like "scripting" matching "Python scripting".

---

## 📊 Score Labels

| Score | Label |
|---|---|
| 75%+ | 🟢 Excellent Match |
| 60–74% | 🟡 Good Match |
| 45–59% | 🟠 Partial Match |
| <45% | 🔴 Low Match |

---

## 🔬 Research Basis

- **SBERT**: [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://arxiv.org/abs/1908.10084) (Reimers & Gurevych, 2019)
- **Bias detection**: [Evidence That Gendered Wording in Job Advertisements Exists](https://psycnet.apa.org/record/2011-09948-003) (Gaucher et al., 2011)
- **Model**: `all-MiniLM-L6-v2` — 6-layer MiniLM fine-tuned for semantic similarity

---

## 🔮 Future Improvements

- [ ] GPT-4 powered detailed feedback generation
- [ ] Named Entity Recognition for better skill extraction (spaCy)
- [ ] Resume parsing into structured JSON (work history, education timeline)
- [ ] ATS score simulation
- [ ] Multi-language support
- [ ] Export results as PDF report
- [ ] Streamlit Cloud deployment

---

## 📝 License

MIT License — feel free to use, modify, and distribute.

---

## 🙏 Acknowledgements

- [Sentence Transformers](https://www.sbert.net/) by UKP Lab
- [Streamlit](https://streamlit.io/) for the UI framework
- [pdfplumber](https://github.com/jsvine/pdfplumber) for PDF parsing

---

*Built as a portfolio project demonstrating practical NLP + Deep Learning skills.*
