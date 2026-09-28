def calculate_coverage(results: list[dict]) -> float:
    """
    Calculate skill coverage using:

    Matched = 1.0
    Partial = 0.5
    Missing = 0.0
    """

    if not results:
        return 0.0

    total_score = 0.0

    for result in results:
        status = result["status"]

        if status == "matched":
            total_score += 1.0

        elif status == "partial":
            total_score += 0.5

    coverage = (total_score / len(results)) * 100

    return round(coverage, 2)


def analyze_skill_gap(results: list[dict]) -> dict:
    """
    Organize matching results into matched, partial,
    and missing skill groups.
    """

    matched = []
    partial = []
    missing = []

    for result in results:
        if result["status"] == "matched":
            matched.append(result)

        elif result["status"] == "partial":
            partial.append(result)

        elif result["status"] == "missing":
            missing.append(result)

    coverage = calculate_coverage(results)

    return {
        "coverage_score": coverage,
        "total_requirements": len(results),
        "matched_count": len(matched),
        "partial_count": len(partial),
        "missing_count": len(missing),
        "matched": matched,
        "partial": partial,
        "missing": missing,
    }