"""Apple Silicon detection module."""

from __future__ import annotations

import json
import logging
import platform
import subprocess

logger = logging.getLogger(__name__)


def is_apple_silicon() -> bool:
    """Return True if running on macOS with an Apple Silicon (arm64) chip."""
    return platform.system() == "Darwin" and platform.machine() == "arm64"


def detect_chip_model(timeout: int = 10) -> str | None:
    """Detect the Apple Silicon chip model (e.g. 'Apple M2 Pro')."""
    if not is_apple_silicon():
        return None
    try:
        result = subprocess.run(
            ["sysctl", "-n", "machdep.cpu.brand_string"],
            capture_output=True, text=True, timeout=timeout,
        )
    except (FileNotFoundError, subprocess.SubprocessError, OSError):
        return None
    if result.returncode != 0:
        return None
    brand = result.stdout.strip()
    return brand or None


def detect_unified_memory_gb(timeout: int = 10) -> float | None:
    """Detect total unified memory in GB via sysctl hw.memsize."""
    if not is_apple_silicon():
        return None
    try:
        result = subprocess.run(
            ["sysctl", "-n", "hw.memsize"],
            capture_output=True, text=True, timeout=timeout,
        )
    except (FileNotFoundError, subprocess.SubprocessError, OSError):
        return None
    if result.returncode != 0:
        return None
    try:
        total_bytes = int(result.stdout.strip())
        return round(total_bytes / (1024**3), 2)
    except (ValueError, TypeError):
        return None


def detect_gpu_info(timeout: int = 30) -> tuple[str | None, int | None, bool]:
    """Detect integrated GPU name, core count, and Metal support."""
    if not is_apple_silicon():
        return None, None, False
    try:
        result = subprocess.run(
            ["system_profiler", "SPDisplaysDataType", "-json"],
            capture_output=True, text=True, timeout=timeout,
        )
    except (FileNotFoundError, subprocess.SubprocessError, OSError):
        return None, None, False
    if result.returncode != 0:
        return None, None, False
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None, None, False
    displays = data.get("SPDisplaysDataType") or []
    if not displays:
        return None, None, False
    gpu = displays[0]
    name = gpu.get("sppci_model") or gpu.get("_name")
    gpu_cores: int | None = None
    cores_raw = gpu.get("sppci_cores")
    if cores_raw:
        try:
            gpu_cores = int(str(cores_raw).strip())
        except (ValueError, TypeError):
            gpu_cores = None
    metal_supported = bool(
        gpu.get("spdisplays_mtlgpufamilysupport") or gpu.get("sppci_metal")
    )
    return name, gpu_cores, metal_supported
