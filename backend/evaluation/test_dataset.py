TEST_CASES = [

    # =====================================================
    # EXACT / NORMALIZED MATCHES
    # =====================================================

    {
        "candidate_skill": {
            "skill": "Python",
            "category": "programming_languages",
            "evidence": ["Developed applications using Python"],
        },
        "job_skill": {
            "skill": "Python",
            "category": "programming_languages",
            "evidence": ["Python development experience required"],
        },
        "expected": "matched",
    },

    {
        "candidate_skill": {
            "skill": "PostgreSQL",
            "category": "databases",
            "evidence": ["Used PostgreSQL for application data"],
        },
        "job_skill": {
            "skill": "PostgreSQL",
            "category": "databases",
            "evidence": ["Experience with PostgreSQL"],
        },
        "expected": "matched",
    },

    {
        "candidate_skill": {
            "skill": "Git",
            "category": "devops_tools",
            "evidence": ["Used Git for version control"],
        },
        "job_skill": {
            "skill": "Git",
            "category": "devops_tools",
            "evidence": ["Git experience required"],
        },
        "expected": "matched",
    },

    {
        "candidate_skill": {
            "skill": "REST API",
            "category": "backend",
            "evidence": ["Built RESTful backend services"],
        },
        "job_skill": {
            "skill": "REST API",
            "category": "backend",
            "evidence": ["Experience developing REST APIs"],
        },
        "expected": "matched",
    },

    # =====================================================
    # SEMANTICALLY RELATED / PARTIAL
    # =====================================================

    {
        "candidate_skill": {
            "skill": "Machine Learning",
            "category": "aiml",
            "evidence": [
                "Built machine learning classification models"
            ],
        },
        "job_skill": {
            "skill": "Deep Learning",
            "category": "aiml",
            "evidence": [
                "Experience with deep learning models"
            ],
        },
        "expected": "partial",
    },

    {
        "candidate_skill": {
            "skill": "Python",
            "category": "programming_languages",
            "evidence": [
                "Developed Python backend applications"
            ],
        },
        "job_skill": {
            "skill": "FastAPI",
            "category": "backend",
            "evidence": [
                "Experience developing FastAPI services"
            ],
        },
        "expected": "missing",
    },

    {
        "candidate_skill": {
            "skill": "Docker",
            "category": "devops_tools",
            "evidence": [
                "Containerized applications using Docker"
            ],
        },
        "job_skill": {
            "skill": "Kubernetes",
            "category": "devops_tools",
            "evidence": [
                "Experience deploying containers with Kubernetes"
            ],
        },
        "expected": "partial",
    },

    # =====================================================
    # UNRELATED / MISSING
    # =====================================================

    {
        "candidate_skill": {
            "skill": "React",
            "category": "frontend",
            "evidence": [
                "Built web interfaces using React"
            ],
        },
        "job_skill": {
            "skill": "Django",
            "category": "backend",
            "evidence": [
                "Experience developing applications using Django"
            ],
        },
        "expected": "missing",
    },

    {
        "candidate_skill": {
            "skill": "Python",
            "category": "programming_languages",
            "evidence": [
                "Python programming experience"
            ],
        },
        "job_skill": {
            "skill": "Docker",
            "category": "devops_tools",
            "evidence": [
                "Docker containerization experience"
            ],
        },
        "expected": "missing",
    },

    {
        "candidate_skill": {
            "skill": "SQL",
            "category": "databases",
            "evidence": [
                "Wrote SQL queries for databases"
            ],
        },
        "job_skill": {
            "skill": "AWS",
            "category": "cloud",
            "evidence": [
                "AWS cloud experience required"
            ],
        },
        "expected": "missing",
    },

    # =====================================================
    # SAME-DOMAIN BUT NOT SAME SKILL
    # =====================================================

    {
        "candidate_skill": {
            "skill": "MySQL",
            "category": "databases",
            "evidence": [
                "Used MySQL for application storage"
            ],
        },
        "job_skill": {
            "skill": "PostgreSQL",
            "category": "databases",
            "evidence": [
                "PostgreSQL database experience"
            ],
        },
        "expected": "missing",
    },

    {
        "candidate_skill": {
            "skill": "AWS",
            "category": "cloud",
            "evidence": [
                "Deployed applications on AWS"
            ],
        },
        "job_skill": {
            "skill": "Microsoft Azure",
            "category": "cloud",
            "evidence": [
                "Azure cloud experience required"
            ],
        },
        "expected": "missing",
    },

    # =====================================================
    # SOFT SKILLS
    # =====================================================

    {
        "candidate_skill": {
            "skill": "Communication",
            "category": "soft_skills",
            "evidence": [
                "Strong communication and presentation skills"
            ],
        },
        "job_skill": {
            "skill": "Communication",
            "category": "soft_skills",
            "evidence": [
                "Excellent communication skills"
            ],
        },
        "expected": "matched",
    },

    {
        "candidate_skill": {
            "skill": "Teamwork",
            "category": "soft_skills",
            "evidence": [
                "Worked effectively in team projects"
            ],
        },
        "job_skill": {
            "skill": "Leadership",
            "category": "soft_skills",
            "evidence": [
                "Leadership experience required"
            ],
        },
        "expected": "missing",
    },

    # =====================================================
    # AI / ML
    # =====================================================

    {
        "candidate_skill": {
            "skill": "Pandas",
            "category": "aiml",
            "evidence": [
                "Used Pandas for data preprocessing"
            ],
        },
        "job_skill": {
            "skill": "Pandas",
            "category": "aiml",
            "evidence": [
                "Pandas experience required"
            ],
        },
        "expected": "matched",
    },

    {
        "candidate_skill": {
            "skill": "Scikit-learn",
            "category": "aiml",
            "evidence": [
                "Built models using Scikit-learn"
            ],
        },
        "job_skill": {
            "skill": "Machine Learning",
            "category": "aiml",
            "evidence": [
                "Machine learning experience required"
            ],
        },
        "expected": "partial",
    },

    {
        "candidate_skill": {
            "skill": "Computer Vision",
            "category": "aiml",
            "evidence": [
                "Worked on image recognition systems"
            ],
        },
        "job_skill": {
            "skill": "NLP",
            "category": "aiml",
            "evidence": [
                "Natural language processing experience"
            ],
        },
        "expected": "missing",
    },

    # =====================================================
    # DEVOPS
    # =====================================================

    {
        "candidate_skill": {
            "skill": "Linux",
            "category": "devops_tools",
            "evidence": [
                "Worked in Linux environments"
            ],
        },
        "job_skill": {
            "skill": "Linux",
            "category": "devops_tools",
            "evidence": [
                "Linux administration experience"
            ],
        },
        "expected": "matched",
    },

    {
        "candidate_skill": {
            "skill": "GitHub",
            "category": "devops_tools",
            "evidence": [
                "Used GitHub for source control"
            ],
        },
        "job_skill": {
            "skill": "Git",
            "category": "devops_tools",
            "evidence": [
                "Git version control experience"
            ],
        },
        "expected": "partial",
    },
]