from nlp.job_skill_extractor import extract_job_skills


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
    skills = extract_job_skills(JOB_DESCRIPTION)

    print("\nREQUIREMENT CLASSIFICATION TEST")
    print("=" * 60)

    for skill in skills:
        print(
            f"{skill['skill']:<20} "
            f"{skill['requirement_type']}"
        )

    print("=" * 60)


if __name__ == "__main__":
    main()