"""Terminal output formatter with beautiful colors"""

from typing import List, Union

from ..core.config import Config
from ..core.result import TargetResult, BenchmarkResult, Status


class Colors:
    """ANSI color codes"""

    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BLUE = "\033[94m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    BRIGHT = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

    # Combinations
    BOLD_GREEN = f"{BRIGHT}{GREEN}"
    BOLD_YELLOW = f"{BRIGHT}{YELLOW}"
    BOLD_RED = f"{BRIGHT}{RED}"
    BOLD_CYAN = f"{BRIGHT}{CYAN}"
    BOLD_MAGENTA = f"{BRIGHT}{MAGENTA}"


class TerminalFormatter:
    """Format output for terminal with colors"""

    STATUS_ICONS = {
        Status.SUCCESS: "✓",
        Status.WARNING: "⚠️",
        Status.FAILURE: "✗",
        Status.SKIPPED: "⊘",
    }

    def __init__(self, config: Config):
        self.config = config
        self.c = (
            Colors()
            if not config.no_color
            else type(
                "obj",
                (object,),
                {
                    "GREEN": "",
                    "YELLOW": "",
                    "RED": "",
                    "CYAN": "",
                    "MAGENTA": "",
                    "BLUE": "",
                    "WHITE": "",
                    "GRAY": "",
                    "BRIGHT": "",
                    "DIM": "",
                    "RESET": "",
                    "BOLD_GREEN": "",
                    "BOLD_YELLOW": "",
                    "BOLD_RED": "",
                    "BOLD_CYAN": "",
                    "BOLD_MAGENTA": "",
                },
            )()
        )

    def format(self, results: Union[List[TargetResult], BenchmarkResult]) -> str:
        """Format results for terminal"""
        if isinstance(results, BenchmarkResult):
            return self._format_benchmark(results)
        elif isinstance(results, list) and len(results) == 1:
            return self._format_single(results[0])
        elif isinstance(results, list):
            return self._format_multiple(results)
        else:
            return self._format_single(results)

    def _format_single(self, result: TargetResult) -> str:
        """Format single target result"""
        lines = []
        c = self.c

        # Header
        if not self.config.quiet:
            lines.extend(
                [
                    "",
                    f"{c.MAGENTA}╔════════════════════════════════════════════════════════════╗{c.RESET}",
                    f"{c.MAGENTA}║{c.RESET}  {c.BOLD_MAGENTA}🔍 pulse — Network Diagnostics{c.RESET}{c.MAGENTA}                        ║{c.RESET}",
                    f"{c.MAGENTA}╚════════════════════════════════════════════════════════════╝{c.RESET}",
                    "",
                    f"  {c.BRIGHT}Target:{c.RESET}  {c.BOLD_CYAN}{result.target.address}{c.RESET}",
                ]
            )

            if self.config.deep_mode:
                lines.append(
                    f"  {c.BRIGHT}Mode:{c.RESET}    {c.BOLD_YELLOW}Deep Analysis{c.RESET}"
                )

            lines.append("")

        # Results section
        lines.extend(
            [
                f"{c.CYAN}┌────────────────────────────────────────────────────────────┐{c.RESET}",
                f"{c.CYAN}│{c.RESET} {c.BRIGHT}Results{c.RESET}{c.CYAN}                                                     │{c.RESET}",
                f"{c.CYAN}└────────────────────────────────────────────────────────────┘{c.RESET}",
                "",
            ]
        )

        # Check results
        for check in result.checks:
            lines.append(self._format_check_line(check))

        lines.append("")

        # Summary box
        lines.extend(self._format_summary(result))

        return "\n".join(lines)

    def _format_multiple(self, results: List[TargetResult]) -> str:
        """Format multiple target results"""
        lines = []
        c = self.c

        # Header
        lines.extend(
            [
                "",
                f"{c.MAGENTA}╔════════════════════════════════════════════════════════════╗{c.RESET}",
                f"{c.MAGENTA}║{c.RESET}  {c.BOLD_MAGENTA}🔍 pulse — Network Diagnostics ({len(results)} targets){c.RESET}{c.MAGENTA}      ║{c.RESET}",
                f"{c.MAGENTA}╚════════════════════════════════════════════════════════════╝{c.RESET}",
                "",
            ]
        )

        # Summary table
        lines.extend(
            [
                f"{c.CYAN}┌────────────────────────────────────────────────────────────┐{c.RESET}",
                f"{c.CYAN}│{c.RESET} {c.BRIGHT}Summary{c.RESET}{c.CYAN}                                                     │{c.RESET}",
                f"{c.CYAN}└────────────────────────────────────────────────────────────┘{c.RESET}",
                "",
            ]
        )

        # Table header
        lines.append(
            f"  {c.BRIGHT}{'Target':<30} {'Status':<10} {'Duration':<12} {'Checks'}{c.RESET}"
        )
        lines.append(f"  {c.GRAY}{'─' * 70}{c.RESET}")

        # Table rows
        for result in results:
            status = self._get_overall_status(result)
            status_str = f"{status['icon']} {status['text']}"

            checks_str = f"{result.success_count}✓"
            if result.warning_count:
                checks_str += f" {result.warning_count}⚠"
            if result.failure_count:
                checks_str += f" {result.failure_count}✗"

            lines.append(
                f"  {result.target.address:<30} "
                f"{status_str:<10} "
                f"{result.total_duration_ms:>6.0f} ms   "
                f"{checks_str}"
            )

        lines.append("")

        # Detailed results
        if self.config.verbose >= 1:
            for result in results:
                lines.append(f"\n{c.CYAN}▶ {result.target.address}{c.RESET}")
                for check in result.checks:
                    lines.append("  " + self._format_check_line(check, indent=True))

        return "\n".join(lines)

    def _format_benchmark(self, result: BenchmarkResult) -> str:
        """Format benchmark results"""
        lines = []
        c = self.c

        lines.extend(
            [
                "",
                f"{c.MAGENTA}╔════════════════════════════════════════════════════════════╗{c.RESET}",
                f"{c.MAGENTA}║{c.RESET}  {c.BOLD_MAGENTA}📊 Benchmark Results{c.RESET}{c.MAGENTA}                                ║{c.RESET}",
                f"{c.MAGENTA}╚════════════════════════════════════════════════════════════╝{c.RESET}",
                "",
                f"  {c.BRIGHT}Target:{c.RESET}      {c.BOLD_CYAN}{result.target.address}{c.RESET}",
                f"  {c.BRIGHT}Iterations:{c.RESET}  {result.iterations}",
                "",
            ]
        )

        # Statistics
        lines.extend(
            [
                f"{c.CYAN}┌────────────────────────────────────────────────────────────┐{c.RESET}",
                f"{c.CYAN}│{c.RESET} {c.BRIGHT}Statistics{c.RESET}{c.CYAN}                                                  │{c.RESET}",
                f"{c.CYAN}└────────────────────────────────────────────────────────────┘{c.RESET}",
                "",
                f"  {c.BRIGHT}Average:{c.RESET}     {c.BOLD_CYAN}{result.avg_duration_ms:>6.1f} ms{c.RESET}",
                f"  {c.BRIGHT}Minimum:{c.RESET}     {c.GREEN}{result.min_duration_ms:>6.1f} ms{c.RESET}",
                f"  {c.BRIGHT}Maximum:{c.RESET}     {c.YELLOW}{result.max_duration_ms:>6.1f} ms{c.RESET}",
                f"  {c.BRIGHT}Success Rate:{c.RESET} {c.GREEN if result.success_rate >= 90 else c.YELLOW if result.success_rate >= 50 else c.RED}{result.success_rate:.1f}%{c.RESET}",
                "",
            ]
        )

        # Per-iteration details
        if self.config.verbose >= 1:
            lines.extend(
                [
                    f"{c.CYAN}┌────────────────────────────────────────────────────────────┐{c.RESET}",
                    f"{c.CYAN}│{c.RESET} {c.BRIGHT}Iterations{c.RESET}{c.CYAN}                                                 │{c.RESET}",
                    f"{c.CYAN}└────────────────────────────────────────────────────────────┘{c.RESET}",
                    "",
                ]
            )

            for i, run in enumerate(result.results, 1):
                status = "✓" if run.is_healthy else "✗"
                color = c.GREEN if run.is_healthy else c.RED
                lines.append(
                    f"  {color}{status}{c.RESET} Run {i:2d}: {run.total_duration_ms:>6.1f} ms"
                )

        lines.append("")

        return "\n".join(lines)

    def _format_check_line(self, check, indent: bool = False) -> str:
        """Format a single check line"""
        c = self.c
        prefix = "  " if indent else ""

        icon = self.STATUS_ICONS.get(check.status, "?")

        if check.status == Status.SUCCESS:
            color = c.BOLD_GREEN
        elif check.status == Status.WARNING:
            color = c.BOLD_YELLOW
        elif check.status == Status.FAILURE:
            color = c.BOLD_RED
        else:
            color = c.GRAY

        time_str = f"{check.duration_ms:>6.0f} ms"
        name_pad = f"{check.name:<7}"

        line = f"{prefix}{color}▸ {icon}{c.RESET}  {c.BRIGHT}{name_pad}{c.RESET}  {c.CYAN}{time_str}{c.RESET}  {c.MAGENTA}»{c.RESET}  {check.details}"

        if check.error:
            line += f"\n{prefix}     {c.RED}⚠ {check.error}{c.RESET}"

        return line

    def _format_summary(self, result: TargetResult) -> List[str]:
        """Format summary box"""
        lines = []
        c = self.c

        total = result.total_duration_ms

        if result.is_healthy:
            lines.extend(
                [
                    f"{c.GREEN}╔════════════════════════════════════════════════════════════╗{c.RESET}",
                    f"{c.GREEN}║{c.RESET}  {c.BOLD_GREEN}✨ All Systems Healthy ✨{c.RESET}{c.GREEN}                          ║{c.RESET}",
                    f"{c.GREEN}║{c.RESET}  Total time: {c.BOLD_CYAN}{total:.0f} ms{c.RESET}{c.GREEN}                                  ║{c.RESET}",
                    f"{c.GREEN}╚════════════════════════════════════════════════════════════╝{c.RESET}",
                ]
            )
        elif result.has_warnings and not result.has_failures:
            lines.extend(
                [
                    f"{c.YELLOW}╔════════════════════════════════════════════════════════════╗{c.RESET}",
                    f"{c.YELLOW}║{c.RESET}  {c.BOLD_YELLOW}⚡ Performance Issues Detected ⚡{c.RESET}{c.YELLOW}                   ║{c.RESET}",
                    f"{c.YELLOW}║{c.RESET}  Total time: {c.BOLD_CYAN}{total:.0f} ms{c.RESET}{c.YELLOW}                                  ║{c.RESET}",
                    f"{c.YELLOW}╚════════════════════════════════════════════════════════════╝{c.RESET}",
                ]
            )
            lines.extend(self._format_recommendations(result))
        else:
            lines.extend(
                [
                    f"{c.RED}╔════════════════════════════════════════════════════════════╗{c.RESET}",
                    f"{c.RED}║{c.RESET}  {c.BOLD_RED}🚨 Critical Issues Found 🚨{c.RESET}{c.RED}                       ║{c.RESET}",
                    f"{c.RED}║{c.RESET}  Total time: {c.BOLD_CYAN}{total:.0f} ms{c.RESET}{c.RED}                                  ║{c.RESET}",
                    f"{c.RED}╚════════════════════════════════════════════════════════════╝{c.RESET}",
                ]
            )
            lines.extend(self._format_troubleshooting(result))

        return lines

    def _format_recommendations(self, result: TargetResult) -> List[str]:
        """Format recommendations for warnings"""
        lines = []
        c = self.c

        lines.extend(
            [
                "",
                f"{c.YELLOW}💡 Recommendations:{c.RESET}",
                "",
            ]
        )

        for check in result.checks:
            if check.is_warning:
                if check.name == "TLS":
                    if "deprecated" in check.details.lower():
                        lines.extend(
                            [
                                f"  {c.CYAN}→ TLS Version Issue{c.RESET}",
                                f"    {c.MAGENTA}•{c.RESET} Upgrade to TLS 1.3",
                                f"    {c.MAGENTA}•{c.RESET} Disable legacy TLS versions",
                                "",
                            ]
                        )
                    elif "slow" in check.details.lower():
                        lines.extend(
                            [
                                f"  {c.CYAN}→ TLS Performance Issue{c.RESET}",
                                f"    {c.MAGENTA}•{c.RESET} Enable TLS session resumption",
                                f"    {c.MAGENTA}•{c.RESET} Use modern cipher suites",
                                "",
                            ]
                        )
                elif check.name == "HTTP":
                    lines.extend(
                        [
                            f"  {c.CYAN}→ HTTP Response Warning{c.RESET}",
                            f"    {c.MAGENTA}•{c.RESET} Check server configuration",
                            "",
                        ]
                    )

        return lines

    def _format_troubleshooting(self, result: TargetResult) -> List[str]:
        """Format troubleshooting guide for failures"""
        lines = []
        c = self.c

        lines.extend(
            [
                "",
                f"{c.RED}🔧 Troubleshooting:{c.RESET}",
                "",
            ]
        )

        for check in result.checks:
            if check.is_failure:
                if check.name == "DNS":
                    lines.extend(
                        [
                            f"  {c.RED}❌ DNS Resolution Failed{c.RESET}",
                            f"     {c.CYAN}→{c.RESET} Run: nslookup {result.target.host}",
                            f"     {c.CYAN}→{c.RESET} Check DNS settings",
                            "",
                        ]
                    )
                elif check.name == "TCP":
                    lines.extend(
                        [
                            f"  {c.RED}❌ TCP Connection Failed{c.RESET}",
                            f"     {c.CYAN}→{c.RESET} Check if service is running on port {result.target.port}",
                            f"     {c.CYAN}→{c.RESET} Verify firewall rules",
                            "",
                        ]
                    )
                elif check.name == "TLS":
                    lines.extend(
                        [
                            f"  {c.RED}❌ TLS Handshake Failed{c.RESET}",
                            f"     {c.CYAN}→{c.RESET} Check certificate validity",
                            f"     {c.CYAN}→{c.RESET} Run: openssl s_client -connect {result.target.address}",
                            "",
                        ]
                    )
                elif check.name == "HTTP":
                    lines.extend(
                        [
                            f"  {c.RED}❌ HTTP Request Failed{c.RESET}",
                            f"     {c.CYAN}→{c.RESET} Check application logs",
                            f"     {c.CYAN}→{c.RESET} Verify URL path",
                            "",
                        ]
                    )

        return lines

    def _get_overall_status(self, result: TargetResult) -> dict:
        """Get overall status for a result"""
        if result.has_failures:
            return {"icon": "❌", "text": "FAIL", "color": self.c.RED}
        elif result.has_warnings:
            return {"icon": "⚠️", "text": "WARN", "color": self.c.YELLOW}
        else:
            return {"icon": "✅", "text": "OK", "color": self.c.GREEN}
