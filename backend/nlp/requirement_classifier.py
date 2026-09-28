import re


REQUIRED_SECTION_PATTERNS = [
    r"\brequired\s+skills?\b",
    r"\brequired\s+requirements?\b",
    r"\bminimum\s+qualifications?\b",
    r"\bmandatory\s+skills?\b",
    r"\bmust[\s-]+have\b",
    r"\brequirements?\b",
]


PREFERRED_SECTION_PATTERNS = [
    r"\bpreferred\s+skills?\b",
    r"\bpreferred\s+qualifications?\b",
    r"\bnice[\s-]+to[\s-]+have\b",
    r"\bgood\s+to\s+have\b",
    r"\bdesirable\s+skills?\b",
    r"\bbonus\s+skills?\b",
    r"\bpreferred\b",
]


def normalize_text(text: str) -> str:
    """
    Normalize text while preserving enough structure
    for requirement detection.
    """

    text = text.lower()

    text = text.replace("–", "-")
    text = text.replace("—", "-")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def find_section_markers(
    text: str,
) -> list[tuple[int, str]]:
    """
    Find required/preferred section markers.

    Works whether the JD is formatted with newlines
    or flattened into one line.
    """

    normalized = normalize_text(text)

    markers = []

    for pattern in REQUIRED_SECTION_PATTERNS:
        for match in re.finditer(
            pattern,
            normalized,
            re.IGNORECASE,
        ):
            markers.append(
                (
                    match.start(),
                    "required",
                )
            )

    for pattern in PREFERRED_SECTION_PATTERNS:
        for match in re.finditer(
            pattern,
            normalized,
            re.IGNORECASE,
        ):
            markers.append(
                (
                    match.start(),
                    "preferred",
                )
            )

    # Sort by position in the document.
    markers.sort(
        key=lambda item: item[0]
    )

    # Remove duplicate/overlapping markers.
    cleaned = []

    for position, section_type in markers:

        if not cleaned:
            cleaned.append(
                (
                    position,
                    section_type,
                )
            )
            continue

        previous_position, previous_type = cleaned[-1]

        if (
            position - previous_position
            < 3
        ):
            continue

        cleaned.append(
            (
                position,
                section_type,
            )
        )

    return cleaned


def classify_requirement(
    text: str,
) -> str:
    """
    Classify a local text fragment.
    """

    normalized = normalize_text(text)

    has_preferred = any(
        re.search(
            pattern,
            normalized,
            re.IGNORECASE,
        )
        for pattern in PREFERRED_SECTION_PATTERNS
    )

    has_required = any(
        re.search(
            pattern,
            normalized,
            re.IGNORECASE,
        )
        for pattern in REQUIRED_SECTION_PATTERNS
    )

    if has_preferred and not has_required:
        return "preferred"

    if has_required and not has_preferred:
        return "required"

    return "unknown"


def classify_skill_requirement(
    skill: dict,
    job_description: str,
) -> str:
    """
    Determine whether a skill belongs to a required
    or preferred section.

    Handles both:
        Required Skills:
        Python
        Docker

    and flattened text:
        Required Skills: Python Docker Preferred Skills: AWS
    """

    skill_name = skill["skill"]

    normalized = normalize_text(
        job_description
    )

    skill_pattern = re.compile(
        rf"(?<!\w){re.escape(skill_name.lower())}(?!\w)",
        re.IGNORECASE,
    )

    markers = find_section_markers(
        normalized
    )

    if not markers:
        return "unknown"

    # Find every occurrence of the skill.
    skill_matches = list(
        skill_pattern.finditer(
            normalized
        )
    )

    if not skill_matches:
        return "unknown"

    for skill_match in skill_matches:

        skill_position = skill_match.start()

        # Find the most recent section heading
        # before this skill occurrence.
        current_section = "unknown"

        for marker_position, section_type in markers:

            if marker_position <= skill_position:
                current_section = section_type
            else:
                break

        if current_section != "unknown":
            return current_section

    return "unknown"