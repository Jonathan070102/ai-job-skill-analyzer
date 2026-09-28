from matching.skill_matcher import match_skills


candidate_skills = [
    {
        "skill": "Python",
        "category": "programming_languages",
        "matched_aliases": ["python"],
        "sections": ["skills", "projects"],
        "evidence": [
            "Python SQL Git",
            "Built a Python application"
        ],
    },
    {
        "skill": "REST API",
        "category": "backend",
        "matched_aliases": ["restful api"],
        "sections": ["projects"],
        "evidence": [
            "Built RESTful backend services using Python."
        ],
    },
    {
        "skill": "SQL",
        "category": "databases",
        "matched_aliases": ["sql"],
        "sections": ["skills"],
        "evidence": [
            "Python SQL Git"
        ],
    },
]


job_skills = [
    {
        "skill": "Python",
        "category": "programming_languages",
        "requirement_type": "required",
        "evidence": [
            "Strong Python development experience"
        ],
    },
    {
        "skill": "REST API",
        "category": "backend",
        "requirement_type": "required",
        "evidence": [
            "Experience building REST APIs"
        ],
    },
    {
        "skill": "FastAPI",
        "category": "backend",
        "requirement_type": "required",
        "evidence": [
            "Experience with FastAPI"
        ],
    },
    {
        "skill": "Docker",
        "category": "devops_tools",
        "requirement_type": "preferred",
        "evidence": [
            "Docker experience is preferred"
        ],
    },
]


results = match_skills(
    candidate_skills=candidate_skills,
    job_skills=job_skills
)


print("\nSKILL MATCH RESULTS")
print("---------------------------")

for result in results:
    print(
        f"{result['skill']}"
        f" | Status: {result['status']}"
        f" | Similarity: {result['similarity_score']}"
        f" | Candidate: {result['matched_candidate_skill']}"
    )

print("---------------------------")