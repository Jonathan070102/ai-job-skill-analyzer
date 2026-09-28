from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from parsers.document_parser import extract_text
from parsers.section_detector import detect_sections
from parsers.text_cleaner import clean_text

from nlp.skill_extractor import extract_skills_from_sections
from nlp.job_skill_extractor import extract_job_skills
from nlp.skill_normalizer import normalize_extracted_skills


from matching.skill_matcher import match_skills
from matching.gap_analyzer import analyze_skill_gap

from matching.multi_job_analyzer import analyze_skill_demand
from matching.multi_job_schemas import MultiJobRequest

from matching.common_gap_analyzer import analyze_common_skill_gaps

from roadmap.roadmap_generator import generate_learning_roadmap

app = FastAPI(
    title="AI Job Skill-Gap Analyzer API",
    version="0.1.0",
    description="Backend API for the AI Job Skill-Gap Analyzer"
)

# Allow the Next.js frontend to communicate with this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "AI Job Skill-Gap Analyzer API is running",
        "status": "ok"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    allowed_types = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    if file.content_type not in allowed_types:
        return {
            "success": False,
            "message": "Only PDF and DOCX resumes are supported."
        }

    try:
        contents = await file.read()

        extracted_text = extract_text(
            file_bytes=contents,
            filename=file.filename or ""
        )

        if not extracted_text:
            return {
                "success": False,
                "message": "No readable text was found in the document."
            }

        sections = detect_sections(extracted_text)

        detected_sections = {
            section: content
            for section, content in sections.items()
            if content
        }

        raw_skills = extract_skills_from_sections(detected_sections)

        skills = normalize_extracted_skills(raw_skills)

        return {
            "success": True,
            "filename": file.filename,
            "text_length": len(extracted_text),
            "text_preview": extracted_text[:1000],
            "detected_sections": list(detected_sections.keys()),
            "sections": detected_sections,
            "skills": skills,
            "message": "Resume processed successfully."
        }

    except ValueError as error:
        return {
            "success": False,
            "message": str(error)
        }

    except Exception as error:
        return {
            "success": False,
            "message": f"Failed to process the document: {error}"
        }

    except ValueError as error:
        return {
            "success": False,
            "message": str(error)
        }

    except Exception as error:
        return {
            "success": False,
            "message": f"Failed to process the document: {error}"
        }


@app.post("/analyze-job")
async def analyze_job(
    job_title: str = Form(...),
    job_description: str = Form(...)
):
    try:
        cleaned_description = clean_text(job_description)

        if not cleaned_description:
            return {
                "success": False,
                "message": "Job description cannot be empty."
            }

        job_skills = extract_job_skills(cleaned_description)

        return {
            "success": True,
            "job_title": job_title.strip(),
            "description_length": len(cleaned_description),
            "description_preview": cleaned_description[:1500],
            "skills": job_skills,
            "message": "Job description processed successfully."
        }

    except Exception as error:
        return {
            "success": False,
            "message": f"Failed to process job description: {error}"
        }


@app.post("/upload-job-description")
async def upload_job_description(
    file: UploadFile = File(...)
):
    allowed_types = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    if file.content_type not in allowed_types:
        return {
            "success": False,
            "message": "Only PDF and DOCX job descriptions are supported."
        }

    try:
        contents = await file.read()

        extracted_text = extract_text(
            file_bytes=contents,
            filename=file.filename or ""
        )

        if not extracted_text:
            return {
                "success": False,
                "message": "No readable text was found in the job description."
            }

        return {
            "success": True,
            "filename": file.filename,
            "text_length": len(extracted_text),
            "text_preview": extracted_text[:1500],
            "message": "Job description extracted successfully."
        }

    except ValueError as error:
        return {
            "success": False,
            "message": str(error)
        }

    except Exception as error:
        return {
            "success": False,
            "message": f"Failed to process job description: {error}"
        }


@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    job_title: str = Form(...),
    job_description: str = Form(...)
):
    allowed_types = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    if file.content_type not in allowed_types:
        return {
            "success": False,
            "message": "Only PDF and DOCX resumes are supported."
        }

    if not job_title.strip():
        return {
            "success": False,
            "message": "Job title cannot be empty."
        }

    if not job_description.strip():
        return {
            "success": False,
            "message": "Job description cannot be empty."
        }

    try:
        # ==========================================
        # 1. PROCESS RESUME
        # ==========================================
        resume_bytes = await file.read()

        resume_text = extract_text(
            file_bytes=resume_bytes,
            filename=file.filename or ""
        )

        if not resume_text:
            return {
                "success": False,
                "message": "No readable text was found in the resume."
            }

        resume_sections = detect_sections(resume_text)

        detected_sections = {
            section: content
            for section, content in resume_sections.items()
            if content
        }

        raw_resume_skills = extract_skills_from_sections(
            detected_sections
        )

        candidate_skills = normalize_extracted_skills(
            raw_resume_skills
        )

        # ==========================================
        # 2. PROCESS JOB DESCRIPTION
        # ==========================================
        cleaned_job_description = clean_text(job_description)

        if not cleaned_job_description:
            return {
                "success": False,
                "message": "Job description contains no readable text."
            }

        job_skills = extract_job_skills(
            cleaned_job_description
        )

        # ==========================================
        # 3. MATCH SKILLS
        # ==========================================
        match_results = match_skills(
            candidate_skills=candidate_skills,
            job_skills=job_skills
        )

        # ==========================================
        # 4. ANALYZE SKILL GAP
        # ==========================================
        gap_report = analyze_skill_gap(
            results=match_results
        )

        # ==========================================
        # 5. RETURN COMPLETE ANALYSIS
        # ==========================================
        return {
            "success": True,

            "job": {
                "title": job_title.strip(),
                "description_length": len(cleaned_job_description),
                "description_preview": cleaned_job_description[:1500],
                "skills": job_skills,
            },

            "resume": {
                "filename": file.filename,
                "text_length": len(resume_text),
                "detected_sections": list(
                    detected_sections.keys()
                ),
                "skills": candidate_skills,
            },

            "analysis": {
                "coverage_score": gap_report["coverage_score"],
                "total_requirements": gap_report[
                    "total_requirements"
                ],
                "matched_count": gap_report[
                    "matched_count"
                ],
                "partial_count": gap_report[
                    "partial_count"
                ],
                "missing_count": gap_report[
                    "missing_count"
                ],
                "matched": gap_report["matched"],
                "partial": gap_report["partial"],
                "missing": gap_report["missing"],
            },

            "message": "Job skill-gap analysis completed successfully."
        }

    except ValueError as error:
        return {
            "success": False,
            "message": str(error)
        }

    except Exception as error:
        return {
            "success": False,
            "message": f"Analysis failed: {error}"
        }
    
    return {
        "success": True,
        "filename": file.filename,
        "job_title": job_title,
        "message": "End-to-end request received successfully. NLP analysis will be added in later phases.",
        "next_phase": "Resume and job-description processing"
    }

@app.post("/analyze-multiple-jobs")
async def analyze_multiple_jobs(
    file: UploadFile = File(...),
    request: str = Form(...)
):
    allowed_types = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    if file.content_type not in allowed_types:
        return {
            "success": False,
            "message": "Only PDF and DOCX resumes are supported."
        }

    try:
        # -----------------------------------------
        # 1. Parse request JSON
        # -----------------------------------------
        import json

        request_data = json.loads(request)

        multi_job_request = MultiJobRequest(
            **request_data
        )

        # -----------------------------------------
        # 2. Process resume
        # -----------------------------------------
        resume_bytes = await file.read()

        resume_text = extract_text(
            file_bytes=resume_bytes,
            filename=file.filename or ""
        )

        if not resume_text:
            return {
                "success": False,
                "message": "No readable text was found in the resume."
            }

        resume_sections = detect_sections(resume_text)

        detected_sections = {
            section: content
            for section, content in resume_sections.items()
            if content
        }

        raw_resume_skills = extract_skills_from_sections(
            detected_sections
        )

        candidate_skills = normalize_extracted_skills(
            raw_resume_skills
        )

        # -----------------------------------------
        # 3. Process jobs
        # -----------------------------------------
        processed_jobs = []

        for job in multi_job_request.jobs:
            cleaned_description = clean_text(
                job.description
            )

            if not cleaned_description:
                continue

            skills = extract_job_skills(
                cleaned_description
            )

            processed_jobs.append(
                {
                    "title": job.title.strip(),
                    "description": cleaned_description,
                    "skills": skills,
                }
            )

        if not processed_jobs:
            return {
                "success": False,
                "message": "No valid job descriptions were provided."
            }

        # -----------------------------------------
        # 4. Skill demand
        # -----------------------------------------
        skill_demand = analyze_skill_demand(
            jobs=[
                job["skills"]
                for job in processed_jobs
            ]
        )

        # -----------------------------------------
        # 5. Common skill gaps
        # -----------------------------------------
        common_gaps = analyze_common_skill_gaps(
            candidate_skills=candidate_skills,
            skill_demand=skill_demand,
            minimum_frequency=50.0
        )

        roadmap = generate_learning_roadmap(
            common_skill_gaps=common_gaps,
            candidate_skills=candidate_skills,
        )

        # -----------------------------------------
        # 6. Return result
        # -----------------------------------------
        return {
            "success": True,

            "resume": {
                "filename": file.filename,
                "skills": candidate_skills,
            },

            "job_count": len(processed_jobs),

            "jobs": [
                {
                    "title": job["title"],
                    "skills": job["skills"],
                }
                for job in processed_jobs
            ],

            "skill_demand": skill_demand,

            "common_skill_gaps": common_gaps,

            "learning_roadmap": roadmap,

            "message": "Multiple job descriptions analyzed successfully."
        }

    except json.JSONDecodeError:
        return {
            "success": False,
            "message": "Invalid job data."
        }

    except Exception as error:
        return {
            "success": False,
            "message": f"Multi-job analysis failed: {error}"
        }