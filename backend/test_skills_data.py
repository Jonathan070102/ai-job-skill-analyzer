from nlp.skills_data import SKILLS


total_skills = 0

for category, skills in SKILLS.items():
    total_skills += len(skills)

    print(f"\n{category.upper()}")

    for skill, aliases in skills.items():
        print(f"- {skill}: {aliases}")


print("\n---------------------------")
print(f"Total canonical skills: {total_skills}")
print("---------------------------")