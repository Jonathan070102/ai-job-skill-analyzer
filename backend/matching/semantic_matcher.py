from functools import lru_cache

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    """
    Load and cache the local sentence-transformer model.
    """
    return SentenceTransformer(MODEL_NAME)


def build_skill_text(skill: dict) -> str:
    """
    Build a richer text representation of a skill using
    its canonical name and available evidence.
    """

    skill_name = skill.get("skill", "")

    evidence = skill.get("evidence", [])

    if isinstance(evidence, list):
        evidence_text = " ".join(evidence)
    else:
        evidence_text = str(evidence)

    if evidence_text:
        return f"{skill_name}. {evidence_text}"

    return skill_name


def calculate_similarity(
    candidate_skill: dict,
    job_skill: dict
) -> float:
    """
    Calculate semantic similarity between a candidate skill
    and a job requirement.
    """

    model = get_model()

    candidate_text = build_skill_text(candidate_skill)
    job_text = build_skill_text(job_skill)

    embeddings = model.encode(
        [candidate_text, job_text],
        convert_to_tensor=True,
        normalize_embeddings=True
    )

    similarity = cos_sim(
        embeddings[0],
        embeddings[1]
    ).item()

    return round(float(similarity), 4)