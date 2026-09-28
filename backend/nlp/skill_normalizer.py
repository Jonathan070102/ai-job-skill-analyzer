def normalize_extracted_skills(
    skills: list[dict],
) -> list[dict]:
    """
    Remove duplicate canonical skills while preserving
    aliases, sections, and evidence.
    """

    normalized = {}

    for item in skills:
        skill_name = item["skill"]

        if skill_name not in normalized:
            normalized[skill_name] = {
                "skill": item["skill"],
                "category": item["category"],
                "matched_aliases": [],
                "sections": [],
                "evidence": [],
            }

        current = normalized[skill_name]

        # -----------------------------------------
        # Aliases
        # -----------------------------------------

        alias = item.get("matched_alias")

        if alias and alias not in current["matched_aliases"]:
            current["matched_aliases"].append(alias)

        # -----------------------------------------
        # Sections
        # -----------------------------------------

        section = item.get("section")

        if section and section not in current["sections"]:
            current["sections"].append(section)

        # -----------------------------------------
        # Evidence
        # -----------------------------------------

        evidence = item.get("evidence", [])

        if isinstance(evidence, str):
            evidence = [evidence]

        if isinstance(evidence, list):
            for evidence_item in evidence:

                if not isinstance(evidence_item, str):
                    continue

                cleaned_evidence = evidence_item.strip()

                if (
                    cleaned_evidence
                    and cleaned_evidence
                    not in current["evidence"]
                ):
                    current["evidence"].append(
                        cleaned_evidence
                    )

        # -----------------------------------------
        # Requirement type
        # -----------------------------------------

        requirement_type = item.get(
            "requirement_type"
        )

        if requirement_type:
            existing_type = current.get(
                "requirement_type"
            )

            if existing_type is None:
                current["requirement_type"] = (
                    requirement_type
                )

            elif (
                existing_type == "unknown"
                and requirement_type != "unknown"
            ):
                current["requirement_type"] = (
                    requirement_type
                )

    return list(normalized.values())