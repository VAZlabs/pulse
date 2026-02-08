"""DNS resolution checker"""

import asyncio
import socket
import time
from typing import List, Optional

from . import BaseChecker
from ..core.target import Target
from ..core.result import CheckResult, Status
from ..utils.logger import get_logger


logger = get_logger(__name__)


class DNSChecker(BaseChecker):
    """Check DNS resolution"""

    name = "DNS"

    async def check(self, target: Target) -> CheckResult:
        """Resolve DNS for target"""
        start_time = time.time()

        try:
            # Try to get all address info (IPv4 and IPv6)
            loop = asyncio.get_event_loop()

            # Get address info asynchronously
            addrs = await loop.run_in_executor(
                None,
                lambda: socket.getaddrinfo(
                    target.host,
                    None,
                    socket.AF_UNSPEC,  # Allow both IPv4 and IPv6
                    socket.SOCK_STREAM,
                ),
            )

            duration = (time.time() - start_time) * 1000

            if not addrs:
                return CheckResult(
                    name=self.name,
                    duration_ms=duration,
                    status=Status.FAILURE,
                    details="No DNS records found",
                    error="Empty DNS response",
                )

            # Extract unique IPs
            ips = list(set([addr[4][0] for addr in addrs]))

            # Determine IP version preference
            ipv4_ips = [str(ip) for ip in ips if "." in str(ip)]
            ipv6_ips = [str(ip) for ip in ips if ":" in str(ip)]

            if self.config.prefer_ipv6 and ipv6_ips:
                primary_ip = ipv6_ips[0]
                ip_version = "IPv6"
            elif ipv4_ips:
                primary_ip = ipv4_ips[0]
                ip_version = "IPv4"
            else:
                primary_ip = ips[0]
                ip_version = "IPv6"

            details = f"→ {primary_ip} ({ip_version})"
            if len(ips) > 1:
                details += f" +{len(ips) - 1} more"

            return CheckResult(
                name=self.name,
                duration_ms=duration,
                status=Status.SUCCESS,
                details=details,
                metadata={
                    "ips": ips,
                    "ipv4_count": len(ipv4_ips),
                    "ipv6_count": len(ipv6_ips),
                    "primary_ip": primary_ip,
                },
            )

        except socket.gaierror as e:
            duration = (time.time() - start_time) * 1000
            return CheckResult(
                name=self.name,
                duration_ms=duration,
                status=Status.FAILURE,
                details="DNS resolution failed",
                error=f"DNS error: {e}",
            )
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            return CheckResult(
                name=self.name,
                duration_ms=duration,
                status=Status.FAILURE,
                details="DNS check error",
                error=str(e),
            )

    async def get_dns_records(self, host: str, record_type: str = "A") -> List[str]:
        """Get specific DNS records"""
        try:
            import dns.resolver

            resolver = dns.resolver.Resolver()
            answers = resolver.resolve(host, record_type)
            return [str(rdata) for rdata in answers]
        except ImportError:
            logger.debug("dnspython not available for advanced DNS checks")
            return []
        except Exception as e:
            logger.debug(f"DNS query failed: {e}")
            return []
