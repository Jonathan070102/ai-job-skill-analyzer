from matching.semantic_matcher import calculate_similarity


candidate_skill = {
    "skill": "REST API",
    "category": "backend",
    "evidence": [
        "Built RESTful backend services using Python."
    ]
}


job_skill = {
    "skill": "REST API",
    "category": "backend",
    "evidence": [
        "Experience developing REST APIs."
    ]
}


similarity = calculate_similarity(
    candidate_skill,
    job_skill
)


print("\nSEMANTIC MATCHING TEST")
print("---------------------------")
print("Candidate:", candidate_skill["skill"])
print("Job:", job_skill["skill"])
print("Similarity:", similarity)
print("---------------------------")