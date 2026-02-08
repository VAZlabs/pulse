"""HTTP/HTTPS checker"""

import asyncio
import http.client
import time
from typing import Dict, Any, Optional
from urllib.parse import urlparse

from . import BaseChecker
from ..core.target import Target
from ..core.result import CheckResult, Status
from ..utils.logger import get_logger


logger = get_logger(__name__)


class HTTPChecker(BaseChecker):
    """Check HTTP/HTTPS connectivity"""

    name = "HTTP"

    # HTTP status categories
    STATUS_CATEGORIES = {
        "success": [200, 201, 202, 204],
        "redirect": [301, 302, 303, 307, 308],
        "client_error": [400, 401, 403, 404, 405, 429],
        "server_error": [500, 502, 503, 504],
    }

    def __init__(self, config):
        super().__init__(config)
        self.redirect_history = []

    async def check(self, target: Target) -> CheckResult:
        """Check HTTP connection"""
        start_time = time.time()
        self.redirect_history = []

        try:
            loop = asyncio.get_event_loop()

            # Build URL
            scheme = "https" if target.use_tls else "http"
            url = f"{scheme}://{target.host}:{target.port}{target.path}"

            # Make HTTP request
            def do_http_check():
                if target.use_tls:
                    conn = http.client.HTTPSConnection(
                        target.host, target.port, timeout=self.config.timeout
                    )
                else:
                    conn = http.client.HTTPConnection(
                        target.host, target.port, timeout=self.config.timeout
                    )

                try:
                    headers = {
                        "User-Agent": "pulse-network-diagnostics/2.0",
                        "Accept": "*/*",
                        "Accept-Encoding": "identity",
                        "Connection": "close",
                    }

                    conn.request("GET", target.path, headers=headers)
                    response = conn.getresponse()

                    result = {
                        "status": response.status,
                        "reason": response.reason,
                        "headers": dict(response.headers),
                        "body_length": len(response.read()),
                    }

                    # Check for redirects
                    if self.config.follow_redirects and response.status in [
                        301,
                        302,
                        307,
                        308,
                    ]:
                        location = response.getheader("Location")
                        if location:
                            result["redirect"] = location

                    return result

                finally:
                    conn.close()

            http_info = await loop.run_in_executor(None, do_http_check)
            duration = (time.time() - start_time) * 1000

            status_code = http_info["status"]
            reason = http_info["reason"]

            # Determine status
            if status_code in self.STATUS_CATEGORIES["success"]:
                check_status = Status.SUCCESS
                details = f"→ GET {target.path} → {status_code} {reason}"
            elif status_code in self.STATUS_CATEGORIES["redirect"]:
                check_status = Status.SUCCESS
                details = f"→ GET {target.path} → {status_code} {reason}"
                if http_info.get("redirect"):
                    details += f" → {http_info['redirect'][:40]}"
            elif status_code in self.STATUS_CATEGORIES["server_error"]:
                check_status = Status.WARNING
                details = f"→ GET {target.path} → {status_code} {reason}"
            else:
                check_status = Status.WARNING
                details = f"→ GET {target.path} → {status_code} {reason}"

            # Check HTTP/2 if requested
            if self.config.check_http2:
                http2_supported = await self._check_http2(target)
                if http2_supported:
                    details += " [HTTP/2]"
                else:
                    details += " [HTTP/1.1]"

            # Build metadata
            metadata: Dict[str, Any] = {
                "status_code": status_code,
                "reason": reason,
                "path": target.path,
                "response_size": http_info.get("body_length", 0),
            }

            # Add response headers in deep mode
            if self.config.deep_mode:
                headers = http_info.get("headers", {})
                metadata["server"] = headers.get("Server", "Unknown")
                metadata["content_type"] = headers.get("Content-Type", "Unknown")

                # Check security headers
                security_headers = {
                    "strict-transport-security": headers.get(
                        "Strict-Transport-Security"
                    ),
                    "content-security-policy": headers.get("Content-Security-Policy"),
                    "x-frame-options": headers.get("X-Frame-Options"),
                    "x-content-type-options": headers.get("X-Content-Type-Options"),
                }
                metadata["security_headers"] = {
                    k: v for k, v in security_headers.items() if v
                }

            return CheckResult(
                name=self.name,
                duration_ms=duration,
                status=check_status,
                details=details,
                metadata=metadata,
            )

        except Exception as e:
            duration = (time.time() - start_time) * 1000
            return CheckResult(
                name=self.name,
                duration_ms=duration,
                status=Status.FAILURE,
                details="HTTP request failed",
                error=str(e),
            )

    async def _check_http2(self, target: Target) -> bool:
        """Check if HTTP/2 is supported"""
        try:
            import ssl
            import socket

            loop = asyncio.get_event_loop()

            def do_http2_check():
                context = ssl.create_default_context()
                context.set_alpn_protocols(["h2", "http/1.1"])

                sock = socket.create_connection((target.host, target.port), timeout=5.0)

                try:
                    with context.wrap_socket(
                        sock, server_hostname=target.host
                    ) as tls_sock:
                        negotiated = tls_sock.selected_alpn_protocol()
                        return negotiated == "h2"
                finally:
                    sock.close()

            return await loop.run_in_executor(None, do_http2_check)

        except Exception:
            return False
