# pulse - Installation & Usage Guide

## Installation

### Option 1: Direct execution
```bash
python pulse.py <host>
```

### Option 2: pip install
```bash
pip install .
pulse api.github.com
```

### Option 3: From source
```bash
git clone https://github.com/yourname/pulse.git
cd pulse
python pulse.py <host>
```

## Quick Start

### Basic HTTPS check
```bash
pulse api.github.com
```

Output:
```
✓ DNS       67 ms  → 140.82.121.6
✓ TCP       52 ms  → SYN → SYN-ACK → ACK
✓ TLS      252 ms  → TLSv1.3 • TLS_AES_256_GCM_SHA384
✓ HTTP     341 ms  → GET /health → 200
──────────────────────────────────
Total: 712 ms • Healthy ✅
```

### Custom port
```bash
pulse example.com:8443
```

### Deep analysis (anomaly detection)
```bash
pulse api.example.com --deep
```

Output:
```
✓ DNS       19 ms  → 93.184.216.34
✓ TCP       41 ms  → SYN → SYN-ACK → ACK
⚠️ TLS      287 ms → TLSv1.2 • ECDHE-RSA-AES256-GCM-SHA384 (SLOW)
✓ HTTP     254 ms  → GET /health → 200
──────────────────────────────────
Total: 601 ms • Degraded ⚠️

💡 Quick fix suggestions:
  • Enable TLS 1.3 and session resumption on server
```

### Machine-readable output (JSON)
```bash
pulse api.github.com --json | jq '.checks[].name'
```

Output:
```json
[
  "DNS",
  "TCP",
  "TLS",
  "HTTP"
]
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All checks passed (healthy) |
| 1 | Degraded (warnings present) |
| 2 | Failed (critical error) |

Useful for scripting:
```bash
if pulse api.example.com --json > /dev/null; then
  echo "Service healthy"
else
  echo "Service down!"
fi
```

## Features

### No dependencies
pulse uses only Python standard library:
- `socket` for DNS/TCP
- `ssl` for TLS handshake
- `http.client` for HTTP requests
- `argparse` for CLI parsing

### Works on
✅ Linux (any distro with Python 3.8+)
✅ macOS (pre-installed Python)
✅ Windows (WSL or Python 3.8+)
✅ Alpine Linux (no glibc issues)

## Troubleshooting

### DNS resolution failed
```bash
# Check your DNS resolver
cat /etc/resolv.conf

# Try with public DNS
nslookup api.example.com 8.8.8.8
```

### TCP connection failed
```bash
# Check if service is running
systemctl status <service>

# Check firewall
sudo ufw status
netstat -an | grep <port>
```

### TLS handshake failed
```bash
# Debug certificate
openssl s_client -connect api.example.com:443 -showcerts

# Check expiration
openssl s_client -connect api.example.com:443 | grep -A 5 "Verify"
```

### HTTP 403/404 errors
Some services don't have a `/health` endpoint:
```bash
# Try different paths
curl -v https://api.example.com/
curl -v https://api.example.com/health
curl -v https://api.example.com/status
```

## API Reference

### Command Line Options

```
usage: pulse.py [-h] [--deep] [--json] [--timeout TIMEOUT] target

positional arguments:
  target              Host[:port] or URL to check

optional arguments:
  -h, --help          show help message
  --deep              Enable deep analysis
  --json              Output as JSON
  --timeout TIMEOUT   Timeout for checks (default: 10s)
```

### JSON Output Format

```json
{
  "target": "api.github.com:443",
  "checks": [
    {
      "name": "DNS",
      "duration_ms": 67.3,
      "status": "✓",
      "details": "→ 140.82.121.6",
      "error": null
    }
  ],
  "total_ms": 712.0,
  "healthy": true
}
```

## Development

### Running tests
```bash
python -m pytest test_pulse.py -v
```

### Code style
```bash
black pulse.py
pylint pulse.py
```

### Building distribution
```bash
python setup.py sdist bdist_wheel
```

## License
GPL-3.0 © 2026 VAZlabs
