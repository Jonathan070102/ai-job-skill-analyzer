from nlp.job_skill_extractor import extract_job_skills
from parsers.text_cleaner import clean_text


JOB_DESCRIPTION = """
Junior Python Backend Developer

Required Skills:
Python
FastAPI
PostgreSQL
Docker

Preferred Skills:
AWS
Kubernetes
Linux
"""


def main():
    cleaned = clean_text(JOB_DESCRIPTION)

    print("\nCLEANED JOB DESCRIPTION")
    print("=" * 60)
    print(repr(cleaned))
    print("=" * 60)

    skills = extract_job_skills(cleaned)

    print("\nEXTRACTED JOB SKILLS")
    print("=" * 60)

    for skill in skills:
        print(
            f"{skill['skill']:<20}"
            f"{skill.get('requirement_type', 'MISSING')}"
        )

    print("=" * 60)


if __name__ == "__main__":
    main()