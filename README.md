# pulse — Advanced Network Diagnostics Tool

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)
![License](https://img.shields.io/badge/license-GPL--3.0-red.svg)

> A high-performance async network diagnostics tool that checks DNS → TCP → TLS → HTTP chains with comprehensive analysis, multiple output formats, and actionable insights.

---

## ✨ What's New in 2.0

- **Async Architecture** — Concurrent checks with configurable workers
- **Multiple Output Formats** — Terminal, JSON, CSV, HTML, Markdown, YAML
- **IPv6 Support** — Full IPv4/IPv6 dual-stack support
- **Benchmark Mode** — Run multiple iterations and get statistics
- **Comparison Mode** — Compare multiple targets side-by-side
- **Deep Analysis** — TLS certificate details, security headers, HTTP/2 detection
- **Configuration Files** — Save and load settings
- **Retry Logic** — Automatic retries with exponential backoff

---

## 🚀 Quick Start

```bash
# Install
pip install pulse-network-diagnostics

# Basic check
pulse google.com

# Multiple targets with comparison
pulse google.com cloudflare.com github.com --compare

# JSON output for automation
pulse google.com --format json

# Benchmark mode (10 iterations)
pulse google.com --benchmark

# Deep analysis with all checks
pulse api.example.com --deep --checks dns,tcp,tls,http
```

---

## 📊 Example Output

### Terminal (Beautiful colors)

```
╔════════════════════════════════════════════════════════════╗
║  🔍 pulse — Network Diagnostics                            ║
╚════════════════════════════════════════════════════════════╝

  Target:  google.com

┌────────────────────────────────────────────────────────────┐
│ Results                                                     │
└────────────────────────────────────────────────────────────┘

  ▸ ✓  DNS      12 ms  »  → 142.250.180.14 (IPv4) +1 more
  ▸ ✓  TCP      45 ms  »  Connected (fast)
  ▸ ✓  TLS     165 ms  »  → TLSv1.3 • TLS_AES_256_GCM_SHA384
  ▸ ✓  HTTP    198 ms  »  → GET / → 301 → https://www.google.com/

╔════════════════════════════════════════════════════════════╗
║  ✨ All Systems Healthy ✨                                  ║
║  Total time: 420 ms                                        ║
╚════════════════════════════════════════════════════════════╝
```

### JSON (Machine-readable)

```json
[
  {
    "target": "google.com",
    "address": "google.com:443",
    "checks": [
      {
        "name": "DNS",
        "duration_ms": 12.34,
        "status": "success",
        "details": "→ 142.250.180.14 (IPv4) +1 more",
        "metadata": {
          "ips": ["142.250.180.14", "2a00:1450::200e"],
          "ipv4_count": 1,
          "ipv6_count": 1
        }
      }
    ],
    "total_duration_ms": 420.5,
    "is_healthy": true
  }
]
```

---

## 🛠️ Installation

### From PyPI (Recommended)

```bash
pip install pulse-network-diagnostics
```

### From Source

```bash
git clone https://github.com/vazor-code/pulse.git
cd pulse
pip install -e .
```

### Development Mode

```bash
pip install -e ".[dev]"
pip install -r requirements-dev.txt
```

---

## 📖 Usage

### Basic Checks

```bash
# Check a single host
pulse example.com

# Check specific port
pulse example.com:8080

# Check with URL
pulse https://api.github.com

# Check multiple targets
pulse google.com github.com cloudflare.com
```

### Output Formats

```bash
# Terminal (default, with colors)
pulse google.com

# JSON
pulse google.com --format json

# CSV
pulse google.com --format csv -o results.csv

# HTML report
pulse google.com --format html -o report.html

# Markdown
pulse google.com --format markdown

# YAML
pulse google.com --format yaml
```

### Advanced Options

```bash
# Deep analysis (certificate info, security headers)
pulse google.com --deep

# IPv6 preference
pulse google.com --ipv6

# HTTP/2 support check
pulse google.com --http2

# Custom timeout and retries
pulse google.com --timeout 30 --retries 3

# Concurrent workers
pulse target1.com target2.com target3.com --workers 5

# Quiet mode (errors only)
pulse google.com --quiet

# No colors
pulse google.com --no-color

# Verbose output
pulse google.com -v
pulse google.com -vv  # Debug level
```

### Benchmark Mode

```bash
# Run 10 iterations
pulse google.com --benchmark

# With verbose output
pulse google.com --benchmark -v
```

### Comparison Mode

```bash
# Compare multiple targets side-by-side
pulse google.com cloudflare.com github.com --compare
```

### Configuration Files

```bash
# Save current options
pulse google.com --deep --timeout 30 --save-config myconfig.json

# Load configuration
pulse google.com --config myconfig.json
```

### Reading Targets from File

```bash
# Create targets.txt with one target per line
echo "google.com
cloudflare.com
github.com" > targets.txt

# Check all targets
pulse -f targets.txt --compare
```

---

## 🏗️ Architecture

```
pulse/
├── pulse/
│   ├── __init__.py          # Main CLI entry point
│   ├── __main__.py          # Module execution
│   ├── core/                # Core components
│   │   ├── config.py        # Configuration management
│   │   ├── engine.py        # Async check engine
│   │   ├── target.py        # Target parsing
│   │   └── result.py        # Result data classes
│   ├── checks/              # Check implementations
│   │   ├── dns.py           # DNS resolution
│   │   ├── tcp.py           # TCP connectivity
│   │   ├── tls.py           # TLS/SSL handshake
│   │   └── http.py          # HTTP/HTTPS requests
│   ├── output/              # Output formatters
│   │   ├── formatters.py    # Main formatter dispatcher
│   │   └── terminal.py      # Terminal output with colors
│   └── utils/               # Utilities
│       └── logger.py        # Logging utilities
├── tests/                   # Test suite
└── docs/                    # Documentation
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pulse

# Run specific test file
pytest tests/test_pulse.py

# Run with verbose output
pytest -v
```

---

## 📋 CLI Reference

```
usage: pulse [-h] [--from-file] [--compare] [--deep] [--checks CHECKS]
             [--timeout TIMEOUT] [--retries RETRIES] [--ipv6] [--http2]
             [--follow-redirects]
             [--format {terminal,json,csv,html,markdown,yaml}]
             [--output OUTPUT] [--quiet] [--no-color] [--verbose]
             [--workers WORKERS] [--benchmark] [--config CONFIG]
             [--save-config SAVE_CONFIG] [--version]
             [targets ...]

positional arguments:
  targets               Host[:port], URL, or path to file with targets

options:
  -h, --help            show this help message and exit
  --from-file, -f       Read targets from file (one per line)
  --compare, -c         Compare multiple targets side by side
  --deep, -d            Enable deep analysis (TLS analysis, anomaly detection)
  --checks CHECKS       Comma-separated list of checks (default: dns,tcp,tls,http)
  --timeout TIMEOUT, -t TIMEOUT
                        Timeout per check in seconds (default: 10)
  --retries RETRIES, -r RETRIES
                        Number of retries for failed checks (default: 1)
  --ipv6                Prefer IPv6 over IPv4
  --http2               Check HTTP/2 support
  --follow-redirects    Follow HTTP redirects (default: True)
  --format {terminal,json,csv,html,markdown,yaml}, -o {terminal,json,csv,html,markdown,yaml}
                        Output format (default: terminal)
  --output OUTPUT, -O OUTPUT
                        Output file path (default: stdout)
  --quiet, -q           Suppress non-error output
  --no-color            Disable colored output
  --verbose, -v         Increase verbosity (use -vv for debug)
  --workers WORKERS, -w WORKERS
                        Number of concurrent workers (default: 10)
  --benchmark, -b       Run benchmark mode (10 iterations)
  --config CONFIG       Path to configuration file
  --save-config SAVE_CONFIG
                        Save current options to configuration file
  --version             show program's version number and exit
```

### Exit Codes

- `0` — All healthy (all checks passed)
- `1` — Warnings detected (performance issues)
- `2` — Failures detected (connection errors)
- `130` — Interrupted by user (Ctrl+C)

---

## 🔧 Troubleshooting

### DNS Issues

```
❌ DNS Resolution Failed
   → Run: nslookup <host>
   → Try: nslookup <host> 8.8.8.8
   → Check: /etc/resolv.conf or DNS settings
```

### TCP Connection Issues

```
❌ TCP Connection Failed
   → Service not listening on port
   → Check firewall rules
   → Run: netstat -an | grep <port>
```

### TLS Issues

```
❌ TLS Handshake Failed
   → Certificate issue or service down
   → Run: openssl s_client -connect <host>:<port>
   → Check certificate expiration
```

### HTTP Issues

```
❌ HTTP Request Failed
   → Application may be offline
   → Check service logs
   → Verify URL path
```

---

## 🤝 Contributing

Contributions are welcome! Please see `CONTRIBUTING.md` for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Setup

```bash
# Clone and setup
git clone https://github.com/vazor-code/pulse.git
cd pulse
pip install -e ".[dev]"

# Run tests
pytest

# Code formatting
black pulse tests
isort pulse tests

# Type checking
mypy pulse

# Linting
flake8 pulse tests
```

---

## 📄 License

This project is licensed under the GPL-3.0 License — see the `LICENSE` file for details.

---

## 🙏 Acknowledgments

- Inspired by the need for simple, fast network diagnostics
- Built with Python's excellent asyncio and ssl modules
- Thanks to all contributors!

---

<p align="center">
  Made with ❤️ by the pulse team
</p>
