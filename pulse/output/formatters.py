"""Output formatters for different formats"""

import json
import csv
import io
from typing import List, Any, Union
from datetime import datetime

from ..core.config import Config
from ..core.result import TargetResult, BenchmarkResult
from .terminal import TerminalFormatter


class OutputFormatter:
    """Main output formatter that delegates to specific formatters"""

    def __init__(self, config: Config):
        self.config = config
        self.terminal = TerminalFormatter(config)

    def format(self, results: Union[List[TargetResult], BenchmarkResult]) -> str:
        """Format results based on config format"""
        if self.config.format == "terminal":
            return self.terminal.format(results)
        elif self.config.format == "json":
            return self._format_json(results)
        elif self.config.format == "csv":
            return self._format_csv(results)
        elif self.config.format == "html":
            return self._format_html(results)
        elif self.config.format == "markdown":
            return self._format_markdown(results)
        elif self.config.format == "yaml":
            return self._format_yaml(results)
        else:
            return self.terminal.format(results)

    def _format_json(self, results: Union[List[TargetResult], BenchmarkResult]) -> str:
        """Format as JSON"""
        if isinstance(results, BenchmarkResult):
            data = results.to_dict()
        elif isinstance(results, list):
            data = [r.to_dict() for r in results]
        else:
            data = results.to_dict()

        return json.dumps(data, indent=2, ensure_ascii=False)

    def _format_csv(self, results: Union[List[TargetResult], BenchmarkResult]) -> str:
        """Format as CSV"""
        if isinstance(results, BenchmarkResult):
            results = results.results
        elif not isinstance(results, list):
            results = [results]

        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(
            [
                "Target",
                "Check",
                "Status",
                "Duration (ms)",
                "Details",
                "Error",
                "Timestamp",
            ]
        )

        # Data
        for target_result in results:
            for check in target_result.checks:
                writer.writerow(
                    [
                        str(target_result.target),
                        check.name,
                        check.status.value,
                        round(check.duration_ms, 2),
                        check.details,
                        check.error or "",
                        check.timestamp.isoformat(),
                    ]
                )

        return output.getvalue()

    def _format_html(self, results: Union[List[TargetResult], BenchmarkResult]) -> str:
        """Format as HTML"""
        if isinstance(results, BenchmarkResult):
            results = results.results
        elif not isinstance(results, list):
            results = [results]

        html = """<!DOCTYPE html>
<html>
<head>
    <title>Pulse Network Diagnostics Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        h1 { color: #333; }
        .target { background: white; margin: 20px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .target-header { font-size: 1.2em; font-weight: bold; margin-bottom: 10px; color: #555; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f8f8f8; font-weight: bold; }
        .status-success { color: #28a745; font-weight: bold; }
        .status-warning { color: #ffc107; font-weight: bold; }
        .status-failure { color: #dc3545; font-weight: bold; }
        .status-skipped { color: #6c757d; font-weight: bold; }
        .error { color: #dc3545; font-size: 0.9em; }
        .timestamp { color: #999; font-size: 0.85em; margin-top: 10px; }
    </style>
</head>
<body>
    <h1>🔍 Pulse Network Diagnostics Report</h1>
    <p>Generated: {}</p>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        for target_result in results:
            html += f'<div class="target">\n'
            html += f'<div class="target-header">{target_result.target.address}</div>\n'
            html += "<table>\n"
            html += "<tr><th>Check</th><th>Status</th><th>Duration</th><th>Details</th></tr>\n"

            for check in target_result.checks:
                status_class = f"status-{check.status.value}"
                error_cell = (
                    f'<div class="error">{check.error}</div>' if check.error else ""
                )

                html += f"<tr>\n"
                html += f"  <td>{check.name}</td>\n"
                html += (
                    f'  <td class="{status_class}">{check.status.value.upper()}</td>\n'
                )
                html += f"  <td>{check.duration_ms:.2f} ms</td>\n"
                html += f"  <td>{check.details}{error_cell}</td>\n"
                html += f"</tr>\n"

            html += "</table>\n"
            html += f'<div class="timestamp">Total: {target_result.total_duration_ms:.2f} ms</div>\n'
            html += "</div>\n"

        html += """
</body>
</html>
"""
        return html

    def _format_markdown(
        self, results: Union[List[TargetResult], BenchmarkResult]
    ) -> str:
        """Format as Markdown"""
        if isinstance(results, BenchmarkResult):
            results = results.results
        elif not isinstance(results, list):
            results = [results]

        md = f"# 🔍 Pulse Network Diagnostics Report\n\n"
        md += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        for target_result in results:
            md += f"## {target_result.target.address}\n\n"
            md += "| Check | Status | Duration | Details |\n"
            md += "|-------|--------|----------|----------|\n"

            for check in target_result.checks:
                status_icon = {
                    "success": "✅",
                    "warning": "⚠️",
                    "failure": "❌",
                    "skipped": "⏭️",
                }.get(check.status.value, "❓")

                details = check.details.replace("|", "\\|")
                md += f"| {check.name} | {status_icon} {check.status.value} | {check.duration_ms:.2f} ms | {details} |\n"

            md += f"\n**Total:** {target_result.total_duration_ms:.2f} ms\n\n"

            if target_result.has_failures:
                md += "⚠️ **Issues detected**\n\n"
            elif target_result.has_warnings:
                md += "⚡ **Warnings detected**\n\n"
            else:
                md += "✨ **All healthy**\n\n"

            md += "---\n\n"

        return md

    def _format_yaml(self, results: Union[List[TargetResult], BenchmarkResult]) -> str:
        """Format as YAML"""
        try:
            import yaml

            if isinstance(results, BenchmarkResult):
                data = results.to_dict()
            elif isinstance(results, list):
                data = [r.to_dict() for r in results]
            else:
                data = results.to_dict()

            return yaml.dump(data, default_flow_style=False, allow_unicode=True)
        except ImportError:
            # Fallback to JSON if PyYAML not available
            return self._format_json(results)
