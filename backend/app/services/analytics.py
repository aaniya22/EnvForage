from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.diagnostic import DiagnosticReport, VerificationCheck


def _gpu_vendor(gpu_name: str | None) -> str:
    if not gpu_name:
        return "No GPU"
    name = gpu_name.lower()
    if "nvidia" in name:
        return "NVIDIA"
    if "amd" in name:
        return "AMD"
    if "intel" in name:
        return "Intel"
    return "Other"


class AnalyticsEngine:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_summary(self) -> dict[str, Any]:
        gpu_rows = await self.db.execute(select(DiagnosticReport.gpu_name))
        gpu_distribution: dict[str, int] = {}
        for (gpu_name,) in gpu_rows.all():
            vendor = _gpu_vendor(gpu_name)
            gpu_distribution[vendor] = gpu_distribution.get(vendor, 0) + 1

        python_counts = await self.db.execute(
            select(DiagnosticReport.python_version, func.count())
            .group_by(DiagnosticReport.python_version)
        )
        python_version_histogram = {
            (v or "unknown"): c for v, c in python_counts.all()
        }

        cuda_gpu_counts = await self.db.execute(
            select(
                DiagnosticReport.cuda_version,
                DiagnosticReport.gpu_name,
                func.count(),
            )
            .where(DiagnosticReport.cuda_version.is_not(None))
            .group_by(DiagnosticReport.cuda_version, DiagnosticReport.gpu_name)
        )
        cuda_version_heatmap = [
            {"cuda_version": cv, "gpu_name": gn or "unknown", "count": c}
            for cv, gn, c in cuda_gpu_counts.all()
        ]

        os_counts = await self.db.execute(
            select(DiagnosticReport.os_type, func.count())
            .group_by(DiagnosticReport.os_type)
        )
        os_distribution = {(o or "unknown"): c for o, c in os_counts.all()}

        failure_counts = await self.db.execute(
            select(VerificationCheck.check_name, func.count())
            .where(VerificationCheck.passed.is_(False))
            .group_by(VerificationCheck.check_name)
            .order_by(func.count().desc())
            .limit(10)
        )
        common_failures = dict(failure_counts.all())

        return {
            "gpu_distribution": gpu_distribution,
            "python_version_histogram": python_version_histogram,
            "cuda_version_heatmap": cuda_version_heatmap,
            "os_distribution": os_distribution,
            "common_failures": common_failures,
        }
