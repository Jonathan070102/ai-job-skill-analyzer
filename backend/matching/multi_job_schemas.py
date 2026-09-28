from pydantic import BaseModel, Field


class JobInput(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)


class MultiJobRequest(BaseModel):
    jobs: list[JobInput] = Field(..., min_length=1, max_length=10)