#!/usr/bin/env python3
"""
pulse — Advanced Network Diagnostics Tool
High-performance async network diagnostics with comprehensive checks
"""

__version__ = "2.0.0"
__author__ = "pulse-team"

import argparse
import asyncio
import sys
from pathlib import Path
from typing import List, Optional

from pulse.core.config import Config
from pulse.core.engine import PulseEngine
from pulse.core.target import Target
from pulse.core.result import BenchmarkResult
from pulse.output.formatters import OutputFormatter
from pulse.utils.logger import get_logger


logger = get_logger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser"""
    parser = argparse.ArgumentParser(
        prog="pulse",
        description="Advanced Network Diagnostics Tool",
        epilog="""
Examples:
  pulse google.com
  pulse example.com:8080 --deep
  pulse https://api.github.com --json
  pulse targets.txt --from-file
  pulse google.com cloudflare.com --compare
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Target specification
    target_group = parser.add_argument_group("Target Specification")
    target_group.add_argument(
        "targets", nargs="*", help="Host[:port], URL, or path to file with targets"
    )
    target_group.add_argument(
        "--from-file",
        "-f",
        action="store_true",
        help="Read targets from file (one per line)",
    )
    target_group.add_argument(
        "--compare",
        "-c",
        action="store_true",
        help="Compare multiple targets side by side",
    )

    # Check options
    check_group = parser.add_argument_group("Check Options")
    check_group.add_argument(
        "--deep",
        "-d",
        action="store_true",
        help="Enable deep analysis (TLS details, cipher suites, etc.)",
    )
    check_group.add_argument(
        "--checks",
        default="dns,tcp,tls,http",
        help="Comma-separated list of checks to run (default: dns,tcp,tls,http)",
    )
    check_group.add_argument(
        "--timeout",
        "-t",
        type=float,
        default=10.0,
        help="Timeout per check in seconds (default: 10)",
    )
    check_group.add_argument(
        "--retries",
        "-r",
        type=int,
        default=1,
        help="Number of retries for failed checks (default: 1)",
    )
    check_group.add_argument(
        "--ipv6", action="store_true", help="Prefer IPv6 over IPv4"
    )
    check_group.add_argument(
        "--http2", action="store_true", help="Check HTTP/2 support"
    )
    check_group.add_argument(
        "--follow-redirects",
        action="store_true",
        default=True,
        help="Follow HTTP redirects (default: True)",
    )

    # Output options
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument(
        "--format",
        "-o",
        choices=["terminal", "json", "csv", "html", "markdown", "yaml"],
        default="terminal",
        help="Output format (default: terminal)",
    )
    output_group.add_argument(
        "--output", "-O", type=str, help="Output file path (default: stdout)"
    )
    output_group.add_argument(
        "--quiet", "-q", action="store_true", help="Suppress non-error output"
    )
    output_group.add_argument(
        "--no-color", action="store_true", help="Disable colored output"
    )
    output_group.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        help="Increase verbosity (use -vv for debug)",
    )

    # Performance options
    perf_group = parser.add_argument_group("Performance Options")
    perf_group.add_argument(
        "--workers",
        "-w",
        type=int,
        default=10,
        help="Number of concurrent workers (default: 10)",
    )
    perf_group.add_argument(
        "--benchmark",
        "-b",
        action="store_true",
        help="Run benchmark mode (10 iterations)",
    )

    # Config
    config_group = parser.add_argument_group("Configuration")
    config_group.add_argument("--config", type=str, help="Path to configuration file")
    config_group.add_argument(
        "--save-config", type=str, help="Save current options to configuration file"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    return parser


def load_targets(args) -> List[Target]:
    """Load targets from arguments or file"""
    targets = []

    if args.from_file and args.targets:
        # Read from file
        file_path = Path(args.targets[0])
        if file_path.exists():
            with open(file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        targets.append(Target(line))
        else:
            logger.error(f"File not found: {file_path}")
            sys.exit(2)
    elif args.targets:
        # Parse from command line
        for target_str in args.targets:
            targets.append(Target(target_str))
    else:
        logger.error("No targets specified")
        sys.exit(2)

    return targets


async def main_async():
    """Main async entry point"""
    parser = create_parser()
    args = parser.parse_args()

    # Load configuration
    config = Config.from_args(args)
    if args.config:
        config.load_from_file(args.config)

    # Save configuration if requested
    if args.save_config:
        config.save_to_file(args.save_config)
        if not args.quiet:
            print(f"Configuration saved to {args.save_config}")
        return

    # Load targets
    targets = load_targets(args)

    if not targets:
        logger.error("No valid targets to check")
        sys.exit(2)

    # Create engine and run checks
    engine = PulseEngine(config)

    try:
        if args.compare and len(targets) > 1:
            # Compare mode
            results = await engine.compare_targets(targets)
        elif args.benchmark:
            # Benchmark mode
            results = await engine.benchmark(targets[0], iterations=10)
        else:
            # Normal mode
            results = await engine.check_targets(targets)

        # Format and output results
        formatter = OutputFormatter(config)
        output = formatter.format(results)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            if not args.quiet:
                print(f"Results saved to {args.output}")
        else:
            print(output)

        # Exit codes: 0 = all healthy, 1 = warnings, 2 = failures
        exit_code = 0

        # Handle different result types
        if isinstance(results, BenchmarkResult):
            # For benchmark, check success rate
            if results.success_rate < 50:
                exit_code = 2
            elif results.success_rate < 90:
                exit_code = 1
        elif isinstance(results, list):
            # For list of TargetResult
            for result in results:
                if result.has_failures:
                    exit_code = 2
                    break
                elif result.has_warnings:
                    exit_code = 1
        else:
            # Single TargetResult
            if results.has_failures:
                exit_code = 2
            elif results.has_warnings:
                exit_code = 1

        sys.exit(exit_code)

    except KeyboardInterrupt:
        if not args.quiet:
            print("\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Error: {e}")
        if args.verbose >= 2:
            import traceback

            traceback.print_exc()
        sys.exit(2)


def main():
    """Main entry point"""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
