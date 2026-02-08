"""Result classes for pulse checks"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class Status(Enum):
    """Check status enumeration"""

    SUCCESS = "success"
    WARNING = "warning"
    FAILURE = "failure"
    SKIPPED = "skipped"


@dataclass
class CheckResult:
    """Result of a single check"""

    name: str
    duration_ms: float
    status: Status
    details: str = ""
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def is_success(self) -> bool:
        return self.status == Status.SUCCESS

    @property
    def is_warning(self) -> bool:
        return self.status == Status.WARNING

    @property
    def is_failure(self) -> bool:
        return self.status == Status.FAILURE

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "duration_ms": round(self.duration_ms, 2),
            "status": self.status.value,
            "details": self.details,
            "error": self.error,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class TargetResult:
    """Result of checking a target"""

    target: Any  # Target object
    checks: List[CheckResult] = field(default_factory=list)
    total_duration_ms: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.total_duration_ms and self.checks:
            self.total_duration_ms = sum(c.duration_ms for c in self.checks)

    @property
    def has_failures(self) -> bool:
        return any(c.is_failure for c in self.checks)

    @property
    def has_warnings(self) -> bool:
        return any(c.is_warning for c in self.checks)

    @property
    def is_healthy(self) -> bool:
        return all(c.is_success for c in self.checks)

    @property
    def success_count(self) -> int:
        return sum(1 for c in self.checks if c.is_success)

    @property
    def warning_count(self) -> int:
        return sum(1 for c in self.checks if c.is_warning)

    @property
    def failure_count(self) -> int:
        return sum(1 for c in self.checks if c.is_failure)

    def get_check(self, name: str) -> Optional[CheckResult]:
        """Get check by name"""
        for check in self.checks:
            if check.name == name:
                return check
        return None

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "target": str(self.target),
            "address": self.target.address,
            "checks": [c.to_dict() for c in self.checks],
            "total_duration_ms": round(self.total_duration_ms, 2),
            "is_healthy": self.is_healthy,
            "has_failures": self.has_failures,
            "has_warnings": self.has_warnings,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class BenchmarkResult:
    """Result of benchmark runs"""

    target: Any
    iterations: int
    results: List[TargetResult] = field(default_factory=list)

    @property
    def avg_duration_ms(self) -> float:
        if not self.results:
            return 0.0
        return sum(r.total_duration_ms for r in self.results) / len(self.results)

    @property
    def min_duration_ms(self) -> float:
        if not self.results:
            return 0.0
        return min(r.total_duration_ms for r in self.results)

    @property
    def max_duration_ms(self) -> float:
        if not self.results:
            return 0.0
        return max(r.total_duration_ms for r in self.results)

    @property
    def success_rate(self) -> float:
        if not self.results:
            return 0.0
        healthy = sum(1 for r in self.results if r.is_healthy)
        return (healthy / len(self.results)) * 100

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "target": str(self.target),
            "iterations": self.iterations,
            "avg_duration_ms": round(self.avg_duration_ms, 2),
            "min_duration_ms": round(self.min_duration_ms, 2),
            "max_duration_ms": round(self.max_duration_ms, 2),
            "success_rate": round(self.success_rate, 2),
            "runs": [r.to_dict() for r in self.results],
        }
