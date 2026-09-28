import re


SECTION_ALIASES = {
    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "key skills",
        "skills & technologies",
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "work history",
    ],
    "education": [
        "education",
        "academic background",
        "academic qualifications",
        "qualifications",
    ],
    "projects": [
        "projects",
        "personal projects",
        "academic projects",
        "key projects",
    ],
    "certifications": [
        "certifications",
        "certificates",
        "courses",
    ],
    "achievements": [
        "achievements",
        "awards",
        "honors",
    ],
    "languages": [
        "languages",
        "language proficiency",
    ],
}


def normalize_heading(line: str) -> str:
    """
    Normalize a possible section heading.
    """
    line = line.strip().lower()

    # Remove common heading characters.
    line = re.sub(r"[:\-|]+$", "", line)
    line = re.sub(r"\s+", " ", line)

    return line


def detect_sections(text: str) -> dict[str, list[str]]:
    """
    Detect common resume sections and return their text.
    """

    lines = text.splitlines()

    detected = {
        section: []
        for section in SECTION_ALIASES
    }

    current_section = None

    for line in lines:
        cleaned_line = normalize_heading(line)

        if not cleaned_line:
            continue

        matched_section = None

        for section, aliases in SECTION_ALIASES.items():
            if cleaned_line in aliases:
                matched_section = section
                break

        if matched_section:
            current_section = matched_section
            continue

        if current_section:
            detected[current_section].append(line.strip())

    return detected