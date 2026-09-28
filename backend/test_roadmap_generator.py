from roadmap.roadmap_generator import (
    generate_learning_roadmap
)


candidate_skills = [
    {
        "skill": "Python",
        "category": "programming_languages",
    }
]


common_skill_gaps = [
    {
        "skill": "Docker",
        "category": "devops_tools",
        "jobs_count": 4,
        "total_jobs": 5,
        "frequency_percent": 80.0,
        "required_count": 3,
        "preferred_count": 1,
    },
    {
        "skill": "FastAPI",
        "category": "backend",
        "jobs_count": 4,
        "total_jobs": 5,
        "frequency_percent": 80.0,
        "required_count": 3,
        "preferred_count": 1,
    },
    {
        "skill": "REST API",
        "category": "backend",
        "jobs_count": 3,
        "total_jobs": 5,
        "frequency_percent": 60.0,
        "required_count": 2,
        "preferred_count": 1,
    },
]


roadmap = generate_learning_roadmap(
    common_skill_gaps=common_skill_gaps,
    candidate_skills=candidate_skills,
)


print("\nLEARNING ROADMAP")
print("---------------------------")

for item in roadmap:
    print(
        f"{item['learning_order']}. "
        f"{item['skill']} | "
        f"Priority: {item['priority_score']} | "
        f"Dependencies: {item['dependencies']}"
    )

print("---------------------------")