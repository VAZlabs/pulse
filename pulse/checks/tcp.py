"""TCP connection checker"""

import asyncio
import socket
import time

from . import BaseChecker
from ..core.target import Target
from ..core.result import CheckResult, Status
from ..utils.logger import get_logger


logger = get_logger(__name__)


class TCPChecker(BaseChecker):
    """Check TCP connectivity"""

    name = "TCP"

    async def check(self, target: Target) -> CheckResult:
        """Check TCP connection to target"""
        start_time = time.time()

        try:
            loop = asyncio.get_event_loop()

            # Create connection
            sock = await loop.run_in_executor(
                None,
                lambda: socket.create_connection(
                    (target.host, target.port), timeout=self.config.timeout
                ),
            )

            duration = (time.time() - start_time) * 1000
            sock.close()

            # Determine connection quality
            if duration < 50:
                quality = "fast"
            elif duration < 150:
                quality = "good"
            else:
                quality = "slow"

            return CheckResult(
                name=self.name,
                duration_ms=duration,
                status=Status.SUCCESS,
                details=f"Connected ({quality})",
                metadata={
                    "host": target.host,
                    "port": target.port,
                    "quality": quality,
                },
            )

        except socket.timeout:
            duration = (time.time() - start_time) * 1000
            return CheckResult(
                name=self.name,
                duration_ms=duration,
                status=Status.FAILURE,
                details="Connection timeout",
                error=f"Timeout after {self.config.timeout}s",
            )
        except ConnectionRefusedError:
            duration = (time.time() - start_time) * 1000
            return CheckResult(
                name=self.name,
                duration_ms=duration,
                status=Status.FAILURE,
                details="Connection refused",
                error="Port closed or service not running",
            )
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            return CheckResult(
                name=self.name,
                duration_ms=duration,
                status=Status.FAILURE,
                details="Connection failed",
                error=str(e),
            )
