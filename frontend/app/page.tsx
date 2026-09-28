"use client";

import { ChangeEvent, FormEvent, useState } from "react";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://localhost:8000";


/* =========================================================
   TYPES
========================================================= */

interface SkillResult {
  skill: string;
  category: string;
  requirement_type?: string;
  status: "matched" | "partial" | "missing";
  similarity_score: number;
  matched_candidate_skill?: string | null;
  candidate_evidence: string[];
  candidate_sections: string[];
}

interface CandidateSkill {
  skill: string;
  category: string;
  matched_aliases: string[];
  sections: string[];
  evidence: string[];
}

interface MultiJobSkillDemand {
  skill: string;
  category: string;
  jobs_count: number;
  total_jobs: number;
  frequency_percent: number;
  required_count: number;
  preferred_count: number;
  job_indexes: number[];
}

interface CommonSkillGap {
  skill: string;
  category: string;
  jobs_count: number;
  total_jobs: number;
  frequency_percent: number;
  required_count: number;
  preferred_count: number;
}

interface MultiJobResponse {
  success: boolean;

  resume?: {
    filename: string;
    skills: CandidateSkill[];
  };

  job_count?: number;

  jobs?: {
    title: string;
    skills: {
      skill: string;
      category: string;
      requirement_type?: string;
    }[];
  }[];

  skill_demand?: MultiJobSkillDemand[];

  common_skill_gaps?: CommonSkillGap[];

  learning_roadmap?: {
    skill: string;
    category: string;
    priority_score: number;
    frequency_percent: number;
    jobs_count: number;
    total_jobs: number;
    required_count: number;
    preferred_count: number;
    dependencies: string[];
    learning_order: number;
  }[];

  message: string;
}

interface AnalysisResponse {
  success: boolean;

  job?: {
    title: string;
    description_length: number;
    description_preview: string;
    skills: {
      skill: string;
      category: string;
      requirement_type?: string;
      evidence?: string[];
    }[];
  };

  resume?: {
    filename: string;
    text_length: number;
    detected_sections: string[];
    skills: CandidateSkill[];
  };

  analysis?: {
    coverage_score: number;
    total_requirements: number;
    matched_count: number;
    partial_count: number;
    missing_count: number;
    matched: SkillResult[];
    partial: SkillResult[];
    missing: SkillResult[];
  };

  message: string;
}

interface MultiJobInput {
  title: string;
  description: string;
}

/* =========================================================
   COMPONENT
========================================================= */

export default function Home() {
  /* =======================================================
     SINGLE JOB STATE
  ======================================================= */

  const [resume, setResume] = useState<File | null>(null);

  const [jobTitle, setJobTitle] = useState("");

  const [jobDescription, setJobDescription] = useState("");

  const [loading, setLoading] = useState(false);

  const [result, setResult] =
    useState<AnalysisResponse | null>(null);

  const [error, setError] = useState("");

  /* =======================================================
     MULTI JOB STATE
  ======================================================= */

  const [multiJobs, setMultiJobs] = useState<MultiJobInput[]>([
    {
      title: "",
      description: "",
    },
  ]);

  const [multiJobResult, setMultiJobResult] =
    useState<MultiJobResponse | null>(null);

  const [multiJobLoading, setMultiJobLoading] =
    useState(false);

  const [multiJobError, setMultiJobError] =
    useState("");

  /* =======================================================
     RESUME HANDLING
  ======================================================= */

  const handleResumeChange = (
    event: ChangeEvent<HTMLInputElement>
  ) => {
    const file =
      event.target.files?.[0] ?? null;

    setResume(file);

    setResult(null);

    setMultiJobResult(null);

    setError("");

    setMultiJobError("");
  };

  /* =======================================================
     SINGLE JOB ANALYSIS
  ======================================================= */

  const handleAnalyze = async (
    event: FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    setError("");

    setResult(null);

    if (!resume) {
      setError(
        "Please upload your resume."
      );

      return;
    }

    if (!jobTitle.trim()) {
      setError(
        "Please enter the job title."
      );

      return;
    }

    if (!jobDescription.trim()) {
      setError(
        "Please enter the job description."
      );

      return;
    }

    const formData = new FormData();

    formData.append(
      "file",
      resume
    );

    formData.append(
      "job_title",
      jobTitle
    );

    formData.append(
      "job_description",
      jobDescription
    );

    try {
      setLoading(true);

      const response = await fetch(
        `${API_URL}/analyze`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data: AnalysisResponse =
        await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.message ||
          "Analysis failed."
        );
      }

      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to connect to the backend."
      );
    } finally {
      setLoading(false);
    }
  };

  /* =======================================================
     REQUIRED / PREFERRED COUNTS
  ======================================================= */

  const requiredSkillCount =
    result?.job?.skills.filter(
      (skill) =>
        skill.requirement_type ===
        "required"
    ).length ?? 0;

  const preferredSkillCount =
    result?.job?.skills.filter(
      (skill) =>
        skill.requirement_type ===
        "preferred"
    ).length ?? 0;

  /* =======================================================
     MULTI JOB FUNCTIONS
  ======================================================= */

  const addJob = () => {
    if (multiJobs.length >= 10) {
      return;
    }

    setMultiJobs((currentJobs) => [
      ...currentJobs,
      {
        title: "",
        description: "",
      },
    ]);
  };

  const removeJob = (
    index: number
  ) => {
    if (multiJobs.length === 1) {
      return;
    }

    setMultiJobs((currentJobs) =>
      currentJobs.filter(
        (_, jobIndex) =>
          jobIndex !== index
      )
    );
  };

  const updateJob = (
    index: number,
    field: keyof MultiJobInput,
    value: string
  ) => {
    setMultiJobs((currentJobs) =>
      currentJobs.map(
        (job, jobIndex) =>
          jobIndex === index
            ? {
              ...job,
              [field]: value,
            }
            : job
      )
    );
  };

  /* =======================================================
     MULTI JOB ANALYSIS
  ======================================================= */

  const handleMultiJobAnalyze =
    async () => {
      setMultiJobError("");

      setMultiJobResult(null);

      const validJobs =
        multiJobs.filter(
          (job) =>
            job.title.trim() &&
            job.description.trim()
        );

      if (validJobs.length < 2) {
        setMultiJobError(
          "Please enter at least 2 complete job descriptions."
        );

        return;
      }

      if (!resume) {
        setMultiJobError(
          "Please upload your resume first."
        );

        return;
      }

      try {
        setMultiJobLoading(true);

        const formData =
          new FormData();

        formData.append(
          "file",
          resume
        );

        formData.append(
          "request",
          JSON.stringify({
            jobs: validJobs,
          })
        );

        const response =
          await fetch(
            `${API_URL}/analyze-multiple-jobs`,
            {
              method: "POST",
              body: formData,
            }
          );

        const data: MultiJobResponse =
          await response.json();

        if (
          !response.ok ||
          !data.success
        ) {
          throw new Error(
            data.message ||
            "Multi-job analysis failed."
          );
        }

        setMultiJobResult(data);
      } catch (err) {
        setMultiJobError(
          err instanceof Error
            ? err.message
            : "Unable to connect to the backend."
        );
      } finally {
        setMultiJobLoading(false);
      }
    };

  /* =======================================================
     RENDER
  ======================================================= */

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-12 text-white">
      <div className="mx-auto max-w-5xl">

        {/* =================================================
            HEADER
        ================================================= */}

        <div className="mb-10">
          <p className="mb-3 text-sm font-medium text-blue-400">
            AI / NLP PROJECT
          </p>

          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
            AI Job Skill-Gap Analyzer
          </h1>

          <p className="mt-4 max-w-2xl text-slate-400">
            Compare your resume with job descriptions,
            identify demonstrated skills, find missing
            skills, and discover skills repeatedly requested
            across multiple jobs.
          </p>
        </div>

        {/* =================================================
            SINGLE JOB ANALYZER
        ================================================= */}

        <form
          onSubmit={handleAnalyze}
          className="grid gap-6 lg:grid-cols-2"
        >

          {/* Resume */}
          <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <h2 className="text-xl font-semibold">
              1. Upload Resume
            </h2>

            <p className="mt-2 text-sm text-slate-400">
              Upload your PDF or DOCX resume.
            </p>

            <label className="mt-6 flex min-h-40 cursor-pointer flex-col items-center justify-center rounded-xl border border-dashed border-slate-700 bg-slate-950 p-6 text-center transition hover:border-blue-500">

              <input
                type="file"
                accept=".pdf,.docx"
                onChange={
                  handleResumeChange
                }
                className="hidden"
              />

              <span className="text-4xl">
                📄
              </span>

              <span className="mt-3 font-medium">
                {resume
                  ? resume.name
                  : "Choose resume"}
              </span>

              <span className="mt-1 text-sm text-slate-500">
                PDF or DOCX
              </span>

            </label>
          </section>

          {/* Job */}
          <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

            <h2 className="text-xl font-semibold">
              2. Add Job
            </h2>

            <p className="mt-2 text-sm text-slate-400">
              Enter the target role and job description.
            </p>

            <input
              value={jobTitle}
              onChange={(event) =>
                setJobTitle(
                  event.target.value
                )
              }
              placeholder="Job title"
              className="mt-6 w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 outline-none transition focus:border-blue-500"
            />

            <textarea
              value={jobDescription}
              onChange={(event) =>
                setJobDescription(
                  event.target.value
                )
              }
              placeholder="Paste job description here..."
              rows={9}
              className="mt-4 w-full resize-none rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 outline-none transition focus:border-blue-500"
            />

          </section>

          {/* Analyze */}
          <section className="lg:col-span-2">

            {error && (
              <div className="mb-4 rounded-xl border border-red-900 bg-red-950/40 px-4 py-3 text-sm text-red-300">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-xl bg-blue-600 px-6 py-4 font-semibold transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading
                ? "Analyzing..."
                : "Analyze Job"}
            </button>

          </section>

        </form>

        {/* =================================================
            SINGLE JOB RESULTS
        ================================================= */}

        {result?.success &&
          result.analysis && (
            <section className="mt-8 space-y-6">

              {/* Overview */}
              <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

                <div className="grid gap-6 lg:grid-cols-3">

                  {/* Coverage */}
                  <div className="rounded-xl bg-slate-950 p-5">

                    <p className="text-sm text-slate-400">
                      Skill Coverage
                    </p>

                    <p className="mt-2 text-5xl font-bold">
                      {
                        result.analysis
                          .coverage_score
                      }%
                    </p>

                    <div className="mt-5">
                      <div className="h-3 w-full overflow-hidden rounded-full bg-slate-800">

                        <div
                          className="h-full rounded-full bg-blue-500 transition-all duration-700"
                          style={{
                            width: `${Math.min(
                              Math.max(
                                result.analysis
                                  .coverage_score,
                                0
                              ),
                              100
                            )}%`,
                          }}
                        />

                      </div>

                      <div className="mt-2 flex justify-between text-xs text-slate-500">
                        <span>
                          0%
                        </span>

                        <span>
                          100%
                        </span>
                      </div>
                    </div>

                    <p className="mt-2 text-sm text-slate-500">
                      Based on detected job requirements
                    </p>

                  </div>

                  {/* Resume */}
                  <div className="rounded-xl bg-slate-950 p-5">

                    <p className="text-sm text-slate-400">
                      Resume
                    </p>

                    <p className="mt-2 truncate font-medium">
                      {
                        result.resume
                          ?.filename
                      }
                    </p>

                    <p className="mt-2 text-sm text-slate-500">
                      {
                        result.resume
                          ?.skills
                          .length ?? 0
                      }{" "}
                      skills detected
                    </p>

                  </div>

                  {/* Job */}
                  <div className="rounded-xl bg-slate-950 p-5">

                    <p className="text-sm text-slate-400">
                      Target Job
                    </p>

                    <p className="mt-2 truncate font-medium">
                      {
                        result.job
                          ?.title
                      }
                    </p>

                    <p className="mt-2 text-sm text-slate-500">
                      {
                        result.analysis
                          .total_requirements
                      }{" "}
                      requirements detected
                    </p>

                  </div>

                </div>

                {/* Status counts */}
                <div className="mt-6 grid grid-cols-3 gap-3">

                  <div className="rounded-xl border border-slate-800 p-4">

                    <p className="text-2xl font-bold text-emerald-400">
                      {
                        result.analysis
                          .matched_count
                      }
                    </p>

                    <p className="text-sm text-slate-400">
                      Matched
                    </p>

                  </div>

                  <div className="rounded-xl border border-slate-800 p-4">

                    <p className="text-2xl font-bold text-amber-400">
                      {
                        result.analysis
                          .partial_count
                      }
                    </p>

                    <p className="text-sm text-slate-400">
                      Partial
                    </p>

                  </div>

                  <div className="rounded-xl border border-slate-800 p-4">

                    <p className="text-2xl font-bold text-red-400">
                      {
                        result.analysis
                          .missing_count
                      }
                    </p>

                    <p className="text-sm text-slate-400">
                      Missing
                    </p>

                  </div>

                </div>
              </div>

              {/* Required / Preferred */}
              <div className="grid gap-4 sm:grid-cols-2">

                <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">

                  <p className="text-sm text-slate-400">
                    Required Skills
                  </p>

                  <p className="mt-2 text-3xl font-bold">
                    {requiredSkillCount}
                  </p>

                  <p className="mt-1 text-sm text-slate-500">
                    Skills explicitly required by the job
                  </p>

                </div>

                <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">

                  <p className="text-sm text-slate-400">
                    Preferred Skills
                  </p>

                  <p className="mt-2 text-3xl font-bold">
                    {preferredSkillCount}
                  </p>

                  <p className="mt-1 text-sm text-slate-500">
                    Skills listed as preferred or desirable
                  </p>

                </div>

              </div>

              {/* Matched */}
              <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

                <h2 className="text-xl font-semibold text-emerald-400">
                  Matched Skills
                </h2>

                <div className="mt-4 space-y-3">

                  {result.analysis.matched
                    .length > 0 ? (
                    result.analysis.matched.map(
                      (item) => (
                        <div
                          key={item.skill}
                          className="rounded-xl border border-slate-800 bg-slate-950 p-4"
                        >

                          <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">

                            <div>

                              <p className="font-medium text-emerald-300">
                                ✓ {item.skill}
                              </p>

                              <p className="mt-1 text-xs text-slate-500">
                                {
                                  item.category
                                }
                              </p>

                            </div>

                            <span className="w-fit rounded-full bg-slate-900 px-3 py-1 text-xs text-slate-400">
                              {
                                item.requirement_type
                              }
                            </span>

                          </div>

                          {item.matched_candidate_skill && (
                            <p className="mt-3 text-sm text-slate-400">
                              Resume skill:{" "}
                              <span className="text-slate-200">
                                {
                                  item.matched_candidate_skill
                                }
                              </span>
                            </p>
                          )}

                          {item.candidate_sections
                            .length > 0 && (
                              <p className="mt-2 text-sm text-slate-400">
                                Found in:{" "}
                                <span className="text-slate-200">
                                  {item.candidate_sections.join(
                                    ", "
                                  )}
                                </span>
                              </p>
                            )}

                          {item.candidate_evidence
                            .length > 0 && (
                              <div className="mt-3 rounded-lg border border-slate-800 bg-slate-900 p-3">

                                <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                                  Evidence from resume
                                </p>

                                <p className="mt-2 text-sm leading-6 text-slate-300">
                                  "
                                  {
                                    item
                                      .candidate_evidence[0]
                                  }
                                  "
                                </p>

                              </div>
                            )}

                        </div>
                      )
                    )
                  ) : (
                    <p className="text-sm text-slate-500">
                      No matched skills found.
                    </p>
                  )}

                </div>

              </div>

              {/* Partial */}
              <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

                <h2 className="text-xl font-semibold text-amber-400">
                  Partial Skills
                </h2>

                <div className="mt-4 space-y-3">

                  {result.analysis.partial
                    .length > 0 ? (
                    result.analysis.partial.map(
                      (item) => (
                        <div
                          key={item.skill}
                          className="rounded-xl border border-slate-800 bg-slate-950 p-4"
                        >

                          <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">

                            <div>

                              <p className="font-medium text-amber-300">
                                ◐ {item.skill}
                              </p>

                              <p className="mt-1 text-xs text-slate-500">
                                {
                                  item.category
                                }
                              </p>

                            </div>

                            <div className="flex items-center gap-2">

                              <span className="rounded-full bg-slate-900 px-3 py-1 text-xs text-slate-400">
                                {
                                  item.requirement_type
                                }
                              </span>

                              <span className="rounded-full bg-slate-900 px-3 py-1 text-xs text-amber-300">
                                {item.similarity_score.toFixed(
                                  2
                                )}
                              </span>

                            </div>

                          </div>

                          {item.matched_candidate_skill && (
                            <p className="mt-3 text-sm text-slate-400">
                              Closest resume skill:{" "}
                              <span className="text-slate-200">
                                {
                                  item.matched_candidate_skill
                                }
                              </span>
                            </p>
                          )}

                          {item.candidate_sections
                            .length > 0 && (
                              <p className="mt-2 text-sm text-slate-400">
                                Found in:{" "}
                                <span className="text-slate-200">
                                  {item.candidate_sections.join(
                                    ", "
                                  )}
                                </span>
                              </p>
                            )}

                          {item.candidate_evidence
                            .length > 0 && (
                              <div className="mt-3 rounded-lg border border-slate-800 bg-slate-900 p-3">

                                <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                                  Evidence from resume
                                </p>

                                <p className="mt-2 text-sm leading-6 text-slate-300">
                                  "
                                  {
                                    item
                                      .candidate_evidence[0]
                                  }
                                  "
                                </p>

                              </div>
                            )}

                        </div>
                      )
                    )
                  ) : (
                    <p className="text-sm text-slate-500">
                      No partial skills found.
                    </p>
                  )}

                </div>

              </div>

              {/* Missing */}
              <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

                <h2 className="text-xl font-semibold text-red-400">
                  Missing Skills
                </h2>

                <div className="mt-4 space-y-3">

                  {result.analysis.missing
                    .length > 0 ? (
                    result.analysis.missing.map(
                      (item) => (
                        <div
                          key={item.skill}
                          className="rounded-xl border border-slate-800 bg-slate-950 p-4"
                        >

                          <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">

                            <div>

                              <p className="font-medium text-red-300">
                                ✗ {item.skill}
                              </p>

                              <p className="mt-1 text-xs text-slate-500">
                                {
                                  item.category
                                }
                              </p>

                            </div>

                            <span className="w-fit rounded-full bg-slate-900 px-3 py-1 text-xs text-slate-400">
                              {
                                item.requirement_type
                              }
                            </span>

                          </div>

                          <p className="mt-3 text-sm text-slate-500">
                            No meaningful matching skill was
                            identified in the resume.
                          </p>

                        </div>
                      )
                    )
                  ) : (
                    <p className="text-sm text-slate-500">
                      No missing skills found.
                    </p>
                  )}

                </div>

              </div>

              {/* Score explanation */}
              <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

                <h2 className="text-lg font-semibold">
                  How the score is calculated
                </h2>

                <div className="mt-4 space-y-3 text-sm text-slate-400">

                  <div className="flex items-center justify-between rounded-lg bg-slate-950 p-3">
                    <span>
                      Matched skill
                    </span>

                    <span className="font-medium text-emerald-400">
                      1.0 points
                    </span>
                  </div>

                  <div className="flex items-center justify-between rounded-lg bg-slate-950 p-3">
                    <span>
                      Partial skill
                    </span>

                    <span className="font-medium text-amber-400">
                      0.5 points
                    </span>
                  </div>

                  <div className="flex items-center justify-between rounded-lg bg-slate-950 p-3">
                    <span>
                      Missing skill
                    </span>

                    <span className="font-medium text-red-400">
                      0 points
                    </span>
                  </div>

                </div>

                <p className="mt-4 text-sm leading-6 text-slate-500">
                  Coverage is calculated from the detected job
                  requirements and indicates how much of the
                  skill set is demonstrated by the resume.
                </p>

                <div className="mt-4 rounded-xl border border-slate-800 bg-slate-950 p-4">

                  <p className="text-sm font-medium text-slate-300">
                    Important
                  </p>

                  <p className="mt-1 text-sm leading-6 text-slate-500">
                    This score is a skill-coverage metric. It
                    does not represent a probability of getting
                    hired and does not replace recruiter
                    evaluation.
                  </p>

                </div>

              </div>

            </section>
          )}

        {/* =================================================
            MULTI JOB ANALYSIS
        ================================================= */}

        <section className="mt-12 rounded-2xl border border-slate-800 bg-slate-900 p-6">

          {/* Header */}
          <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">

            <div>

              <p className="text-sm font-medium text-blue-400">
                MULTI-JOB ANALYSIS
              </p>

              <h2 className="mt-1 text-2xl font-bold">
                Find the skills repeatedly demanded
              </h2>

              <p className="mt-2 max-w-2xl text-sm text-slate-400">
                Add multiple target jobs and compare the
                skills employers request across them.
              </p>

            </div>

            <span className="text-sm text-slate-500">
              {multiJobs.length}/10 jobs
            </span>

          </div>

          {/* Job inputs */}
          <div className="mt-6 space-y-4">

            {multiJobs.map(
              (job, index) => (
                <div
                  key={index}
                  className="rounded-xl border border-slate-800 bg-slate-950 p-5"
                >

                  <div className="flex items-center justify-between">

                    <h3 className="font-semibold">
                      Job {index + 1}
                    </h3>

                    {multiJobs.length >
                      1 && (
                        <button
                          type="button"
                          onClick={() =>
                            removeJob(
                              index
                            )
                          }
                          className="text-sm text-red-400 transition hover:text-red-300"
                        >
                          Remove
                        </button>
                      )}

                  </div>

                  <input
                    value={job.title}
                    onChange={(event) =>
                      updateJob(
                        index,
                        "title",
                        event.target.value
                      )
                    }
                    placeholder="Job title"
                    className="mt-4 w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 outline-none transition focus:border-blue-500"
                  />

                  <textarea
                    value={
                      job.description
                    }
                    onChange={(event) =>
                      updateJob(
                        index,
                        "description",
                        event.target.value
                      )
                    }
                    placeholder="Paste job description..."
                    rows={6}
                    className="mt-3 w-full resize-none rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 outline-none transition focus:border-blue-500"
                  />

                </div>
              )
            )}

          </div>

          {/* Buttons */}
          <div className="mt-4 flex flex-col gap-3 sm:flex-row">

            <button
              type="button"
              onClick={addJob}
              disabled={
                multiJobs.length >= 10
              }
              className="rounded-xl border border-slate-700 px-5 py-3 text-sm font-medium transition hover:border-slate-500 disabled:cursor-not-allowed disabled:opacity-40"
            >
              + Add Job
            </button>

            <button
              type="button"
              onClick={
                handleMultiJobAnalyze
              }
              disabled={
                multiJobLoading
              }
              className="rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {multiJobLoading
                ? "Analyzing Jobs..."
                : "Analyze All Jobs"}
            </button>

          </div>

          {/* Error */}
          {multiJobError && (
            <div className="mt-4 rounded-xl border border-red-900 bg-red-950/30 p-4 text-sm text-red-300">
              {multiJobError}
            </div>
          )}

          {/* =================================================
              MULTI JOB RESULTS
          ================================================= */}

          {multiJobResult?.success &&
            multiJobResult.skill_demand && (
              <div className="mt-8">

                {/* Summary */}
                <div className="grid gap-4 sm:grid-cols-2">

                  <div className="rounded-xl border border-slate-800 bg-slate-950 p-5">

                    <p className="text-sm text-slate-400">
                      Jobs analyzed
                    </p>

                    <p className="mt-1 text-3xl font-bold">
                      {
                        multiJobResult.job_count
                      }
                    </p>

                  </div>

                  <div className="rounded-xl border border-slate-800 bg-slate-950 p-5">

                    <p className="text-sm text-slate-400">
                      Skills identified
                    </p>

                    <p className="mt-1 text-3xl font-bold">
                      {
                        multiJobResult
                          .skill_demand
                          .length
                      }
                    </p>

                  </div>

                </div>

                {/* =================================================
                    MOST REQUESTED SKILLS
                ================================================= */}

                <div className="mt-8">

                  <div>

                    <p className="text-sm font-medium text-blue-400">
                      SKILL DEMAND
                    </p>

                    <h3 className="mt-1 text-xl font-semibold">
                      Most Requested Skills
                    </h3>

                    <p className="mt-2 text-sm text-slate-400">
                      Skills appearing most frequently
                      across the jobs you selected.
                    </p>

                  </div>

                  <div className="mt-4 space-y-3">

                    {multiJobResult.skill_demand.map(
                      (item) => (
                        <div
                          key={item.skill}
                          className="rounded-xl border border-slate-800 bg-slate-950 p-4"
                        >

                          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">

                            <div>

                              <p className="font-medium">
                                {item.skill}
                              </p>

                              <p className="mt-1 text-xs text-slate-500">
                                {
                                  item.category
                                }
                              </p>

                            </div>

                            <div className="flex items-center gap-2">

                              <span className="rounded-full bg-slate-900 px-3 py-1 text-xs text-slate-300">
                                {
                                  item.jobs_count
                                }
                                /
                                {
                                  item.total_jobs
                                }{" "}
                                jobs
                              </span>

                              <span className="rounded-full bg-slate-900 px-3 py-1 text-xs text-blue-300">
                                {
                                  item.frequency_percent
                                }%
                              </span>

                            </div>

                          </div>

                          {/* Demand bar */}
                          <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-800">

                            <div
                              className="h-full rounded-full bg-blue-500 transition-all duration-500"
                              style={{
                                width: `${Math.min(
                                  Math.max(
                                    item.frequency_percent,
                                    0
                                  ),
                                  100
                                )}%`,
                              }}
                            />

                          </div>

                          <div className="mt-2 flex flex-col gap-1 text-xs text-slate-500 sm:flex-row sm:justify-between">

                            <span>
                              Appears in{" "}
                              {
                                item.jobs_count
                              }{" "}
                              of{" "}
                              {
                                item.total_jobs
                              }{" "}
                              jobs
                            </span>

                            <span>
                              Required:{" "}
                              {
                                item.required_count
                              }
                              {" · "}
                              Preferred:{" "}
                              {
                                item.preferred_count
                              }
                            </span>

                          </div>

                        </div>
                      )
                    )}

                  </div>

                </div>

                {/* =================================================
                    COMMON SKILL GAPS
                ================================================= */}

                <div className="mt-10">

                  <div>

                    <p className="text-sm font-medium text-red-400">
                      COMMON SKILL GAPS
                    </p>

                    <h3 className="mt-1 text-xl font-semibold">
                      Frequently demanded skills missing from your resume
                    </h3>

                    <p className="mt-2 text-sm text-slate-400">
                      These are skills repeatedly requested
                      across your selected jobs but not detected
                      in your resume.
                    </p>

                  </div>

                  {multiJobResult
                    .common_skill_gaps &&
                    multiJobResult
                      .common_skill_gaps
                      .length > 0 ? (

                    <div className="mt-4 space-y-3">

                      {multiJobResult.common_skill_gaps.map(
                        (item) => (
                          <div
                            key={item.skill}
                            className="rounded-xl border border-red-950/70 bg-slate-950 p-4"
                          >

                            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">

                              <div>

                                <p className="font-medium text-red-300">
                                  ✗ {item.skill}
                                </p>

                                <p className="mt-1 text-xs text-slate-500">
                                  {
                                    item.category
                                  }
                                </p>

                              </div>

                              <div className="flex items-center gap-2">

                                <span className="rounded-full bg-slate-900 px-3 py-1 text-xs text-slate-300">
                                  {
                                    item.jobs_count
                                  }
                                  /
                                  {
                                    item.total_jobs
                                  }{" "}
                                  jobs
                                </span>

                                <span className="rounded-full bg-slate-900 px-3 py-1 text-xs text-red-300">
                                  {
                                    item.frequency_percent
                                  }%
                                </span>

                              </div>

                            </div>

                            <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-800">

                              <div
                                className="h-full rounded-full bg-red-500 transition-all duration-500"
                                style={{
                                  width: `${Math.min(
                                    Math.max(
                                      item.frequency_percent,
                                      0
                                    ),
                                    100
                                  )}%`,
                                }}
                              />

                            </div>

                            <div className="mt-2 text-xs text-slate-500">
                              Required in{" "}
                              {
                                item.required_count
                              }{" "}
                              jobs
                              {" · "}
                              Preferred in{" "}
                              {
                                item.preferred_count
                              }{" "}
                              jobs
                            </div>

                          </div>
                        )
                      )}

                    </div>

                  ) : (

                    <div className="mt-4 rounded-xl border border-slate-800 bg-slate-950 p-5">

                      <p className="text-sm text-slate-400">
                        No common skill gaps were found above
                        the current frequency threshold.
                      </p>

                    </div>

                  )}

                </div>

                {/* =================================================
    LEARNING ROADMAP
================================================= */}

                {multiJobResult.learning_roadmap &&
                  multiJobResult.learning_roadmap.length > 0 && (
                    <div className="mt-10">

                      <div>
                        <p className="text-sm font-medium text-blue-400">
                          LEARNING ROADMAP
                        </p>

                        <h3 className="mt-1 text-xl font-semibold">
                          Recommended learning order
                        </h3>

                        <p className="mt-2 text-sm text-slate-400">
                          Skills are ordered using job demand, requirement
                          importance, and available skill dependencies.
                        </p>
                      </div>

                      <div className="mt-6 space-y-4">

                        {multiJobResult.learning_roadmap.map(
                          (item) => (
                            <div
                              key={item.skill}
                              className="rounded-xl border border-slate-800 bg-slate-950 p-5"
                            >

                              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

                                <div className="flex items-center gap-4">

                                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-blue-600 font-bold">
                                    {item.learning_order}
                                  </div>

                                  <div>
                                    <p className="font-semibold">
                                      {item.skill}
                                    </p>

                                    <p className="mt-1 text-xs text-slate-500">
                                      {item.category}
                                    </p>
                                  </div>

                                </div>

                                <div className="flex items-center gap-2">

                                  <span className="rounded-full bg-slate-900 px-3 py-1 text-xs text-blue-300">
                                    {item.frequency_percent}% demand
                                  </span>

                                  <span className="rounded-full bg-slate-900 px-3 py-1 text-xs text-slate-300">
                                    Priority {item.priority_score}
                                  </span>

                                </div>

                              </div>

                              <div className="mt-4 grid gap-3 sm:grid-cols-3">

                                <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
                                  <p className="text-xs text-slate-500">
                                    Jobs
                                  </p>

                                  <p className="mt-1 font-medium">
                                    {item.jobs_count}/
                                    {item.total_jobs}
                                  </p>
                                </div>

                                <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
                                  <p className="text-xs text-slate-500">
                                    Required
                                  </p>

                                  <p className="mt-1 font-medium">
                                    {item.required_count}
                                  </p>
                                </div>

                                <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
                                  <p className="text-xs text-slate-500">
                                    Preferred
                                  </p>

                                  <p className="mt-1 font-medium">
                                    {item.preferred_count}
                                  </p>
                                </div>

                              </div>

                              {item.dependencies.length > 0 && (
                                <div className="mt-4 rounded-lg border border-slate-800 bg-slate-900 p-4">

                                  <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                                    Prerequisites
                                  </p>

                                  <div className="mt-2 flex flex-wrap gap-2">

                                    {item.dependencies.map(
                                      (dependency) => (
                                        <span
                                          key={dependency}
                                          className="rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-300"
                                        >
                                          {dependency}
                                        </span>
                                      )
                                    )}

                                  </div>

                                </div>
                              )}

                            </div>
                          )
                        )}

                      </div>

                    </div>
                  )}

              </div>
            )}

        </section>

      </div>
    </main>
  );
}