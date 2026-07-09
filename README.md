<div align="center">

<img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white"/>
<img src="https://img.shields.io/badge/scikit--learn-1.x-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
<img src="https://img.shields.io/badge/NLTK-NLP-4CAF50?style=for-the-badge"/>
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge"/>

# Explainable NLP-Based Resume Screening & Candidate Ranking

### A transparent, ATS-style candidate ranking engine

*TF-IDF semantic similarity · rule-based skill coverage · fully decomposed scoring*

</div>

---

## Overview

This project screens and ranks multiple resumes against a single job description using two interpretable signals — **semantic similarity** and **required-skill coverage** — combined into one weighted score. There is no black-box model: every final score can be traced back to the exact terms and skills that produced it, which is the actual point of the project.

It is intentionally built without a pretrained embedding model or external API. The entire pipeline — parsing, cleaning, vectorizing, scoring, ranking — runs locally with scikit-learn and NLTK, which keeps it fast, dependency-light, and fully explainable end to end.

```
I built an ATS-style resume ranking system that scores candidates using
TF-IDF cosine similarity and rule-based skill-coverage matching, then
explains every score with a matched/missing skill breakdown per candidate.
```

---

## Key Features

| Feature | Description |
|---|---|
| Multi-format resume parsing | Accepts PDF, DOCX, and TXT uploads in a single batch |
| NLP preprocessing | Lowercasing, non-alphabetic character stripping, NLTK stopword removal |
| Rule-based skill extraction | Substring matching against a configurable skills list |
| TF-IDF semantic scoring | Cosine similarity between job description and resume vectors |
| Skill coverage scoring | % of the JD's required skills found in the resume |
| Weighted composite score | Final score = 60% semantic similarity + 40% skill coverage |
| Automatic ranking | All uploaded candidates sorted best-fit first |
| Per-candidate skill gap report | Explicit matched vs. missing skill lists, no hidden logic |
| Flask web UI | Upload page + a ranked results dashboard with score breakdowns |

---

## How It Works

```
                     ┌───────────────────────────┐
                     │   Upload (PDF/DOCX/TXT)   │
                     │      Flask /rank route    │
                     └─────────────┬─────────────┘
                                   │  in-memory, per request
                     ┌─────────────▼─────────────┐
                     │   Resume Text Extraction   │
                     │  PyPDF2 · python-docx · TXT│
                     └─────────────┬─────────────┘
                                   │
                     ┌─────────────▼─────────────┐
                     │      Text Cleaning         │
                     │ lowercase → strip non-alpha│
                     │ → remove NLTK stopwords    │
                     └──────────────┬─────────────┘
                                   │
                ┌──────────────────┴───────────────────┐
                │                                       │
   ┌────────────▼────────────┐          ┌───────────────▼───────────────┐
   │   Semantic Similarity    │          │        Skill Extraction        │
   │ TF-IDF fit on [JD, resume]│          │  substring match vs SKILLS_DB  │
   │ + cosine similarity      │          │  matched ∩ / missing − vs JD   │
   └────────────┬────────────┘          └───────────────┬───────────────┘
                │ × 0.6                                 │ × 0.4
                └──────────────────┬────────────────────┘
                                   │
                     ┌─────────────▼─────────────┐
                     │      Final ATS Score       │
                     │  sort → rank → render UI   │
                     └────────────────────────────┘
```

Nothing is persisted to disk — uploaded files are read straight from memory for the duration of the request, scored, and discarded.

---

## Scoring Methodology

### Semantic similarity (60% weight)

For each resume, a fresh `TfidfVectorizer` is fit on a two-document corpus — the cleaned job description and the cleaned resume — and scored with cosine similarity:

```python
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform([clean_job_desc, clean_resume])
semantic_score = cosine_similarity(vectors[0], vectors[1])[0][0] * 100
```

**Design note:** because the vectorizer is re-fit on just these two documents every time, IDF weighting mainly separates terms that appear in one document but not the other, rather than capturing rarity across a large corpus. In practice this behaves close to a weighted term-overlap score — which is a deliberate trade-off for keeping the system stateless and free of any pretrained artifacts, not an attempt to replicate corpus-scale TF-IDF.

### Skill coverage (40% weight)

Skill coverage is calculated only against the job description's required skills, so a resume can't inflate its score by listing irrelevant skills:

```python
skill_coverage = (len(matched_required_skills) / len(job_skills)) * 100
```

### Final score

$$\text{Final ATS Score} = (0.6 \times \text{Semantic Score}) + (0.4 \times \text{Skill Coverage})$$

| Component | Weight | What it captures |
|---|---|---|
| Semantic similarity | 60% | Overall contextual/word-overlap alignment with the JD |
| Skill coverage | 40% | Hard requirement fulfillment |

The split favors holistic alignment over a pure skills checklist, similar to how a recruiter reads a resume before scanning it against a requirements list.

---

## Why TF-IDF Over an Embedding Model

Heavier alternatives (Word2Vec averaging, Sentence-BERT, spaCy's vector similarity) were considered during design rather than implemented and benchmarked here — the table below is the reasoning, not a reported experiment:

| Approach | What it offers | Why it wasn't used here |
|---|---|---|
| **TF-IDF + cosine** (used) | Fast, fully interpretable weights, zero pretrained downloads | — |
| Bag-of-Words + cosine | Simpler baseline | No term weighting; drowned out by frequent, low-signal words |
| Word2Vec averaging | Captures some synonymy | Needs a pretrained model; averaging discards word order/structure |
| Sentence-BERT | Strongest semantic understanding | Heavy dependency and slower inference for a keyword-dense JD-matching task |
| spaCy `.similarity()` | Convenient API | Requires a large model download; similarity scores are less directly explainable |

TF-IDF was chosen because job descriptions and resumes are keyword-dense documents, and because every contributing term weight can be shown to a user — which is the core requirement of an "explainable" screening tool, not just a nice-to-have.

---

## Screenshots

**Upload interface** — batch upload for multiple resumes at once.

![Home Page](https://github.com/user-attachments/assets/b7ca6cbe-21a4-4b31-8c8f-10a2b85e6869)

**Rank 1 — strong match** — full skill coverage, high semantic alignment.

![Rank 1 Strong Resume](https://github.com/user-attachments/assets/91240b2d-a24e-45c2-98ab-835d93ff1fe6)

**Rank 2 — partial match** — some required skills present, moderate alignment.

![Rank 2 Medium Resume](https://github.com/user-attachments/assets/e51ddc7c-5066-433b-b58d-0fba840991e6)

**Rank 3 — weak match** — largest skill gap, lowest score.

![Rank 3 Weak Resume](https://github.com/user-attachments/assets/159aed01-1afd-4bf9-a942-d245e32d3db8)

---

## Example Walkthrough

Running the app against three deliberately different sample resumes (strong / partial / weak match against the sample JD) produces output like this — illustrative numbers from a local run, not a benchmark suite:

```
Candidate: strong_candidate.pdf
─────────────────────────────────────
Matched Skills  : python, nlp, flask, pandas, scikit learn
Missing Skills  : (none)
Semantic Score  : ~72%
Skill Coverage  : ~100%
Final ATS Score : ~83.2
Rank            : #1

Candidate: partial_candidate.pdf
─────────────────────────────────────
Matched Skills  : python, pandas
Missing Skills  : nlp, flask, scikit learn
Semantic Score  : ~45%
Skill Coverage  : ~60%
Final ATS Score : ~51.0
Rank            : #2

Candidate: weak_candidate.pdf
─────────────────────────────────────
Matched Skills  : python
Missing Skills  : nlp, flask, pandas, scikit learn
Semantic Score  : ~18%
Skill Coverage  : ~20%
Final ATS Score : ~18.8
Rank            : #3
```

The gap report is what makes the score actionable — a recruiter (or the candidate) can see exactly which required skills are missing rather than just a single opaque number.

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python 3.9+ | Core application logic |
| Web framework | Flask | Routing, file upload, HTML rendering |
| NLP | NLTK | Stopword removal |
| ML | scikit-learn | TF-IDF vectorization, cosine similarity |
| Document parsing | PyPDF2 | PDF text extraction |
| Document parsing | python-docx | DOCX text extraction |
| Frontend | HTML5 + CSS3 | Upload form and ranked results dashboard |

---

## Project Structure

```
FUTURE_ML_03/
│
├── app.py                    # Flask routes + resume processing pipeline
├── requirements.txt          # Python dependencies
├── LICENSE
│
├── data/
│   └── job_description.txt   # Job description to match resumes against
│
├── models/
│   └── vectorizer.pkl        # Reserved for a future persisted vectorizer (currently unused)
│
├── utils/
│   ├── text_cleaner.py       # Lowercase → strip non-alpha chars → stopword removal
│   ├── skill_extractor.py    # Substring matching against SKILLS_DB
│   └── ranker.py             # TF-IDF + cosine similarity scoring
│
├── templates/
│   ├── index.html            # Upload interface
│   └── ranking.html          # Ranked results with score breakdown
│
└── static/
    └── style.css
```

Uploaded resumes are handled entirely in memory during the request — there is no `uploads/` directory on disk.

---

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/varshinisomineni/Explainable-NLP-Based-Resume-Screening-Candidate-Ranking.git
cd Explainable-NLP-Based-Resume-Screening-Candidate-Ranking

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install python-docx          # required for .docx parsing, see note below

# 4. Download NLTK stopwords (first run only)
python -c "import nltk; nltk.download('stopwords')"

# 5. Run the app
python app.py
```

> **Note:** `app.py` imports `python-docx` for `.docx` parsing, but it isn't currently listed in `requirements.txt` — install it separately as shown above, or add it to the file before deploying.

### Usage

1. Open `http://127.0.0.1:5000`
2. Upload one or more resumes (PDF, DOCX, or TXT)
3. Review the ranked results — each candidate shows its semantic score, skill coverage, and matched/missing skill lists

### Customizing the job description

Edit `data/job_description.txt` to screen against any role:

```
Looking for a Data Scientist with experience in Python, machine learning,
deep learning, SQL, TensorFlow, PyTorch, and statistical modeling.
```

### Extending the skills database

Add entries to `SKILLS_DB` in `utils/skill_extractor.py`:

```python
SKILLS_DB = [
    "python", "machine learning", "deep learning", "nlp",
    "tensorflow", "pytorch", "docker", "kubernetes",  # add more here
    ...
]
```

---

## Known Limitations & Roadmap

Being upfront about current constraints — this is what an explainable system should do with its own shortcomings, too:

- **Hyphenated terms don't match.** Text cleaning strips punctuation without inserting a space, so `scikit-learn` collapses to `scikitlearn` and won't match the `"scikit learn"` entry in `SKILLS_DB`. Digits are stripped entirely as well, so versioned terms like "Python 3.9" reduce to "python".
- **Substring matching, not word-boundary matching.** A short skill like `"sql"` will match as a substring inside longer tokens (e.g., `"mysql"`), which can occasionally produce false positives.
- **`vectorizer.pkl` is currently an empty placeholder** — the TF-IDF vectorizer is fit fresh per request rather than loaded from disk.
- **`requirements.txt` lists `pandas`, `numpy`, and `spaCy`, none of which are imported by the current code** — reserved for planned features (see below) and safe to trim if not needed.

Planned improvements:

| Enhancement | Description |
|---|---|
| Word-boundary skill matching | Tokenize and match on whole words/phrases instead of raw substrings |
| Sentence-BERT option | Swap in transformer-based similarity for cases where synonym matching matters more than speed |
| Persisted vectorizer | Fit once on a larger reference corpus and load it, instead of refitting per request |
| Score dashboard | Visualize score distribution and skill-gap frequency across a batch |
| Database storage | Persist candidate evaluations (SQLite/PostgreSQL) instead of a single-request view |
| Multi-role screening | Score the same batch of resumes against several job descriptions at once |

---

## Internship Context

Built as **Task 3** of the Machine Learning track at **Future Interns**.

| Field | Detail |
|---|---|
| Track | Machine Learning |
| Task | Task 3 — Automated Resume Screening & Ranking |
| Requirements covered | Resume parsing, skill extraction, semantic scoring, ranking, skill gap analysis, explainability |

---

## Key Learnings

- Designing an end-to-end NLP pipeline: ingestion → cleaning → vectorization → scoring
- Trade-offs of fitting TF-IDF on small, per-request corpora vs. a persisted global vectorizer
- Weighted composite scoring across two independent, individually explainable signals
- Multi-format document parsing (PDF/DOCX/TXT) with graceful fallback handling
- Treating explainability as a first-class design constraint rather than a post-hoc add-on

---

## License

Released under the [MIT License](LICENSE) for academic, educational, and portfolio use.
