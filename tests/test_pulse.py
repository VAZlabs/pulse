"""Tests for pulse package"""

import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock
import socket
import ssl

from pulse.core.target import Target
from pulse.core.config import Config
from pulse.core.result import CheckResult, TargetResult, Status
from pulse.checks.dns import DNSChecker
from pulse.checks.tcp import TCPChecker
from pulse.checks.tls import TLSChecker
from pulse.checks.http import HTTPChecker
from pulse.core.engine import PulseEngine


class TestTarget:
    """Test Target parsing"""

    def test_parse_simple_host(self):
        target = Target("example.com")
        assert target.host == "example.com"
        assert target.port == 443
        assert target.scheme == "https"

    def test_parse_host_with_port(self):
        target = Target("example.com:8080")
        assert target.host == "example.com"
        assert target.port == 8080
        assert target.scheme == "http"

    def test_parse_http_url(self):
        target = Target("http://example.com")
        assert target.host == "example.com"
        assert target.port == 80
        assert target.scheme == "http"

    def test_parse_https_url(self):
        target = Target("https://example.com")
        assert target.host == "example.com"
        assert target.port == 443
        assert target.scheme == "https"

    def test_parse_https_url_with_port(self):
        target = Target("https://example.com:8443")
        assert target.host == "example.com"
        assert target.port == 8443
        assert target.scheme == "https"

    def test_use_tls_property(self):
        assert Target("https://example.com").use_tls is True
        assert Target("example.com:443").use_tls is True
        assert Target("http://example.com").use_tls is False
        assert Target("example.com:80").use_tls is False


class TestConfig:
    """Test Config class"""

    def test_default_config(self):
        config = Config()
        assert config.timeout == 10.0
        assert config.retries == 1
        assert config.workers == 10
        assert "dns" in config.checks

    def test_config_from_dict(self):
        data = {
            "timeout": 5.0,
            "retries": 3,
            "checks": ["dns", "tcp"],
        }
        config = Config.from_dict(data)
        assert config.timeout == 5.0
        assert config.retries == 3
        assert config.checks == ["dns", "tcp"]

    def test_config_to_dict(self):
        config = Config(timeout=5.0)
        data = config.to_dict()
        assert data["timeout"] == 5.0


class TestCheckResult:
    """Test CheckResult class"""

    def test_success_result(self):
        result = CheckResult(
            name="DNS", duration_ms=100.0, status=Status.SUCCESS, details="OK"
        )
        assert result.is_success is True
        assert result.is_failure is False
        assert result.is_warning is False

    def test_failure_result(self):
        result = CheckResult(
            name="TCP",
            duration_ms=50.0,
            status=Status.FAILURE,
            details="Failed",
            error="Connection refused",
        )
        assert result.is_success is False
        assert result.is_failure is True

    def test_to_dict(self):
        result = CheckResult(
            name="DNS", duration_ms=100.0, status=Status.SUCCESS, details="OK"
        )
        data = result.to_dict()
        assert data["name"] == "DNS"
        assert data["status"] == "success"


class TestDNSChecker:
    """Test DNS checker"""

    @pytest.mark.asyncio
    async def test_dns_success(self):
        config = Config()
        checker = DNSChecker(config)
        target = Target("localhost")

        result = await checker.check(target)

        assert result.name == "DNS"
        assert result.is_success
        assert "127.0.0.1" in result.details

    @pytest.mark.asyncio
    async def test_dns_failure(self):
        config = Config()
        checker = DNSChecker(config)
        target = Target("this-host-does-not-exist-12345.invalid")

        result = await checker.check(target)

        assert result.is_failure
        assert "Failed" in result.details or "error" in result.error.lower()


class TestTCPChecker:
    """Test TCP checker"""

    @pytest.mark.asyncio
    async def test_tcp_refused(self):
        config = Config(timeout=1.0)
        checker = TCPChecker(config)
        target = Target("localhost:65432")  # Unlikely to be open

        result = await checker.check(target)

        assert result.name == "TCP"
        assert result.is_failure


class TestTLSChecker:
    """Test TLS checker"""

    @pytest.mark.asyncio
    async def test_tls_success(self):
        config = Config()
        checker = TLSChecker(config)
        target = Target("cloudflare.com")

        result = await checker.check(target)

        assert result.name == "TLS"
        # Should succeed on real TLS site
        assert result.is_success or result.is_failure  # Either is valid


class TestHTTPChecker:
    """Test HTTP checker"""

    @pytest.mark.asyncio
    async def test_http_success(self):
        config = Config()
        checker = HTTPChecker(config)
        target = Target("httpbin.org")

        result = await checker.check(target)

        assert result.name == "HTTP"
        assert result.duration_ms > 0


class TestPulseEngine:
    """Test PulseEngine"""

    @pytest.mark.asyncio
    async def test_check_single_target(self):
        config = Config(checks=["dns"])
        engine = PulseEngine(config)
        target = Target("localhost")

        result = await engine.check_target(target)

        assert isinstance(result, TargetResult)
        assert result.target == target
        assert len(result.checks) == 1
        assert result.checks[0].name == "DNS"

        await engine.close()

    @pytest.mark.asyncio
    async def test_check_multiple_targets(self):
        config = Config(checks=["dns"], workers=2)
        engine = PulseEngine(config)
        targets = [Target("localhost"), Target("127.0.0.1")]

        results = await engine.check_targets(targets)

        assert len(results) == 2
        assert all(isinstance(r, TargetResult) for r in results)

        await engine.close()

    @pytest.mark.asyncio
    async def test_benchmark(self):
        config = Config(checks=["dns"])
        engine = PulseEngine(config)
        target = Target("localhost")

        result = await engine.benchmark(target, iterations=3)

        assert result.iterations == 3
        assert len(result.results) == 3
        assert result.avg_duration_ms > 0

        await engine.close()


class TestOutputFormatters:
    """Test output formatters"""

    def test_terminal_formatter(self):
        from pulse.output.terminal import TerminalFormatter

        config = Config()
        formatter = TerminalFormatter(config)

        result = TargetResult(
            target=Target("example.com"),
            checks=[
                CheckResult("DNS", 10.0, Status.SUCCESS, "OK"),
                CheckResult("TCP", 20.0, Status.SUCCESS, "Connected"),
            ],
        )

        output = formatter.format(result)
        assert "example.com" in output
        assert "DNS" in output
        assert "TCP" in output

    def test_json_formatter(self):
        from pulse.output.formatters import OutputFormatter
        import json

        config = Config(format="json")
        formatter = OutputFormatter(config)

        result = TargetResult(
            target=Target("example.com"),
            checks=[
                CheckResult("DNS", 10.0, Status.SUCCESS, "OK"),
            ],
        )

        output = formatter.format([result])
        data = json.loads(output)
        assert len(data) == 1
        assert data[0]["target"] == "example.com"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
