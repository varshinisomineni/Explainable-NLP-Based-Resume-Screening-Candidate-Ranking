SKILLS_DB = [
    "python", "machine learning", "deep learning", "nlp",
    "data analysis", "flask", "django", "sql", "power bi",
    "excel", "pandas", "numpy", "scikit learn"
]

def extract_skills(text):
    found_skills = []
    for skill in SKILLS_DB:
        if skill in text:
            found_skills.append(skill)
    return list(set(found_skills))
