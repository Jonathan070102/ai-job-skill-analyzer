from nlp.skill_extractor import extract_skills
from nlp.requirement_classifier import classify_skill_requirement
from nlp.skill_normalizer import normalize_extracted_skills


def extract_job_skills(job_description: str) -> list[dict]:
    """
    Extract and normalize skills from a job description.
    """

    raw_skills = extract_skills(
        text=job_description,
        section="job_description"
    )

    for skill in raw_skills:
        skill["requirement_type"] = classify_skill_requirement(
            skill=skill,
            job_description=job_description
        )

    return normalize_extracted_skills(raw_skills)