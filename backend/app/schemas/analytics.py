"""Pydantic schemas for the analytics summary endpoint."""

from pydantic import BaseModel, Field


class AnalyticsSummaryResponse(BaseModel):
    os_breakdown: dict[str, int] = Field(..., description="Report count per OS type.")
    gpu_breakdown: dict[str, int] = Field(..., description="Report count per GPU name.")
    status_breakdown: dict[str, int] = Field(
        ..., description="Verification result count per overall_status."
    )
    top_failing_checks: dict[str, int] = Field(
        ..., description="Top 10 most frequently failing check names."
    )
    period_days: int = Field(..., description="Number of days included in this summary.")
