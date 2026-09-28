RELATED_SKILLS = {
    "machine learning": {
        "deep learning",
        "scikit-learn",
    },

    "deep learning": {
        "machine learning",
    },

    "scikit-learn": {
        "machine learning",
    },

    "docker": {
        "kubernetes",
    },

    "kubernetes": {
        "docker",
    },

    "github": {
        "git",
    },

    "git": {
        "github",
    },
}


def are_related(
    candidate_skill: str,
    job_skill: str,
) -> bool:
    """
    Determine whether two canonical skills have an
    explicitly defined partial relationship.
    """

    candidate = candidate_skill.lower()
    job = job_skill.lower()

    if candidate == job:
        return False

    return job in RELATED_SKILLS.get(
        candidate,
        set(),
    )