from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class MonitoringResult:
    source: str
    success: bool
    data: Any = None
    error: str | None = None


def run_with_fallback(
    brand24_function: Callable[[], Any],
    custom_function: Callable[[], Any],
) -> MonitoringResult:

    try:
        result = brand24_function()

        return MonitoringResult(
            source="Brand24",
            success=True,
            data=result,
        )

    except Exception as brand24_error:

        try:
            result = custom_function()

            return MonitoringResult(
                source="Custom EWS",
                success=True,
                data=result,
                error=f"Brand24 failed: {brand24_error}",
            )

        except Exception as custom_error:

            return MonitoringResult(
                source="Unavailable",
                success=False,
                data=None,
                error=(
                    f"Brand24 failed: {brand24_error}; "
                    f"Custom EWS failed: {custom_error}"
                ),
            )
