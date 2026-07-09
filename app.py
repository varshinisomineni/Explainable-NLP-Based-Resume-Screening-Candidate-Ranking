from flask import Flask, render_template, request
import PyPDF2
from docx import Document

from utils.text_cleaner import clean_text
from utils.skill_extractor import extract_skills
from utils.ranker import score_resume

app = Flask(__name__)

def extract_resume_text(file):
    filename = file.filename.lower()
    text = ""

    if filename.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""

    elif filename.endswith('.docx'):
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text + " "

    elif filename.endswith('.txt'):
        try:
            text = file.read().decode('utf-8')
        except UnicodeDecodeError:
            text = file.read().decode('latin-1')

    return text


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rank', methods=['POST'])
def rank():
    files = request.files.getlist('resumes')

    with open("data/job_description.txt", "r", encoding="utf-8") as f:
        job_description = f.read()

    job_skills = extract_skills(clean_text(job_description))
    ranked_candidates = []

    for file in files:
        resume_text = extract_resume_text(file)

        semantic_score = score_resume(resume_text, job_description) * 100
        resume_skills = extract_skills(clean_text(resume_text))

        matched_required_skills = list(set(job_skills) & set(resume_skills))
        missing_skills = list(set(job_skills) - set(resume_skills))

        skill_coverage = (
            (len(matched_required_skills) / len(job_skills)) * 100
            if job_skills else 0
        )

        final_score = round(
            (0.6 * semantic_score) + (0.4 * skill_coverage), 2
        )

        ranked_candidates.append({
            "name": file.filename,
            "final_score": final_score,
            "semantic_score": round(semantic_score, 2),
            "skill_coverage": round(skill_coverage, 2),
            "matched_skills": matched_required_skills,
            "missing_skills": missing_skills
        })

    # -------- SORT BY FINAL SCORE (RANKING) --------
    ranked_candidates.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return render_template(
        "ranking.html",
        candidates=ranked_candidates
    )


if __name__ == "__main__":
    app.run(debug=True)
