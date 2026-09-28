from pathlib import Path

from parsers.document_parser import extract_text
from parsers.section_detector import detect_sections
from nlp.skill_extractor import extract_skills_from_sections


resume_path = Path(
    "sample-resume-information-technology.pdf"
)

file_bytes = resume_path.read_bytes()

resume_text = extract_text(
    file_bytes=file_bytes,
    filename=resume_path.name,
)

sections = detect_sections(resume_text)

detected_sections = {
    section: content
    for section, content in sections.items()
    if content
}

skills = extract_skills_from_sections(
    detected_sections
)

print("\nDETECTED SKILLS")
print("=" * 60)

for item in skills:
    print(f"\nSkill: {item['skill']}")
    print(f"Category: {item['category']}")
    print(f"Section: {item['section']}")
    print(f"Alias: {item['matched_alias']}")
    print(f"Evidence: {item['evidence'][0]}")

print("\n" + "=" * 60)
print(f"Total detected skills: {len(skills)}")