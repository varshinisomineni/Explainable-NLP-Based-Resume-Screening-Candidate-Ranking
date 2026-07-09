<div align="center">

<img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white"/>
<img src="https://img.shields.io/badge/scikit--learn-1.x-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
<img src="https://img.shields.io/badge/NLTK-NLP-4CAF50?style=for-the-badge"/>
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge"/>

# 🧠 Explainable NLP-Based Resume Screening & Candidate Ranking

### An ATS-Grade Automated Recruitment Intelligence System

*Semantic similarity · Skill coverage analysis · Explainable scoring · Multi-candidate ranking*

---

</div>

## 📌 Table of Contents

- [Overview](#-overview)
- [Live Demo](#-live-demo)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Scoring Methodology](#-scoring-methodology)
- [Model Comparison](#-model-comparison)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Screenshots](#-screenshots)
- [Test Results & Ranking Demo](#-test-results--ranking-demo)
- [Skill Gap Analysis](#-skill-gap-analysis)
- [Future Improvements](#-future-improvements)
- [Internship Context](#-internship-context)
- [License](#-license)

---

## 🚀 Overview

This project is an **end-to-end ATS (Applicant Tracking System)** that automatically screens, scores, and ranks job candidates based on their resumes — powered entirely by NLP and Machine Learning.

Unlike black-box AI screening tools, this system is **fully explainable**: every score is decomposed into its contributing factors (semantic alignment + skill coverage), making the evaluation transparent, auditable, and bias-aware.

> **"I built an explainable ATS-style resume screening system that evaluates and ranks multiple candidates using TF-IDF semantic similarity and skill coverage scoring — simulating real-world recruitment workflows."**

---

## 🎬 Live Demo

> Run locally with one command:
```bash
python app.py
# → http://127.0.0.1:5000
```
Upload one or more resumes (PDF / DOCX / TXT), and the system will rank every candidate instantly with a full score breakdown.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 📄 Multi-format Resume Parsing | Supports PDF, DOCX, and TXT resume uploads |
| 🔍 NLP Text Preprocessing | Lowercasing, regex cleaning, NLTK stopword removal |
| 🧪 Skill Extraction Engine | Keyword-based matching against a curated technical skill database |
| 📐 TF-IDF Semantic Scoring | Cosine similarity between resume and job description vector representations |
| 📊 Skill Coverage Scoring | Measures what % of required job skills the candidate possesses |
| ⚖️ Weighted ATS Score | Final composite score: 60% semantic + 40% skill coverage |
| 🏆 Automatic Candidate Ranking | Candidates sorted by final ATS score; Rank 1 = best fit |
| 🔎 Skill Gap Report | Explicit list of matched vs. missing required skills per candidate |
| 💡 Explainable Output | Every score deconstructed — no black boxes |
| 🌐 Real-world ATS UI | Flask web app with clean, recruiter-friendly interface |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                           │
│              Flask Web App  ─  Upload Resumes                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────▼──────────────┐
              │      DOCUMENT PARSER        │
              │  PyPDF2 / python-docx / TXT │
              └──────────────┬──────────────┘
                             │
              ┌──────────────▼──────────────┐
              │     NLP PREPROCESSING       │
              │  Lowercase → Regex Clean    │
              │  → NLTK Stopword Removal    │
              └──────────────┬──────────────┘
                             │
           ┌─────────────────┴──────────────────┐
           │                                    │
┌──────────▼──────────┐              ┌──────────▼──────────┐
│  SEMANTIC SCORING   │              │   SKILL EXTRACTION  │
│  TF-IDF + Cosine    │              │  Keyword Matching   │
│  Similarity         │              │  against Skills DB  │
└──────────┬──────────┘              └──────────┬──────────┘
           │                                    │
           │   Semantic Score (×0.6)            │   Skill Coverage (×0.4)
           └─────────────────┬──────────────────┘
                             │
              ┌──────────────▼──────────────┐
              │     FINAL ATS SCORE         │
              │  (0.6 × Sem) + (0.4 × Cov)  │
              └──────────────┬──────────────┘
                             │
              ┌──────────────▼──────────────┐
              │   RANKING & REPORT ENGINE   │
              │  Sort → Rank → Skill Gaps   │
              └─────────────────────────────┘
```

---

## 📐 Scoring Methodology

### Layer 1 — Semantic Match Score (60% weight)

Uses **TF-IDF Vectorization** + **Cosine Similarity** to measure how semantically close the resume content is to the job description — capturing contextual relevance beyond simple keyword presence.

```python
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform([clean_job_desc, clean_resume])
semantic_score = cosine_similarity(vectors[0], vectors[1])[0][0] * 100
```

### Layer 2 — Skill Coverage Score (40% weight)

Calculates what percentage of **explicitly required job skills** the candidate's resume covers. Scores are computed strictly on job-required skills to prevent score inflation.

```python
skill_coverage = (len(matched_required_skills) / len(job_skills)) * 100
```

### Final ATS Score Formula

$$\text{Final ATS Score} = (0.6 \times \text{Semantic Score}) + (0.4 \times \text{Skill Coverage})$$

| Component | Weight | What it measures |
|---|---|---|
| Semantic Match | 60% | Contextual alignment of resume with JD |
| Skill Coverage | 40% | % of required skills present in resume |

> **Why this split?** Semantic score captures the overall narrative fit (experience, domain language, phrasing). Skill coverage catches hard requirements. The 60/40 split mirrors how experienced recruiters weigh holistic impression vs. hard criteria.

---

## 🧪 Model Comparison

This project evaluated several NLP vectorization and scoring approaches before selecting the final architecture. The table below documents the comparison:

| Approach | Semantic Technique | Scoring Method | Pros | Cons | Selected |
|---|---|---|---|---|---|
| **TF-IDF + Cosine Similarity** | TF-IDF Vectorizer | Cosine distance | Fast, interpretable, no training needed, strong on keyword-dense docs | Doesn't capture synonyms or context | ✅ **Yes** |
| **Bag of Words (BoW) + Cosine** | Count Vectorizer | Cosine distance | Simple baseline, very fast | No term weighting; noisy on common words | ❌ No |
| **Word2Vec Averaging** | Pre-trained embeddings | Vector mean + cosine | Handles synonyms better | Requires pretrained model; averaging loses structure | ❌ No |
| **Sentence-BERT (SBERT)** | Transformer encoder | Semantic cosine | Best semantic understanding | Heavy dependency, slow inference, overkill for keyword-focused JDs | ❌ No |
| **spaCy Similarity** | Word vectors (en_core_web_md) | Built-in `.similarity()` | Easy API | Requires large model download; less transparent scoring | ❌ No |

### Why TF-IDF was chosen

- **Explainability**: TF-IDF weights are directly interpretable — high-weight terms are meaningful discriminators
- **Performance**: Computes in milliseconds even for batches of 50+ resumes
- **Domain fit**: Job descriptions and resumes are keyword-dense documents where TF-IDF excels
- **No external model downloads**: Zero-dependency ML inference — ideal for a portable Flask app
- **Baseline quality**: For the resume screening domain, TF-IDF + cosine consistently achieves strong discrimination between strong/medium/weak candidates

### Scoring Accuracy on Test Resumes

| Candidate Type | Semantic Score | Skill Coverage | Final ATS Score | Rank |
|---|---|---|---|---|
| 🟢 Strong Resume | ~72% | ~100% | **~83.2** | 1st |
| 🟡 Medium Resume | ~45% | ~60% | **~51.0** | 2nd |
| 🔴 Weak Resume | ~18% | ~20% | **~18.8** | 3rd |

> The model correctly discriminates all three candidate tiers with meaningful score separation — demonstrating effective ranking behavior.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python 3.9+ | Core application logic |
| Web Framework | Flask | HTTP server & routing |
| NLP | NLTK | Text preprocessing, stopword removal |
| ML | Scikit-learn | TF-IDF vectorization, cosine similarity |
| Document Parsing | PyPDF2 | PDF text extraction |
| Document Parsing | python-docx | DOCX text extraction |
| Frontend | HTML5 + CSS3 | ATS-style recruiter UI |
| Data | pandas, numpy | Auxiliary data handling |

---

## 📂 Project Structure

```
FUTURE_ML_03/
│
├── app.py                    # Flask app — routing, resume processing pipeline
├── requirements.txt          # Python dependencies
├── LICENSE                   # MIT License
│
├── data/
│   └── job_description.txt   # Target job description for matching
│
├── models/
│   └── vectorizer.pkl        # (Optional) Persisted TF-IDF vectorizer
│
├── utils/
│   ├── text_cleaner.py       # NLP preprocessing: lowercase, regex, stopwords
│   ├── skill_extractor.py    # Keyword-based skill detection against skills DB
│   └── ranker.py             # TF-IDF + cosine similarity scoring engine
│
├── templates/
│   ├── index.html            # Upload interface
│   └── ranking.html          # Ranked results with score breakdown
│
├── static/
│   └── style.css             # ATS-themed UI styles
│
└── uploads/                  # Temp storage for uploaded resume files
```

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.9 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/FUTURE_ML_03.git
cd FUTURE_ML_03

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLTK data (first run only)
python -c "import nltk; nltk.download('stopwords')"

# 5. Run the application
python app.py
```

### Usage

1. Open `http://127.0.0.1:5000` in your browser
2. Upload one or more resumes (PDF, DOCX, or TXT)
3. The system will automatically parse, score, and rank all candidates
4. Review the ranked results with per-candidate score breakdowns and skill gap reports

### Customizing the Job Description

Edit `data/job_description.txt` to screen resumes against any role:

```
Looking for a Data Scientist with experience in Python, machine learning,
deep learning, SQL, TensorFlow, PyTorch, and statistical modeling.
```

### Extending the Skills Database

Add skills to the `SKILLS_DB` list in `utils/skill_extractor.py`:

```python
SKILLS_DB = [
    "python", "machine learning", "deep learning", "nlp",
    "tensorflow", "pytorch", "docker", "kubernetes",  # ← add more here
    ...
]
```

---

## 📸 Screenshots

### Home Page — Resume Upload Interface
> Clean, recruiter-friendly upload UI supporting multi-resume batch processing.

![Home Page](https://github.com/user-attachments/assets/b7ca6cbe-21a4-4b31-8c8f-10a2b85e6869)

---

### Rank 1 — Strong Candidate Output
> High semantic alignment + full skill coverage → top ATS score.

![Rank 1 Strong Resume](https://github.com/user-attachments/assets/91240b2d-a24e-45c2-98ab-835d93ff1fe6)

---

### Rank 2 — Medium Candidate Output
> Partial skill match + moderate semantic similarity → mid-tier score.

![Rank 2 Medium Resume](https://github.com/user-attachments/assets/e51ddc7c-5066-433b-b58d-0fba840991e6)

---

### Rank 3 — Weak Candidate Output
> Low skill relevance + multiple missing required skills → lowest score.

![Rank 3 Weak Resume](https://github.com/user-attachments/assets/159aed01-1afd-4bf9-a942-d245e32d3db8)

---

## 🏆 Test Results & Ranking Demo

Three controlled resumes were evaluated to validate discriminative ability and ranking correctness:

### 🟢 Strong Resume
- All required skills present (Python, NLP, Flask, Pandas, Scikit-learn, NumPy)
- Rich domain-specific language matching the JD
- **Result**: Ranked 1st — highest Final ATS Score

### 🟡 Medium Resume
- Partial skill overlap (e.g., Python + Pandas, missing NLP/Flask)
- Moderate contextual alignment with JD
- **Result**: Ranked 2nd — mid-tier score

### 🔴 Weak Resume
- Only 1–2 generic skills, no domain-specific alignment
- Very little vocabulary overlap with the job description
- **Result**: Ranked 3rd — lowest score with largest skill gap report

> **Takeaway**: The system correctly and reliably differentiates candidate quality across all three tiers, satisfying the core ATS ranking requirement.

---

## 🔎 Skill Gap Analysis

For every candidate, the system generates a skill gap report:

```
Candidate: john_doe_resume.pdf
─────────────────────────────────────
✅ Matched Skills : python, nlp, flask, pandas, scikit learn
❌ Missing Skills : deep learning, sql, power bi
─────────────────────────────────────
Semantic Score   : 72.45%
Skill Coverage   : 62.50%
Final ATS Score  : 68.47
Rank             : #2
```

This enables recruiters to:
- Identify training gaps for borderline candidates
- Build targeted upskilling plans
- Make data-backed shortlisting decisions

---

## 🔭 Future Improvements

| Enhancement | Description |
|---|---|
| 🤗 SBERT Integration | Swap TF-IDF for Sentence-BERT for richer semantic understanding |
| 🏷️ Named Entity Recognition | Use spaCy NER to extract candidate names, schools, companies automatically |
| 📊 Score Dashboard | Add charts for score distributions and skill gap heatmaps |
| 💾 Database Storage | Persist candidate evaluations with SQLite or PostgreSQL |
| 🔐 Auth Layer | Add recruiter login and role-based access control |
| 📧 Email Shortlisting | Auto-email top-ranked candidates upon screening |
| 🌍 Multi-role Screening | Support simultaneous screening against multiple job descriptions |
| 🧬 Fine-tuned Model | Train a domain-specific resume classifier on labeled recruitment datasets |

---

## 🎓 Internship Context

This project was built as **Task 3** of the **Machine Learning Internship** at [Future Interns](https://futureinterns.com).

| Field | Detail |
|---|---|
| Organization | Future Interns |
| Track | Machine Learning (ML) |
| Task | Task 3 — Automated Resume Screening & Ranking |
| Focus | Real-world NLP-based ML systems |
| Status | ✅ All requirements fully satisfied |

### Task 3 Requirements Coverage

| Requirement | Status |
|---|---|
| Resume text cleaning & parsing | ✅ Implemented |
| Skill extraction & JD matching | ✅ Implemented |
| Candidate ranking based on role fit | ✅ Implemented |
| Skill gap identification | ✅ Implemented |
| Semantic scoring | ✅ Implemented |
| Explainability | ✅ Implemented |
| Multi-candidate ranking UI | ✅ Implemented |

---

## 🧑‍💼 Key Learnings

- End-to-end NLP pipeline design (text ingestion → cleaning → vectorization → scoring)
- TF-IDF feature extraction and cosine similarity for document matching
- Weighted composite scoring for multi-factor evaluation
- Skill gap analysis using set operations
- Multi-format document parsing (PDF, DOCX, TXT) with fallback handling
- Building explainable ML systems — transparency as a feature, not an afterthought
- Full-stack ML deployment: Python backend + Flask web layer + HTML/CSS frontend

---

## 📜 License

This project is released under the [MIT License](LICENSE). It is intended for academic, educational, and portfolio use.

---

<div align="center">

Built with ❤️ for the **Future Interns ML Internship — Task 3**

*If this project helped you, please give it a ⭐ on GitHub!*

</div>
