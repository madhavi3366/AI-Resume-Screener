import re

def calculate_ats_score(job_description, resume_skills):
    # Extract words from the job description
    jd_words = re.findall(r"[A-Za-z\+#/.]+", job_description.lower())

    # Remove duplicates
    jd_skills = list(set(jd_words))

    resume_skills = [skill.lower() for skill in resume_skills]

    matched = []

    for skill in jd_skills:
        if skill in resume_skills:
            matched.append(skill)

    if len(jd_skills) == 0:
        score = 0
    else:
        score = round((len(matched) / len(jd_skills)) * 100)

    return score, matched