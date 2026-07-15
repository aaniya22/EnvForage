from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.diagnostic import DiagnosticReport, VerificationCheck, VerificationResult


class AnalyticsEngine:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_summary(self, days: int = 30) -> dict[str, Any]:
        since = datetime.utcnow() - timedelta(days=days)

        os_counts = await self.db.execute(
            select(DiagnosticReport.os_type, func.count())
            .where(DiagnosticReport.created_at >= since)
            .group_by(DiagnosticReport.os_type)
        )
        gpu_counts = await self.db.execute(
            select(DiagnosticReport.gpu_name, func.count())
            .where(DiagnosticReport.created_at >= since)
            .group_by(DiagnosticReport.gpu_name)
        )
        status_counts = await self.db.execute(
            select(VerificationResult.overall_status, func.count())
            .where(VerificationResult.created_at >= since)
            .group_by(VerificationResult.overall_status)
        )
        check_failures = await self.db.execute(
            select(VerificationCheck.check_name, func.count())
            .where(VerificationCheck.passed.is_(False))
            .group_by(VerificationCheck.check_name)
            .order_by(func.count().desc())
            .limit(10)
        )

        return {
            "os_breakdown": dict(os_counts.all()),
            "gpu_breakdown": dict(gpu_counts.all()),
            "status_breakdown": dict(status_counts.all()),
            "top_failing_checks": dict(check_failures.all()),
            "period_days": days,
        }
