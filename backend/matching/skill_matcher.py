from matching.semantic_matcher import calculate_similarity
from matching.skill_relationships import are_related


# Initial thresholds.
SEMANTIC_MATCH_THRESHOLD = 0.80
SEMANTIC_PARTIAL_THRESHOLD = 0.55


def match_skills(
    candidate_skills: list[dict],
    job_skills: list[dict]
) -> list[dict]:
    """
    Match candidate skills against job requirements using:

    1. Exact canonical matching
    2. Explicit related-skill matching
    3. Semantic similarity
    """

    candidate_lookup = {
        skill["skill"].lower(): skill
        for skill in candidate_skills
    }

    results = []

    for job_skill in job_skills:
        skill_name = job_skill["skill"]
        normalized_name = skill_name.lower()

        # =================================================
        # 1. EXACT CANONICAL MATCH
        # =================================================

        exact_match = candidate_lookup.get(
            normalized_name
        )

        if exact_match:
            results.append(
                {
                    "skill": skill_name,
                    "category": job_skill["category"],
                    "requirement_type": job_skill.get(
                        "requirement_type",
                        "unknown"
                    ),
                    "status": "matched",
                    "similarity_score": 1.0,
                    "matched_candidate_skill": (
                        exact_match["skill"]
                    ),
                    "candidate_evidence": (
                        exact_match.get(
                            "evidence",
                            []
                        )
                    ),
                    "candidate_sections": (
                        exact_match.get(
                            "sections",
                            []
                        )
                    ),
                }
            )

            continue

        # =================================================
        # 2. EXPLICIT RELATED-SKILL MATCH
        # =================================================

        related_candidate = None

        for candidate_skill in candidate_skills:

            if are_related(
                candidate_skill=candidate_skill["skill"],
                job_skill=skill_name,
            ):
                related_candidate = candidate_skill
                break

        if related_candidate:

            similarity = calculate_similarity(
                candidate_skill=related_candidate,
                job_skill=job_skill,
            )

            results.append(
                {
                    "skill": skill_name,
                    "category": job_skill["category"],
                    "requirement_type": job_skill.get(
                        "requirement_type",
                        "unknown"
                    ),
                    "status": "partial",
                    "similarity_score": round(
                        similarity,
                        4
                    ),
                    "matched_candidate_skill": (
                        related_candidate["skill"]
                    ),
                    "candidate_evidence": (
                        related_candidate.get(
                            "evidence",
                            []
                        )
                    ),
                    "candidate_sections": (
                        related_candidate.get(
                            "sections",
                            []
                        )
                    ),
                }
            )

            continue

        # =================================================
        # 3. SEMANTIC MATCHING
        # =================================================

        best_candidate = None
        best_similarity = 0.0

        for candidate_skill in candidate_skills:

            similarity = calculate_similarity(
                candidate_skill=candidate_skill,
                job_skill=job_skill
            )

            if similarity > best_similarity:
                best_similarity = similarity
                best_candidate = candidate_skill

        # =================================================
        # 4. CLASSIFICATION
        # =================================================

        if best_similarity >= SEMANTIC_MATCH_THRESHOLD:
            status = "matched"

        elif best_similarity >= SEMANTIC_PARTIAL_THRESHOLD:
            status = "partial"

        else:
            status = "missing"

        results.append(
            {
                "skill": skill_name,
                "category": job_skill["category"],
                "requirement_type": job_skill.get(
                    "requirement_type",
                    "unknown"
                ),
                "status": status,
                "similarity_score": round(
                    best_similarity,
                    4
                ),
                "matched_candidate_skill": (
                    best_candidate["skill"]
                    if best_candidate
                    else None
                ),
                "candidate_evidence": (
                    best_candidate.get(
                        "evidence",
                        []
                    )
                    if best_candidate
                    else []
                ),
                "candidate_sections": (
                    best_candidate.get(
                        "sections",
                        []
                    )
                    if best_candidate
                    else []
                ),
            }
        )

    return results