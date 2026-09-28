from parsers.section_detector import detect_sections


sample_resume = """
John Doe

Skills
Python
SQL
Git
Machine Learning

Projects
AI Interview System
Smart Shopping Cart

Education
B.Tech Computer Science

Experience
Software Developer Intern

Certifications
Python Certificate
"""


sections = detect_sections(sample_resume)

for section, content in sections.items():
    print(f"\n[{section.upper()}]")

    for line in content:
        print(line)