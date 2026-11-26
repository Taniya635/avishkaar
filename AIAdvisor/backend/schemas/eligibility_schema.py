
from typing import Literal
from pydantic import BaseModel


class SchemeResult(BaseModel):
    scheme_id: str
    scheme_name: str
    status: Literal["eligible", "ineligible", "pending"]
    reasons: list[str]


class EligibilitySummaryResponse(BaseModel):
    user_id: str

    total_schemes: int
    eligible_count: int
    ineligible_count: int
    pending_count: int

    eligible_schemes: list[SchemeResult]
    ineligible_schemes: list[SchemeResult]
    pending_schemes: list[SchemeResult]
