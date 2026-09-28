from matching.multi_job_analyzer import analyze_skill_demand


job_a = [
    {
        "skill": "Python",
        "category": "programming_languages",
        "requirement_type": "required",
    },
    {
        "skill": "SQL",
        "category": "databases",
        "requirement_type": "required",
    },
    {
        "skill": "Docker",
        "category": "devops_tools",
        "requirement_type": "preferred",
    },
]


job_b = [
    {
        "skill": "Python",
        "category": "programming_languages",
        "requirement_type": "required",
    },
    {
        "skill": "SQL",
        "category": "databases",
        "requirement_type": "required",
    },
    {
        "skill": "AWS",
        "category": "cloud",
        "requirement_type": "preferred",
    },
]


job_c = [
    {
        "skill": "Python",
        "category": "programming_languages",
        "requirement_type": "required",
    },
    {
        "skill": "Docker",
        "category": "devops_tools",
        "requirement_type": "required",
    },
    {
        "skill": "AWS",
        "category": "cloud",
        "requirement_type": "preferred",
    },
]


results = analyze_skill_demand(
    jobs=[
        job_a,
        job_b,
        job_c,
    ]
)


print("\nMULTI-JOB SKILL DEMAND")
print("---------------------------")

for item in results:
    print(
        f"{item['skill']} | "
        f"{item['jobs_count']}/{item['total_jobs']} jobs | "
        f"{item['frequency_percent']}% | "
        f"Required: {item['required_count']} | "
        f"Preferred: {item['preferred_count']}"
    )

print("---------------------------")