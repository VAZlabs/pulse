"""Target parsing and representation"""

from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse


@dataclass
class Target:
    """Represents a check target"""

    raw: str
    host: str = ""
    port: int = 0
    scheme: str = "https"
    path: str = "/"
    is_url: bool = False

    def __post_init__(self):
        if not self.host:
            self._parse()

    def _parse(self):
        """Parse target string"""
        target = self.raw.strip()

        # Check if it's a URL
        if target.startswith(("http://", "https://")):
            parsed = urlparse(target)
            self.host = parsed.hostname or ""
            self.port = parsed.port or (443 if parsed.scheme == "https" else 80)
            self.scheme = parsed.scheme
            self.path = parsed.path or "/"
            self.is_url = True
        elif ":" in target:
            # Try to parse as host:port
            parts = target.rsplit(":", 1)
            try:
                self.host = parts[0]
                self.port = int(parts[1])
                self.scheme = "https" if self.port in [443, 8443] else "http"
            except ValueError:
                # Not a valid port, treat as hostname with colon
                self.host = target
                self.port = 443
                self.scheme = "https"
        else:
            # Simple hostname
            self.host = target
            self.port = 443
            self.scheme = "https"

    @property
    def use_tls(self) -> bool:
        """Check if TLS should be used"""
        return self.scheme == "https" or self.port in [443, 8443]

    @property
    def address(self) -> str:
        """Get host:port string"""
        return f"{self.host}:{self.port}"

    @property
    def url(self) -> str:
        """Get full URL"""
        return f"{self.scheme}://{self.host}:{self.port}{self.path}"

    def __str__(self) -> str:
        return self.raw

    def __repr__(self) -> str:
        return f"Target({self.raw!r})"

    def __hash__(self) -> int:
        return hash(self.raw)

    def __eq__(self, other) -> bool:
        if isinstance(other, Target):
            return self.raw == other.raw
        return False
