"""TLS/SSL checker"""

import asyncio
import ssl
import socket
import time
from datetime import datetime
from typing import Dict, Any, Optional

from . import BaseChecker
from ..core.target import Target
from ..core.result import CheckResult, Status
from ..utils.logger import get_logger


logger = get_logger(__name__)


class TLSChecker(BaseChecker):
    """Check TLS/SSL connectivity and certificate"""

    name = "TLS"

    # TLS version ratings
    TLS_VERSIONS = {
        "TLSv1.3": ("excellent", 0),
        "TLSv1.2": ("good", 1),
        "TLSv1.1": ("warning", 2),
        "TLSv1": ("warning", 2),
        "SSLv3": ("critical", 3),
        "SSLv2": ("critical", 3),
    }

    async def check(self, target: Target) -> CheckResult:
        """Check TLS connection and certificate"""
        start_time = time.time()

        try:
            loop = asyncio.get_event_loop()

            # Create SSL context
            context = ssl.create_default_context()
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED

            # Try to connect and get TLS info
            def do_tls_check():
                sock = socket.create_connection(
                    (target.host, target.port), timeout=self.config.timeout
                )

                try:
                    with context.wrap_socket(
                        sock, server_hostname=target.host
                    ) as tls_sock:
                        version = tls_sock.version()
                        cipher = tls_sock.cipher()
                        cert = tls_sock.getpeercert()

                        return {
                            "version": version,
                            "cipher": cipher,
                            "cert": cert,
                        }
                finally:
                    sock.close()

            tls_info = await loop.run_in_executor(None, do_tls_check)
            duration = (time.time() - start_time) * 1000

            # Analyze results
            version = tls_info.get("version", "Unknown")
            cipher_tuple = tls_info.get("cipher")
            cipher_name = cipher_tuple[0] if cipher_tuple else "Unknown"
            cert = tls_info.get("cert", {})

            # Determine status based on TLS version
            version_rating = self.TLS_VERSIONS.get(version, ("unknown", 0))

            if version_rating[1] >= 3:  # SSLv2/3
                status = Status.FAILURE
                details = f"→ {version} (INSECURE!)"
            elif version_rating[1] >= 2:  # TLS 1.0/1.1
                status = Status.WARNING
                details = f"→ {version} (deprecated)"
            elif self.config.deep_mode and duration > 200:
                status = Status.WARNING
                details = f"→ {version} • {cipher_name} (slow)"
            else:
                status = Status.SUCCESS
                details = f"→ {version} • {cipher_name}"

            # Build metadata
            metadata: Dict[str, Any] = {
                "version": version,
                "cipher": cipher_name,
                "version_rating": version_rating[0],
            }

            # Add certificate info in deep mode
            if self.config.deep_mode and cert:
                cert_info = self._parse_certificate(cert)
                metadata["certificate"] = cert_info

                if cert_info.get("expired"):
                    status = Status.FAILURE
                    details += " [EXPIRED CERT]"
                elif cert_info.get("expires_soon"):
                    status = Status.WARNING
                    details += " [expires soon]"

            return CheckResult(
                name=self.name,
                duration_ms=duration,
                status=status,
                details=details,
                metadata=metadata,
            )

        except ssl.SSLError as e:
            duration = (time.time() - start_time) * 1000
            return CheckResult(
                name=self.name,
                duration_ms=duration,
                status=Status.FAILURE,
                details="TLS handshake failed",
                error=f"SSL error: {e}",
            )
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            return CheckResult(
                name=self.name,
                duration_ms=duration,
                status=Status.FAILURE,
                details="TLS check failed",
                error=str(e),
            )

    def _parse_certificate(self, cert: dict) -> dict:
        """Parse certificate info"""
        result = {}

        if "subject" in cert:
            subject = cert["subject"]
            if isinstance(subject, tuple):
                result["subject"] = dict(subject)
            else:
                result["subject"] = subject

        if "issuer" in cert:
            issuer = cert["issuer"]
            if isinstance(issuer, tuple):
                result["issuer"] = dict(issuer)
            else:
                result["issuer"] = issuer

        if "notAfter" in cert:
            result["expires"] = cert["notAfter"]
            # Check if expired
            try:
                # Parse the date
                expire_date = datetime.strptime(
                    cert["notAfter"], "%b %d %H:%M:%S %Y %Z"
                )
                now = datetime.utcnow()
                result["expired"] = expire_date < now
                result["expires_soon"] = (expire_date - now).days < 30
                result["days_until_expiry"] = (expire_date - now).days
            except Exception:
                pass

        if "serialNumber" in cert:
            result["serial"] = cert["serialNumber"]

        return result

    def _get_cipher_security(self, cipher: str) -> str:
        """Get cipher security rating"""
        insecure = ["NULL", "EXPORT", "DES", "MD5", "RC4"]
        weak = ["3DES", "CBC"]

        cipher_upper = cipher.upper()

        for patt in insecure:
            if patt in cipher_upper:
                return "insecure"

        for patt in weak:
            if patt in cipher_upper:
                return "weak"

        if "AES_256_GCM" in cipher_upper or "CHACHA20" in cipher_upper:
            return "strong"

        return "good"
