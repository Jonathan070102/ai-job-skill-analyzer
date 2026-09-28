from matching.common_gap_analyzer import (
    analyze_common_skill_gaps
)


candidate_skills = [
    {
        "skill": "Python",
        "category": "programming_languages",
    },
    {
        "skill": "SQL",
        "category": "databases",
    },
    {
        "skill": "Git",
        "category": "devops_tools",
    },
]


skill_demand = [
    {
        "skill": "Python",
        "category": "programming_languages",
        "jobs_count": 5,
        "total_jobs": 5,
        "frequency_percent": 100.0,
        "required_count": 5,
        "preferred_count": 0,
    },
    {
        "skill": "SQL",
        "category": "databases",
        "jobs_count": 5,
        "total_jobs": 5,
        "frequency_percent": 100.0,
        "required_count": 4,
        "preferred_count": 1,
    },
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
        "skill": "AWS",
        "category": "cloud",
        "jobs_count": 3,
        "total_jobs": 5,
        "frequency_percent": 60.0,
        "required_count": 2,
        "preferred_count": 1,
    },
    {
        "skill": "Kubernetes",
        "category": "devops_tools",
        "jobs_count": 2,
        "total_jobs": 5,
        "frequency_percent": 40.0,
        "required_count": 1,
        "preferred_count": 1,
    },
]


gaps = analyze_common_skill_gaps(
    candidate_skills=candidate_skills,
    skill_demand=skill_demand,
    minimum_frequency=50.0,
)


print("\nCOMMON SKILL GAPS")
print("---------------------------")

for gap in gaps:
    print(
        f"{gap['skill']} | "
        f"{gap['jobs_count']}/{gap['total_jobs']} jobs | "
        f"{gap['frequency_percent']}% | "
        f"Required: {gap['required_count']}"
    )

print("---------------------------")