from collections import defaultdict


def analyze_skill_demand(
    jobs: list[list[dict]]
) -> list[dict]:
    """
    Analyze how frequently skills appear across multiple jobs.

    Each item in `jobs` is a list of normalized job-skill dictionaries.
    """

    total_jobs = len(jobs)

    if total_jobs == 0:
        return []

    skill_data = defaultdict(
        lambda: {
            "skill": "",
            "category": "",
            "jobs_count": 0,
            "job_indexes": [],
            "required_count": 0,
            "preferred_count": 0,
        }
    )

    for job_index, job_skills in enumerate(jobs):
        # Prevent the same skill from being counted twice
        # within one job.
        seen_in_job = set()

        for skill in job_skills:
            skill_name = skill["skill"]
            normalized_name = skill_name.lower()

            if normalized_name in seen_in_job:
                continue

            seen_in_job.add(normalized_name)

            if not skill_data[normalized_name]["skill"]:
                skill_data[normalized_name]["skill"] = skill_name
                skill_data[normalized_name]["category"] = skill.get(
                    "category",
                    "unknown"
                )

            skill_data[normalized_name]["jobs_count"] += 1
            skill_data[normalized_name]["job_indexes"].append(job_index)

            requirement_type = skill.get(
                "requirement_type",
                "unknown"
            )

            if requirement_type == "required":
                skill_data[normalized_name]["required_count"] += 1

            elif requirement_type == "preferred":
                skill_data[normalized_name]["preferred_count"] += 1

    results = []

    for item in skill_data.values():
        frequency = (
            item["jobs_count"] / total_jobs
        ) * 100

        results.append(
            {
                "skill": item["skill"],
                "category": item["category"],
                "jobs_count": item["jobs_count"],
                "total_jobs": total_jobs,
                "frequency_percent": round(frequency, 2),
                "required_count": item["required_count"],
                "preferred_count": item["preferred_count"],
                "job_indexes": item["job_indexes"],
            }
        )

    # Most frequently requested skills first.
    results.sort(
        key=lambda item: (
            item["jobs_count"],
            item["required_count"],
        ),
        reverse=True
    )

    return results