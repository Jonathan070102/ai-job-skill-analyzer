def analyze_common_skill_gaps(
    candidate_skills: list[dict],
    skill_demand: list[dict],
    minimum_frequency: float = 50.0,
) -> list[dict]:
    """
    Identify frequently requested skills that are not
    demonstrated by the candidate.

    minimum_frequency:
        Minimum percentage of analyzed jobs in which the
        skill must appear to be considered a common demand.
    """

    candidate_skill_names = {
        skill["skill"].lower()
        for skill in candidate_skills
    }

    common_gaps = []

    for demand in skill_demand:
        skill_name = demand["skill"]

        # Ignore skills below the frequency threshold.
        if demand["frequency_percent"] < minimum_frequency:
            continue

        # Candidate already demonstrates this skill.
        if skill_name.lower() in candidate_skill_names:
            continue

        common_gaps.append(
            {
                "skill": skill_name,
                "category": demand["category"],
                "jobs_count": demand["jobs_count"],
                "total_jobs": demand["total_jobs"],
                "frequency_percent": demand[
                    "frequency_percent"
                ],
                "required_count": demand[
                    "required_count"
                ],
                "preferred_count": demand[
                    "preferred_count"
                ],
            }
        )

    # Most frequently demanded gaps first.
    common_gaps.sort(
        key=lambda item: (
            item["frequency_percent"],
            item["required_count"],
        ),
        reverse=True,
    )

    return common_gaps