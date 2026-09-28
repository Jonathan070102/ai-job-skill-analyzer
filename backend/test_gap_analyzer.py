from matching.gap_analyzer import analyze_skill_gap


sample_results = [
    {
        "skill": "Python",
        "status": "matched",
        "requirement_type": "required",
    },
    {
        "skill": "SQL",
        "status": "matched",
        "requirement_type": "required",
    },
    {
        "skill": "FastAPI",
        "status": "partial",
        "requirement_type": "required",
    },
    {
        "skill": "Docker",
        "status": "missing",
        "requirement_type": "preferred",
    },
]


report = analyze_skill_gap(sample_results)

print("\nSKILL GAP REPORT")
print("---------------------------")
print("Coverage:", report["coverage_score"], "%")
print("Total:", report["total_requirements"])
print("Matched:", report["matched_count"])
print("Partial:", report["partial_count"])
print("Missing:", report["missing_count"])

print("\nMatched Skills:")
for item in report["matched"]:
    print("-", item["skill"])

print("\nPartial Skills:")
for item in report["partial"]:
    print("-", item["skill"])

print("\nMissing Skills:")
for item in report["missing"]:
    print("-", item["skill"])

print("---------------------------")