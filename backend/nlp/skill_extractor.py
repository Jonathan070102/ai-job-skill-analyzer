import re

from nlp.skills_data import SKILLS


def normalize_text(text: str) -> str:
    """
    Normalize text for easier skill matching.
    """
    text = text.lower()

    text = text.replace("–", "-")
    text = text.replace("—", "-")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def alias_pattern(alias: str) -> re.Pattern:
    """
    Build a regex pattern for matching a skill alias.
    """
    escaped = re.escape(alias.lower())

    return re.compile(
        rf"(?<!\w){escaped}(?!\w)",
        re.IGNORECASE
    )


def find_evidence_line(
    text: str,
    alias: str,
) -> str | None:
    """
    Find the shortest useful line containing the matched alias.
    """

    lines = text.splitlines()

    pattern = alias_pattern(alias)

    for line in lines:
        cleaned_line = line.strip()

        if not cleaned_line:
            continue

        if pattern.search(cleaned_line):
            # Prevent extremely long evidence blocks.
            if len(cleaned_line) > 300:
                return cleaned_line[:300].rstrip() + "..."

            return cleaned_line

    return None


def extract_skills(
    text: str,
    section: str = "general",
) -> list[dict]:
    """
    Extract canonical skills from a text block.

    Each detected skill contains:
    - canonical skill name
    - category
    - matched alias
    - section
    - concise evidence
    """

    detected = []

    normalized_text = normalize_text(text)

    for category, skills in SKILLS.items():
        for canonical_name, aliases in skills.items():

            best_alias = None

            sorted_aliases = sorted(
                aliases,
                key=len,
                reverse=True,
            )

            for alias in sorted_aliases:
                pattern = alias_pattern(alias)

                if pattern.search(normalized_text):
                    best_alias = alias
                    break

            if not best_alias:
                continue

            evidence = find_evidence_line(
                text=text,
                alias=best_alias,
            )

            detected.append(
                {
                    "skill": canonical_name,
                    "category": category,
                    "matched_alias": best_alias,
                    "section": section,
                    "evidence": [
                        evidence
                        if evidence
                        else canonical_name
                    ],
                }
            )

    return detected


def extract_skills_from_sections(
    sections: dict[str, list[str]],
) -> list[dict]:
    """
    Extract skills separately from each detected
    resume section.
    """

    all_skills = []

    for section, content in sections.items():

        if not content:
            continue

        section_text = "\n".join(content)

        skills = extract_skills(
            text=section_text,
            section=section,
        )

        all_skills.extend(skills)

    return all_skills