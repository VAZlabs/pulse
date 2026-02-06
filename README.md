# 🌟 pulse — Network Diagnostics in 3 Seconds

<div align="center">

[![Release](https://img.shields.io/badge/release-1.0.0-blue.svg?style=for-the-badge&logo=github)](https://github.com/VAZlabs/pulse/releases)
[![Python](https://img.shields.io/badge/python-3.8%2B-green.svg?style=for-the-badge&logo=python)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-GPL--3.0-red.svg?style=for-the-badge&logo=gnu)](https://github.com/VAZlabs/pulse/blob/main/LICENSE)
[![Stars](https://img.shields.io/github/stars/vazor-code/pulse?style=for-the-badge&logo=github)](https://github.com/VAZlabs/pulse/stargazers)

</div>

<div align="center">

### 🚀 **The Ultimate Network Diagnostic Tool**
**DNS → TCP → TLS → HTTP** • **Dependency-Free** • **Beautiful Output** • **Machine-Friendly**

</div>

---

## 📚 Navigation Menu

<div align="center">

[✨ Demo](#-demo) • [🎯 Why pulse?](#-why-pulse) • [📦 Installation](#-installation) • [⚡ Quick Start](#-quick-start) • [💡 Examples](#-examples) • [⚙️ CLI Reference](#️-cli-reference) • [🤖 Automation](#-automation) • [🛠️ Troubleshooting](#️-troubleshooting) • [👥 Contributing](#-contributing) • [📄 License](#-license)

</div>

---

## ✨ Demo

<div align="center">

### Experience the Magic in Real-Time

</div>

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

<div align="center">

**🎯 Instantly identify network bottlenecks with beautiful, color-coded results**

</div>

---

## 🎯 Why pulse?

<div align="center">

### Comparison Matrix: Traditional vs Modern Approach

</div>

<table align="center">
  <tr>
    <th width="200">Feature</th>
    <th width="200">Traditional Tools</th>
    <th width="200">pulse</th>
  </tr>
  <tr>
    <td><strong>All-in-one</strong></td>
    <td>❌ (dig, nc, openssl, curl)</td>
    <td>✅ Single command</td>
  </tr>
  <tr>
    <td><strong>Speed</strong></td>
    <td>❌ Slow</td>
    <td>✅ 3 seconds</td>
  </tr>
  <tr>
    <td><strong>No Dependencies</strong></td>
    <td>❌ Multiple packages</td>
    <td>✅ Stdlib only</td>
  </tr>
  <tr>
    <td><strong>Actionable Output</strong></td>
    <td>❌ Raw output</td>
    <td>✅ Clear insights</td>
  </tr>
  <tr>
    <td><strong>Automation</strong></td>
    <td>⚠️ Complex parsing</td>
    <td>✅ JSON + exit codes</td>
  </tr>
  <tr>
    <td><strong>Visual Feedback</strong></td>
    <td>❌ Text-only</td>
    <td>✅ Beautiful formatting</td>
  </tr>
  <tr>
    <td><strong>Cross-Platform</strong></td>
    <td>❌ Platform-specific</td>
    <td>✅ Universal compatibility</td>
  </tr>
</table>

<br>

<div align="center">

### 🌟 Key Advantages

</div>

- 🔧 **Complete Network Chain**: Checks DNS → TCP → TLS → HTTP in one go
- ⚡ **Blazing Fast**: Optimized for speed without sacrificing accuracy
- 🧼 **Zero Dependencies**: Pure Python standard library - works everywhere
- 🎨 **Beautiful Output**: Color-coded, icon-enhanced results for humans
- 🤖 **Machine Ready**: JSON output with proper exit codes for automation
- 📊 **Detailed Insights**: Per-step timing and detailed failure information
- 🌐 **Universal**: Works on any system with Python 3.8+

---

## 📦 Installation

<div align="center">

### Choose Your Weapon

</div>

#### 🏃‍♂️ **Quick Start (No Install)**

```bash
# Direct execution from source
python pulse.py api.github.com
```

#### 🧪 **Development Mode**

```bash
# Clone and install in development mode
git clone https://github.com/VAZlabs/pulse
cd pulse
pip install -e .
pip install -r requirements-dev.txt
```

#### 🐍 **From Source**

```bash
# Download and run directly
wget https://raw.githubusercontent.com/vazor-code/pulse/main/pulse.py
python pulse.py api.github.com
```

---

## ⚡ Quick Start

<div align="center">

### Get Started in Seconds

</div>

#### 🎯 **One-Command Setup**

```bash
$ pulse api.github.com
# ✨ Beautiful output with timing and status
# Exit code: 0 (healthy) | 1 (degraded) | 2 (failed)
```

#### 🔍 **Basic Usage Examples**

```bash
# Standard HTTPS check (port 443)
pulse api.github.com

# Custom port
pulse example.com:8080

# With protocol specification
pulse https://api.github.com

# Deep analysis with extra TLS checks
pulse api.example.com --deep

# Machine-readable JSON output
pulse api.github.com --json

# Custom timeout (30 seconds)
pulse api.example.com --timeout 30
```

---

## 💡 Examples

### 🕶️ **Human-Friendly Output (Default)**

<div align="center">

*See the live demo above*

</div>

### 🔍 **Deep Analysis Mode**

```bash
$ pulse api.example.com --deep

┌──────────────────────────────────────────────────┐
│ Results                                          │
└──────────────────────────────────────────────────┘

  ▸ ✓  DNS          15 ms  »  → 93.184.221.133
  ▸ ✓  TCP          42 ms  »  → SYN → SYN-ACK → ACK
  ▸ ⚠️  TLS         287 ms  »  TLSv1.2 • ECDHE-RSA-AES256 (SLOW)
  ▸ ✓  HTTP        124 ms  »  → GET / → 200

⚡ Performance Issues Detected — TLS negotiation took longer than expected.
```

### 🤖 **JSON Output for Automation**

```json
{
  "timestamp": "2026-02-07T12:34:56Z",
  "target": "api.github.com:443",
  "checks": [
    {
      "name": "DNS",
      "duration_ms": 67.3,
      "status": "✓",
      "details": "→ 140.82.121.6",
      "success": true
    },
    {
      "name": "TCP",
      "duration_ms": 52.1,
      "status": "✓",
      "details": "→ SYN → SYN-ACK → ACK",
      "success": true
    },
    {
      "name": "TLS",
      "duration_ms": 252.4,
      "status": "✓",
      "details": "→ TLSv1.3 • TLS_AES_256_GCM_SHA384",
      "success": true
    },
    {
      "name": "HTTP",
      "duration_ms": 341.2,
      "status": "✓",
      "details": "→ GET /health → 200",
      "success": true
    }
  ],
  "total_ms": 712.0,
  "healthy": true,
  "exit_code": 0
}
```

### 📊 **Advanced JSON Processing**

```bash
# Monitor and alert
pulse api.example.com --json | jq '.healthy' | grep -q 'false' && echo "ALERT: Service down!"

# Performance tracking
pulse api.example.com --json | jq '.total_ms' > performance.log

# CI/CD integration
if ! pulse api.example.com --json --timeout 5 | jq -e '.healthy' >/dev/null; then
    echo "Service check failed"
    exit 1
fi
```

---

## ⚙️ CLI Reference

<div align="center">

### Complete Command Line Interface

</div>

```
pulse [-h] [--deep] [--json] [--timeout TIMEOUT] target

positional arguments:
  target               Host[:port] or URL to check (e.g., api.github.com)

optional arguments:
  -h, --help           Show this help message and exit
  --deep               Enable deep analysis (TLS anomaly detection)
  --json               Output JSON for scripting
  --timeout TIMEOUT    Timeout for individual checks in seconds (default: 10)
```

<div align="center">

### Exit Code Meanings

</div>

| Code | Status | Description |
|------|--------|-------------|
| `0` | ✅ Healthy | All checks passed successfully |
| `1` | ⚠️ Degraded | Warnings present, but functional |
| `2` | ❌ Failed | Critical errors detected |

---

## 🤖 Automation

<div align="center">

### Seamless Integration with Your Infrastructure

</div>

#### 📈 **Monitoring Integration**

```python
# Prometheus metrics export
import json, subprocess, sys

def get_pulse_metrics(target):
    result = subprocess.run(
        ["pulse", target, "--json"], 
        capture_output=True, 
        text=True
    )
    
    if result.returncode == 0:
        data = json.loads(result.stdout)
        return {
            'total_time': data['total_ms'],
            'healthy': data['healthy'],
            'checks': {check['name']: check['duration_ms'] for check in data['checks']}
        }
    return None

# Usage
metrics = get_pulse_metrics('api.github.com')
if metrics:
    print(f"Total time: {metrics['total_time']}ms")
    print(f"Healthy: {metrics['healthy']}")
```

#### 🔄 **CI/CD Pipeline Integration**

```yaml
# GitHub Actions example
name: Network Health Check
on: [schedule, push]
jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - name: Install pulse
        run: pip install pulse-network-diagnostics
      
      - name: Check API health
        run: |
          pulse api.github.com --timeout 15
          echo "Health check completed with exit code $?"
```

#### 📊 **Performance Monitoring**

```bash
#!/bin/bash
# Continuous monitoring script

while true; do
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    result=$(pulse api.example.com --json)
    total_time=$(echo $result | jq '.total_ms')
    healthy=$(echo $result | jq '.healthy')
    
    echo "$timestamp - $total_time ms - $healthy" >> health_monitor.log
    
    # Alert if performance degrades
    if (( $(echo "$total_time > 1000" | bc -l) )); then
        echo "⚠️ Performance degradation detected: $total_time ms"
    fi
    
    sleep 300  # Check every 5 minutes
done
```

---

## 🛠️ Troubleshooting

<div align="center">

### Common Issues & Solutions

</div>

| Check | Common Issues | Quick Fixes |
|-------|---------------|-------------|
| **DNS** | Resolution failures | Try `nslookup <host> 8.8.8.8` or verify `/etc/resolv.conf` |
| **TCP** | Connection timeouts | Check if service listens on port and firewall allows traffic |
| **TLS** | Certificate errors | Verify certificate chain and enable modern cipher suites |
| **HTTP** | Endpoint not found | Confirm application endpoint (not necessarily `/health`) |

#### 🕵️ **Diagnostic Commands**

```bash
# When pulse reports DNS issues
nslookup your-domain.com 8.8.8.8

# For TCP connectivity problems
telnet your-domain.com 443

# For TLS certificate inspection
openssl s_client -connect your-domain.com:443 -servername your-domain.com

# For HTTP endpoint verification
curl -I https://your-domain.com/
```

---

## 👥 Contributing

<div align="center">

### Join Our Community!

</div>

We welcome contributions of all kinds! Here's how to get started:

#### 📋 **Contribution Process**

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feat/amazing-feature`)
3. **Commit** changes using conventional commits (`feat: add amazing feature`)
4. **Push** to the branch (`git push origin feat/amazing-feature`)
5. **Open** a Pull Request

#### 🎯 **Commit Types We Accept**

- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation updates
- `test`: Test improvements
- `refactor`: Code restructuring
- `perf`: Performance improvements
- `chore`: Maintenance tasks

#### 🧪 **Development Setup**

```bash
# Clone the repository
git clone https://github.com/vazor-code/pulse
cd pulse

# Set up development environment
pip install -e .
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Format code
black .
isort .
```

---

## 📦 Release Information

<div align="center">

### Stay Updated

</div>

- **Latest Release**: v1.0.0
- **Repository**: [github.com/VAZlabs/pulse](https://github.com/VAZlabs/pulse)

#### 🔄 **Versioning Policy**

We follow semantic versioning (SemVer). Breaking changes will be clearly documented in release notes.

---

## 📄 License

<div align="center">

### GPL-3.0 License

</div>

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](https://github.com/VAZlabs/pulse/blob/main/LICENSE) file for complete details.

<div align="center">

---

### 💝 Made with Love for Network Diagnostics

**Star this repo** ⭐ if it helped you solve network issues faster!

</div>
