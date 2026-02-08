"""Async engine for running network checks"""

import asyncio
from typing import List, Optional, Dict, Any, Callable
from concurrent.futures import ThreadPoolExecutor
import time

from .config import Config
from .target import Target
from .result import CheckResult, TargetResult, BenchmarkResult, Status
from ..checks.dns import DNSChecker
from ..checks.tcp import TCPChecker
from ..checks.tls import TLSChecker
from ..checks.http import HTTPChecker
from ..utils.logger import get_logger


logger = get_logger(__name__)


class PulseEngine:
    """Main engine for running network diagnostics"""

    CHECKERS = {
        "dns": DNSChecker,
        "tcp": TCPChecker,
        "tls": TLSChecker,
        "http": HTTPChecker,
    }

    def __init__(self, config: Config):
        self.config = config
        self._executor = ThreadPoolExecutor(max_workers=config.workers)
        self._checkers: Dict[str, Any] = {}
        self._init_checkers()

    def _init_checkers(self):
        """Initialize checkers based on config"""
        for check_name in self.config.checks:
            if check_name in self.CHECKERS:
                self._checkers[check_name] = self.CHECKERS[check_name](self.config)
            else:
                logger.warning(f"Unknown check: {check_name}")

    async def check_target(self, target: Target) -> TargetResult:
        """Run all checks for a single target"""
        logger.debug(f"Checking target: {target}")

        checks = []
        start_time = time.time()

        # Run checks sequentially for a single target
        for check_name in self.config.checks:
            if check_name not in self._checkers:
                continue

            checker = self._checkers[check_name]

            # Skip TLS for non-TLS targets
            if check_name == "tls" and not target.use_tls:
                checks.append(
                    CheckResult(
                        name="TLS",
                        duration_ms=0,
                        status=Status.SKIPPED,
                        details="Skipped (non-TLS target)",
                    )
                )
                continue

            # Run check with retries
            result = await self._run_check_with_retries(checker, target)
            checks.append(result)

            # If check failed and it's critical, stop early
            if result.is_failure and check_name in ["dns", "tcp"]:
                logger.debug(f"Critical check {check_name} failed, stopping early")
                break

        total_duration = (time.time() - start_time) * 1000

        return TargetResult(
            target=target, checks=checks, total_duration_ms=total_duration
        )

    async def _run_check_with_retries(self, checker, target: Target) -> CheckResult:
        """Run a check with retry logic"""
        last_result: CheckResult = CheckResult(
            name=checker.name, duration_ms=0, status=Status.FAILURE, error="No result"
        )

        for attempt in range(self.config.retries):
            try:
                result = await checker.check(target)
                if result.is_success:
                    return result
                last_result = result
            except Exception as e:
                logger.debug(f"Check attempt {attempt + 1} failed: {e}")
                last_result = CheckResult(
                    name=checker.name,
                    duration_ms=0,
                    status=Status.FAILURE,
                    error=str(e),
                )

            if attempt < self.config.retries - 1:
                await asyncio.sleep(0.5 * (attempt + 1))  # Exponential backoff

        return last_result

    async def check_targets(self, targets: List[Target]) -> List[TargetResult]:
        """Run checks for multiple targets concurrently"""
        semaphore = asyncio.Semaphore(self.config.workers)

        async def check_with_limit(target: Target) -> TargetResult:
            async with semaphore:
                return await self.check_target(target)

        tasks = [check_with_limit(t) for t in targets]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions
        valid_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error checking {targets[i]}: {result}")
                valid_results.append(
                    TargetResult(
                        target=targets[i],
                        checks=[
                            CheckResult(
                                name="ERROR",
                                duration_ms=0,
                                status=Status.FAILURE,
                                error=str(result),
                            )
                        ],
                    )
                )
            else:
                valid_results.append(result)

        return valid_results

    async def benchmark(self, target: Target, iterations: int = 10) -> BenchmarkResult:
        """Run benchmark mode with multiple iterations"""
        logger.info(f"Running benchmark for {target} ({iterations} iterations)")

        results = []
        for i in range(iterations):
            logger.debug(f"Benchmark iteration {i + 1}/{iterations}")
            result = await self.check_target(target)
            results.append(result)

        return BenchmarkResult(target=target, iterations=iterations, results=results)

    async def compare_targets(self, targets: List[Target]) -> List[TargetResult]:
        """Compare multiple targets side by side"""
        logger.info(f"Comparing {len(targets)} targets")
        return await self.check_targets(targets)

    async def close(self):
        """Cleanup resources"""
        self._executor.shutdown(wait=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        asyncio.run(self.close())
