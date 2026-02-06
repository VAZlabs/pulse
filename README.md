# pulse — Network Diagnostics in 3 Seconds

Check DNS → TCP → TLS → HTTP chain with actionable insights. **No dependencies. Works on bare servers.**

```bash
$ pulse api.github.com

╔════════════════════════════════════════════════╗
║  🔍 pulse — Network Diagnostics            ║
╚════════════════════════════════════════════════╝

  Target:  api.github.com
  Mode:    Fast Check

┌──────────────────────────────────────────────────┐
│ Results                                     │
└──────────────────────────────────────────────────┘

  ▸ ✓  DNS          12 ms  »  → 140.82.121.6
  ▸ ✓  TCP          51 ms  »  → SYN → SYN-ACK → ACK
  ▸ ✓  TLS         240 ms  »  → TLSv1.3 • TLS_AES_128_GCM_SHA256
  ▸ ✓  HTTP        242 ms  »  → GET /health → 200

╔════════════════════════════════════════════════╗
║  ✨ All Systems Healthy ✨                 ║
║  Total time: 544 ms                      ║
╚════════════════════════════════════════════════╝
```

## Why pulse?

| Feature | Traditional tools | pulse |
|---------|-------------------|-------|
| All-in-one | ❌ (dig, nc, openssl, curl) | ✅ Single command |
| Speed | ❌ Slow | ✅ 3 seconds |
| No deps | ❌ Multiple packages | ✅ Stdlib only |
| Actionable | ❌ Raw output | ✅ Clear insights |
| Automation | ⚠️ Complex parsing | ✅ JSON + exit codes |

## Quick Start

### Installation

```bash
# Global installation
pip install pulse-network-diagnostics
pulse api.github.com

# Or use directly (no install)
python pulse.py api.github.com

# Or with git clone
git clone https://github.com/vazor-code/pulse
cd pulse
python pulse.py api.github.com
```

### One-Second Quickstart

```bash
$ pulse api.github.com
# ✨ Beautiful output with timing and status
# Exit code: 0 (healthy) or 1 (degraded) or 2 (failed)
```

## Features

✅ **Complete Diagnostics** - All-in-one: DNS → TCP → TLS → HTTP
  - Resolves hostname to IP
  - Tests port connectivity
  - Validates SSL certificate
  - Checks HTTP health endpoint

✅ **Beautiful Output** - Color-coded results with boxes and emojis
  - Green (✓) for success
  - Yellow (⚠️) for warnings/degraded
  - Red (✗) for critical failures
  - Timing info for each step

✅ **Performance Metrics** - Know exactly where delays happen
  - Individual timing per check (DNS, TCP, TLS, HTTP)
  - Total execution time
  - Anomaly detection (slow TLS versions)

✅ **Automation-Friendly**
  - JSON output: `--json` flag
  - Exit codes: 0=healthy, 1=degraded, 2=failed
  - Works in scripts and monitoring

✅ **Zero Dependencies** - Pure Python stdlib
  - socket, ssl, http.client, argparse, json
  - No pip package overhead
  - Works on bare servers with minimal Python

✅ **Cross-Platform**
  - Linux, macOS, Windows (native & WSL)
  - Alpine Linux (no glibc required)
  - Tested on Python 3.8+

## Examples

### Basic Check
```bash
$ pulse api.github.com

╔════════════════════════════════════════════════╗
║  🔍 pulse — Network Diagnostics                ║
╚════════════════════════════════════════════════╝

  Target:  api.github.com

┌──────────────────────────────────────────────────┐
│ Results                                          │
└──────────────────────────────────────────────────┘

  ▸ ✓  DNS          12 ms  »  → 140.82.121.6
  ▸ ✓  TCP          51 ms  »  → SYN → SYN-ACK → ACK
  ▸ ✓  TLS         240 ms  »  → TLSv1.3 • TLS_AES_256_GCM_SHA384
  ▸ ✓  HTTP        242 ms  »  → GET /health → 200

╔════════════════════════════════════════════════╗
║  ✨ All Systems Healthy ✨                    ║
║  Total time: 544 ms                            ║
╚════════════════════════════════════════════════╝
```

### Deep Analysis (Detects Slow TLS)
```bash
$ pulse api.example.com --deep

╔════════════════════════════════════════════════╗
║  🔍 pulse — Network Diagnostics                ║
╚════════════════════════════════════════════════╝

  Target:  api.example.com
  Mode:    Deep Analysis

┌──────────────────────────────────────────────────┐
│ Results                                          │
└──────────────────────────────────────────────────┘

  ▸ ✓  DNS          19 ms  »  → 93.184.216.34
  ▸ ✓  TCP          41 ms  »  → SYN → SYN-ACK → ACK
  ▸ ⚠️  TLS         287 ms  »  → TLSv1.2 • ECDHE-RSA-AES256 (SLOW)
  ▸ ✓  HTTP        254 ms  »  → GET /health → 200

╔════════════════════════════════════════════════╗
║  ⚡ Performance Issues Detected ⚡            ║
║  Total time: 601 ms                            ║
╚════════════════════════════════════════════════╝

💡 Quick Recommendations:

  → TLS Performance Issue Detected
    ✔ Enable TLS 1.3 support
    ✔ Enable session resumption
    ✔ Use modern cipher suites
```

### JSON Output
```bash
$ python pulse.py api.github.com --json
{
  "target": "api.github.com:443",
  "checks": [
    {"name": "DNS", "duration_ms": 67.3, "status": "✓", "details": "→ 140.82.121.6"},
    {"name": "TCP", "duration_ms": 52.1, "status": "✓", "details": "→ SYN → SYN-ACK → ACK"},
    {"name": "TLS", "duration_ms": 252.4, "status": "✓", "details": "→ TLSv1.3 • TLS_AES_256_GCM_SHA384"},
    {"name": "HTTP", "duration_ms": 341.2, "status": "✓", "details": "→ GET /health → 200"}
  ],
  "total_ms": 712.0,
  "healthy": true
}
```

### Scripting
```bash
# Check if service is healthy
if python pulse.py api.example.com --json > /dev/null; then
  echo "✅ Service is healthy"
else
  echo "❌ Service is down"
fi

# Parse JSON response
result=$(python pulse.py api.github.com --json)
echo "Total time: $(echo $result | jq '.total_ms') ms"
echo "Healthy: $(echo $result | jq '.healthy')"
```

## Exit Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| 0 | All checks passed (healthy) | Success, continue |
| 1 | Degraded (warnings present) | Issues detected, investigate |
| 2 | Failed (critical error) | Service down, alert |

Perfect for automation:
```bash
python pulse.py api.example.com
case $? in
  0) echo "Healthy" ;;
  1) echo "Degraded" ;;
  2) echo "Failed" ;;
esac
```

## CLI Reference

```bash
usage: pulse [-h] [--deep] [--json] [--timeout TIMEOUT] target

positional arguments:
  target               Host[:port] or URL to check
                       Examples: api.github.com
                                 example.com:8443
                                 https://api.stripe.com:8443

optional arguments:
  -h, --help           Show this help message
  --deep               Deep analysis mode (enables TLS version detection)
  --json               Output results as JSON (for scripting)
  --timeout TIMEOUT    Timeout per check in seconds (default: 10)

examples:
  pulse api.github.com
  pulse example.com:8443 --deep
  pulse https://stripe.com --json
  pulse slow-api.local --timeout 30
```

## Documentation

- **INSTALL.md** - Detailed installation guide
- **EXAMPLES.md** - More examples and recipes
- **CONTRIBUTING.md** - How to contribute
- **QUICKREF.txt** - Quick reference

## Development

```bash
# Install for development
pip install -e .
pip install -r requirements-dev.txt

# Run tests
python -m pytest test_pulse.py -v

# Format code
black pulse.py

# Clean artifacts
make clean
```

## Project Structure

```
pulse/
├── pulse.py           Main application (~300 lines)
├── test_pulse.py      Unit tests
├── setup.py           Pip configuration
├── __main__.py        Entry point
├── Makefile           Development commands
├── README.md          This file
├── INSTALL.md         Installation guide
├── EXAMPLES.md        Detailed examples
├── CONTRIBUTING.md    Development guidelines
├── requirements.txt   Dependencies (none!)
└── LICENSE            GPL-3.0
```

## FAQ

**Q: How fast is it?**  
A: Typically 300-1000ms depending on network latency.

**Q: Does it need internet?**  
A: Only to check the remote service. Works offline for local diagnostics.

**Q: Can I integrate with monitoring?**  
A: Yes! Use `--json` output with Prometheus, InfluxDB, Grafana, etc.

**Q: What if `/health` endpoint doesn't exist?**  
A: It just returns the HTTP status code. 404 is still valid feedback.

**Q: Can I check multiple services?**  
A: Yes! Loop in bash or use parallel execution:
```bash
for host in api.github.com api.stripe.com; do
  python pulse.py $host
done
```

**Q: How do I use with cron?**  
A: Schedule checks and parse exit codes:
```bash
0 * * * * python pulse.py api.example.com --json >> /var/log/health.json
```

## Troubleshooting

### DNS fails
```bash
# Check your DNS
nslookup api.example.com
# Try public DNS
nslookup api.example.com 8.8.8.8
```

### TCP connection refused
```bash
# Check if port is listening
netstat -an | grep <port>
# Check firewall
sudo ufw status
```

### TLS certificate error
```bash
# Check certificate details
openssl s_client -connect api.example.com:443 -showcerts
# Check expiration
openssl s_client -connect api.example.com:443 | grep -A 5 "Verify"
```

### Slow responses
```bash
# Increase timeout
python pulse.py api.example.com --timeout 30
# Check network
ping api.example.com
traceroute api.example.com
```

## License

**GPL-3.0** - Free software. See LICENSE file.

## Contributing

Found a bug? Want to add a feature? See CONTRIBUTING.md.

---

**Ready to use!** `python pulse.py api.github.com`