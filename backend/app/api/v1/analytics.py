"""Analytics endpoint -- GET /api/v1/analytics/summary."""

from fastapi import APIRouter, Depends, Query

from app.api.deps import DB, get_current_user
from app.schemas.analytics import AnalyticsSummaryResponse
from app.services.analytics import AnalyticsEngine

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get(
    "/analytics/summary",
    response_model=AnalyticsSummaryResponse,
    status_code=200,
    summary="Aggregate telemetry dashboard summary",
    tags=["Analytics"],
    responses={200: {"description": "Summary returned successfully"}},
)
async def analytics_summary(
    db: DB,
    days: int = Query(30, ge=1, le=365, description="Lookback window in days."),
) -> AnalyticsSummaryResponse:
    engine = AnalyticsEngine(db)
    result = await engine.get_summary(days=days)
    return AnalyticsSummaryResponse(**result)
