"""Configuration management for pulse"""

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, List


@dataclass
class Config:
    """Configuration class for pulse"""

    # Check options
    deep_mode: bool = False
    checks: List[str] = None
    timeout: float = 10.0
    retries: int = 1
    prefer_ipv6: bool = False
    check_http2: bool = False
    follow_redirects: bool = True

    # Output options
    format: str = "terminal"
    output_file: Optional[str] = None
    quiet: bool = False
    no_color: bool = False
    verbose: int = 0

    # Performance
    workers: int = 10
    benchmark_mode: bool = False

    # Comparison
    compare_mode: bool = False

    def __post_init__(self):
        if self.checks is None:
            self.checks = ["dns", "tcp", "tls", "http"]
        elif isinstance(self.checks, str):
            self.checks = [c.strip() for c in self.checks.split(",")]

    @classmethod
    def from_args(cls, args) -> "Config":
        """Create config from argparse args"""
        return cls(
            deep_mode=args.deep,
            checks=args.checks.split(",")
            if isinstance(args.checks, str)
            else args.checks,
            timeout=args.timeout,
            retries=args.retries,
            prefer_ipv6=args.ipv6,
            check_http2=args.http2,
            follow_redirects=args.follow_redirects,
            format=args.format,
            output_file=args.output,
            quiet=args.quiet,
            no_color=args.no_color,
            verbose=args.verbose,
            workers=args.workers,
            benchmark_mode=args.benchmark,
            compare_mode=args.compare,
        )

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        """Create config from dictionary"""
        return cls(**data)

    def to_dict(self) -> dict:
        """Convert config to dictionary"""
        return asdict(self)

    def load_from_file(self, path: str) -> None:
        """Load configuration from JSON file"""
        file_path = Path(path)
        if file_path.exists():
            with open(file_path, "r") as f:
                data = json.load(f)
                for key, value in data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)

    def save_to_file(self, path: str) -> None:
        """Save configuration to JSON file"""
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
