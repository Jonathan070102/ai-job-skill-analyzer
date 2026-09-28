DEFAULT_DEPENDENCIES = {
    "FastAPI": [
        "Python",
        "REST API",
    ],
    "Django": [
        "Python",
    ],
    "Flask": [
        "Python",
    ],
    "REST API": [],
    "Docker": [
        "Linux",
    ],
    "Kubernetes": [
        "Docker",
        "Linux",
    ],
    "AWS": [
        "Linux",
    ],
    "AWS EC2": [
        "AWS",
    ],
    "AWS S3": [
        "AWS",
    ],
    "TensorFlow": [
        "Python",
        "Machine Learning",
    ],
    "PyTorch": [
        "Python",
        "Machine Learning",
    ],
    "Deep Learning": [
        "Python",
        "Machine Learning",
    ],
    "NLP": [
        "Python",
        "Machine Learning",
    ],
}


def calculate_priority(gap: dict) -> float:
    """
    Calculate priority using job frequency and
    required/preferred importance.
    """

    frequency = gap["frequency_percent"]

    required_count = gap["required_count"]
    preferred_count = gap["preferred_count"]

    total_mentions = required_count + preferred_count

    required_ratio = (
        required_count / total_mentions
        if total_mentions > 0
        else 0
    )

    priority = (
        frequency * 0.7
        + required_ratio * 100 * 0.3
    )

    return round(priority, 2)


def dependency_aware_sort(
    roadmap: list[dict],
) -> list[dict]:
    """
    Reorder roadmap so that a skill appears after its
    prerequisite when that prerequisite is also present
    in the roadmap.

    Example:

    FastAPI -> REST API

    becomes:

    REST API
    FastAPI
    """

    roadmap_by_skill = {
        item["skill"].lower(): item
        for item in roadmap
    }

    ordered = []
    added = set()

    def add_with_dependencies(
        item: dict,
        visiting: set[str],
    ):
        skill_name = item["skill"]
        normalized_name = skill_name.lower()

        if normalized_name in added:
            return

        # Protect against accidental circular dependencies.
        if normalized_name in visiting:
            return

        visiting.add(normalized_name)

        dependencies = item.get(
            "dependencies",
            []
        )

        for dependency in dependencies:
            dependency_item = roadmap_by_skill.get(
                dependency.lower()
            )

            if dependency_item:
                add_with_dependencies(
                    dependency_item,
                    visiting
                )

        visiting.remove(normalized_name)

        if normalized_name not in added:
            ordered.append(item)
            added.add(normalized_name)

    for item in roadmap:
        add_with_dependencies(
            item,
            set()
        )

    return ordered


def generate_learning_roadmap(
    common_skill_gaps: list[dict],
    candidate_skills: list[dict],
) -> list[dict]:
    """
    Generate an ordered learning roadmap from
    common skill gaps.
    """

    candidate_names = {
        skill["skill"].lower()
        for skill in candidate_skills
    }

    roadmap = []

    for gap in common_skill_gaps:
        skill_name = gap["skill"]

        priority_score = calculate_priority(
            gap
        )

        dependencies = DEFAULT_DEPENDENCIES.get(
            skill_name,
            []
        )

        missing_dependencies = [
            dependency
            for dependency in dependencies
            if dependency.lower()
            not in candidate_names
        ]

        roadmap.append(
            {
                "skill": skill_name,
                "category": gap["category"],
                "priority_score": priority_score,
                "frequency_percent": gap[
                    "frequency_percent"
                ],
                "jobs_count": gap["jobs_count"],
                "total_jobs": gap["total_jobs"],
                "required_count": gap[
                    "required_count"
                ],
                "preferred_count": gap[
                    "preferred_count"
                ],
                "dependencies": missing_dependencies,
            }
        )

    # First prioritize high-demand / high-importance skills.
    roadmap.sort(
        key=lambda item: (
            item["priority_score"],
            item["frequency_percent"],
        ),
        reverse=True,
    )

    # Then respect dependencies between skills that
    # are actually present in the roadmap.
    roadmap = dependency_aware_sort(
        roadmap
    )

    # Assign final learning order.
    for index, item in enumerate(
        roadmap,
        start=1
    ):
        item["learning_order"] = index

    return roadmap