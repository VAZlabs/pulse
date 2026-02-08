"""Base checker class"""

from abc import ABC, abstractmethod
from typing import Any

from ..core.target import Target
from ..core.result import CheckResult


class BaseChecker(ABC):
    """Base class for all checkers"""

    name = "base"

    def __init__(self, config: Any):
        self.config = config

    @abstractmethod
    async def check(self, target: Target) -> CheckResult:
        """Perform the check and return result"""
        pass

    def _format_duration(self, duration_ms: float) -> str:
        """Format duration for display"""
        if duration_ms < 1:
            return f"{duration_ms:.3f} ms"
        elif duration_ms < 100:
            return f"{duration_ms:.1f} ms"
        else:
            return f"{duration_ms:.0f} ms"
