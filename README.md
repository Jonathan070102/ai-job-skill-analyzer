\# AI Job Skill-Gap Analyzer



An AI-based web application that compares a candidate's resume with job descriptions to identify matched, partially matched, and missing skills.



The system also analyzes multiple job descriptions to find commonly requested skills and generates a learning roadmap based on recurring skill gaps.



\## Problem



Students and job seekers often struggle to understand:



\- Which skills they already have

\- Which skills a job requires

\- Which skills are missing

\- Which skills should be learned first



This project provides an evidence-based skill gap analysis instead of simply comparing keywords.



\## Features



\### Resume Analysis

\- Upload PDF or DOCX resume

\- Extract resume text

\- Detect resume sections

\- Extract technical and soft skills

\- Normalize skill aliases and duplicates

\- Show evidence from the resume



\### Job Description Analysis

\- Enter a job title and description

\- Extract required and preferred skills

\- Normalize different skill representations

\- Classify requirements as required or preferred



\### Skill Matching

\- Exact skill matching

\- Semantic similarity using Sentence Transformers

\- Related-skill detection

\- Match classification:

&#x20; - Matched

&#x20; - Partial

&#x20; - Missing



\### Skill Gap Analysis

\- Overall skill coverage score

\- Matched skill count

\- Partial skill count

\- Missing skill count

\- Resume evidence for matched skills



\### Multiple Job Analysis

\- Analyze multiple job descriptions

\- Find frequently requested skills

\- Identify common skill gaps

\- Separate required and preferred demand

\- Generate a learning roadmap



\### Learning Roadmap

\- Calculate skill priority

\- Consider job frequency

\- Consider required vs preferred demand

\- Consider skill dependencies

\- Generate an ordered learning sequence



\## Technology Stack



\### Frontend

\- Next.js

\- React

\- TypeScript

\- Tailwind CSS



\### Backend

\- Python

\- FastAPI

\- Pydantic



\### NLP / Machine Learning

\- Sentence Transformers

\- `all-MiniLM-L6-v2`

\- Scikit-learn



\### Document Processing

\- PyPDF

\- python-docx



\## System Architecture



```text

Resume PDF/DOCX

&#x20;     |

&#x20;     v

Document Parser

&#x20;     |

&#x20;     v

Text Cleaner

&#x20;     |

&#x20;     v

Section Detector

&#x20;     |

&#x20;     v

Skill Extractor

&#x20;     |

&#x20;     v

Skill Normalizer

&#x20;     |

&#x20;     +--------------------+

&#x20;     |                    |

&#x20;     v                    v

Candidate Skills     Job Description

&#x20;                          |

&#x20;                          v

&#x20;                 Job Skill Extractor

&#x20;                          |

&#x20;                          v

&#x20;                Requirement Classifier

&#x20;                          |

&#x20;                          v

&#x20;                   Skill Matcher

&#x20;                          |

&#x20;                          v

&#x20;                 Gap Analyzer

&#x20;                          |

&#x20;             +------------+------------+

&#x20;             |                         |

&#x20;             v                         v

&#x20;      Single Job Result        Multiple Job Analyzer

&#x20;                                       |

&#x20;                                       v

&#x20;                             Common Gap Analyzer

&#x20;                                       |

&#x20;                                       v

&#x20;                              Roadmap Generator

