from nlp.skill_normalizer import normalize_extracted_skills


sample_skills = [
    {
        "skill": "Python",
        "category": "programming_languages",
        "matched_alias": "python",
        "section": "skills",
        "evidence": "Python, SQL, Git"
    },
    {
        "skill": "Python",
        "category": "programming_languages",
        "matched_alias": "Python",
        "section": "projects",
        "evidence": "Built a Python application"
    },
    {
        "skill": "Git",
        "category": "devops_tools",
        "matched_alias": "git",
        "section": "skills",
        "evidence": "Python, SQL, Git"
    }
]


result = normalize_extracted_skills(sample_skills)

for skill in result:
    print("\nSkill:", skill["skill"])
    print("Aliases:", skill["matched_aliases"])
    print("Sections:", skill["sections"])
    print("Evidence:", skill["evidence"])