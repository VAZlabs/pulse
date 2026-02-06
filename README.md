<!--
  README.md — polished project landing
  - Clear header and badges
  - Table of contents for easy navigation
  - Highlighted quick start and beautiful output examples
  - CLI reference, JSON usage, automation tips and troubleshooting
-->

# pulse — Network Diagnostics in 3 Seconds

![Release](https://img.shields.io/badge/release-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)
![License](https://img.shields.io/badge/license-GPL--3.0-red.svg)

> A tiny, dependency-free CLI that checks the full networking chain — DNS → TCP → TLS → HTTP — and presents actionable, beautifully formatted results for humans and machines.

---

## Table of Contents

- [Demo](#demo)
- [Why pulse?](#why-pulse)
- [Install](#install)
- [Quick Start](#quick-start)
- [Examples](#examples)
- [CLI Reference](#cli-reference)
- [JSON / Automation](#json--automation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Demo

Run `pulse` and enjoy an instantly readable report with colors, icons and advice.

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

This output is intentionally compact and color-coded so you can scan for issues at a glance.

---

## Why pulse?

Pulse fills the gap between low-level tools and human-friendly insight.

- Single command that replaces a pipeline of `dig`/`nc`/`openssl`/`curl` calls
- Fast: completes within a few hundred milliseconds on typical networks
- Zero runtime dependencies — pure Python stdlib
- Machine-friendly JSON + meaningful exit codes for automation

---

## Install

Pick how you want to use it:

- Quick (no install):

```bash
python pulse.py <target>
```

- Global install (recommended for convenience):

```powershell
pip install .
pulse api.github.com
```

- Development mode:

```bash
pip install -e .
pip install -r requirements-dev.txt
```

---

## Quick Start

Basic check (defaults to HTTPS / port 443):

```bash
pulse api.github.com
```

Deep analysis (enable extra TLS checks):

```bash
pulse api.example.com --deep
```

Get machine-readable output:

```bash
pulse api.github.com --json
```

Adjust per-check timeout (seconds):

```bash
pulse api.example.com --timeout 30
```

---

## Examples

### Fast (human) output

See demo above — the human output shows each step with timing and a friendly status.

### Deep analysis (detect slow TLS)

```bash
pulse api.example.com --deep

┌──────────────────────────────────────────────────┐
│ Results                                          │
└──────────────────────────────────────────────────┘

  ▸ ⚠️  TLS         287 ms  »  TLSv1.2 • ECDHE-RSA-AES256 (SLOW)

⚡ Performance Issues Detected — advice provided below.
```

### JSON output (for automation)

```json
{
  "target": "api.github.com:443",
  "checks": [
    {"name":"DNS","duration_ms":67.3,"status":"✓","details":"→ 140.82.121.6"},
    {"name":"TCP","duration_ms":52.1,"status":"✓","details":"→ SYN → SYN-ACK → ACK"},
    {"name":"TLS","duration_ms":252.4,"status":"✓","details":"→ TLSv1.3 • TLS_AES_256_GCM_SHA384"},
    {"name":"HTTP","duration_ms":341.2,"status":"✓","details":"→ GET /health → 200"}
  ],
  "total_ms":712.0,
  "healthy":true
}
```

---

## CLI Reference

```
usage: pulse [-h] [--deep] [--json] [--timeout TIMEOUT] target

positional arguments:
  target               Host[:port] or URL to check (e.g. api.github.com)

optional arguments:
  -h, --help           show this help message and exit
  --deep               enable deep analysis (TLS anomaly detection)
  --json               output JSON for scripting
  --timeout TIMEOUT    timeout for individual checks in seconds (default: 10)
```

Exit codes:

- `0` — healthy (all checks passed)
- `1` — degraded (warnings present)
- `2` — failed (critical error)

---

## JSON & Automation

Pulse produces compact JSON suitable for pipelines and monitoring. Use the `--json` flag and parse fields such as `total_ms`, `healthy` and individual check durations.

Example: send results to Prometheus Pushgateway (conceptual):

```python
import json, subprocess
res = subprocess.run(["pulse","api.github.com","--json"], capture_output=True, text=True)
data = json.loads(res.stdout)
print(data['total_ms'], data['healthy'])
```

---

## Troubleshooting & Quick Fixes

If a check fails, pulse prints concise, actionable suggestions. Common cases:

- DNS: try public DNS (`nslookup <host> 8.8.8.8`) or verify `/etc/resolv.conf`.
- TCP: ensure service listens on port and firewall allows traffic.
- TLS: check certificate chain and enable TLS1.3 / modern ciphers.
- HTTP: verify application endpoint (maybe not `/health`).

If you need more detail, run the specific diagnostic commands suggested by the output (e.g. `openssl s_client -connect host:443`).

---

## Contributing

Contributions welcome — see `CONTRIBUTING.md` for the workflow, testing and code style. Keep commits focused, include tests for new behavior and follow the conventional commit types: `feat`, `fix`, `docs`, `chore`, etc.

---

## Release & changelog

We tag releases and publish to PyPI. Bump `version` in `setup.py` and update `CHANGELOG.md` when preparing a release.

---

## License

This project is released under the **GPL-3.0** license — see `LICENSE` for details.

---

If you'd like, I can now commit this change (suggested commit message: `docs: Polish README with rich examples and TOC`).
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

<!--
  README.md — polished project landing
  - Clear header and badges
  - Table of contents for easy navigation
  - Highlighted quick start and beautiful output examples
  - CLI reference, JSON usage, automation tips and troubleshooting
-->

# pulse — Network Diagnostics in 3 Seconds

![Release](https://img.shields.io/badge/release-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)
![License](https://img.shields.io/badge/license-GPL--3.0-red.svg)

> A tiny, dependency-free CLI that checks the full networking chain — DNS → TCP → TLS → HTTP — and presents actionable, beautifully formatted results for humans and machines.

---

## Table of Contents

- [Demo](#demo)
- [Why pulse?](#why-pulse)
- [Install](#install)
- [Quick Start](#quick-start)
- [Examples](#examples)
- [CLI Reference](#cli-reference)
- [JSON / Automation](#json--automation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Demo

Run `pulse` and enjoy an instantly readable report with colors, icons and advice.

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

This output is intentionally compact and color-coded so you can scan for issues at a glance.

---

## Why pulse?

Pulse fills the gap between low-level tools and human-friendly insight.

- Single command that replaces a pipeline of `dig`/`nc`/`openssl`/`curl` calls
- Fast: completes within a few hundred milliseconds on typical networks
- Zero runtime dependencies — pure Python stdlib
- Machine-friendly JSON + meaningful exit codes for automation

---

## Install

Pick how you want to use it:

- Quick (no install):

```bash
python pulse.py <target>
```

- Global install (recommended for convenience):

```powershell
pip install .
pulse api.github.com
```

- Development mode:

```bash
pip install -e .
pip install -r requirements-dev.txt
```

---

## Quick Start

Basic check (defaults to HTTPS / port 443):

```bash
pulse api.github.com
```

Deep analysis (enable extra TLS checks):

```bash
pulse api.example.com --deep
```

Get machine-readable output:

```bash
pulse api.github.com --json
```

Adjust per-check timeout (seconds):

```bash
pulse api.example.com --timeout 30
```

---

## Examples

### Fast (human) output

See demo above — the human output shows each step with timing and a friendly status.

### Deep analysis (detect slow TLS)

```bash
pulse api.example.com --deep

┌──────────────────────────────────────────────────┐
│ Results                                          │
└──────────────────────────────────────────────────┘

  ▸ ⚠️  TLS         287 ms  »  TLSv1.2 • ECDHE-RSA-AES256 (SLOW)

⚡ Performance Issues Detected — advice provided below.
```

### JSON output (for automation)

```json
{
  "target": "api.github.com:443",
  "checks": [
    {"name":"DNS","duration_ms":67.3,"status":"✓","details":"→ 140.82.121.6"},
    {"name":"TCP","duration_ms":52.1,"status":"✓","details":"→ SYN → SYN-ACK → ACK"},
    {"name":"TLS","duration_ms":252.4,"status":"✓","details":"→ TLSv1.3 • TLS_AES_256_GCM_SHA384"},
    {"name":"HTTP","duration_ms":341.2,"status":"✓","details":"→ GET /health → 200"}
  ],
  "total_ms":712.0,
  "healthy":true
}
```

---

## CLI Reference

```
usage: pulse [-h] [--deep] [--json] [--timeout TIMEOUT] target

positional arguments:
  target               Host[:port] or URL to check (e.g. api.github.com)

optional arguments:
  -h, --help           show this help message and exit
  --deep               enable deep analysis (TLS anomaly detection)
  --json               output JSON for scripting
  --timeout TIMEOUT    timeout for individual checks in seconds (default: 10)
```

Exit codes:

- `0` — healthy (all checks passed)
- `1` — degraded (warnings present)
- `2` — failed (critical error)

---

## JSON & Automation

Pulse produces compact JSON suitable for pipelines and monitoring. Use the `--json` flag and parse fields such as `total_ms`, `healthy` and individual check durations.

Example: send results to Prometheus Pushgateway (conceptual):

```python
import json, subprocess
res = subprocess.run(["pulse","api.github.com","--json"], capture_output=True, text=True)
data = json.loads(res.stdout)
print(data['total_ms'], data['healthy'])
```

---

## Troubleshooting & Quick Fixes

If a check fails, pulse prints concise, actionable suggestions. Common cases:

- DNS: try public DNS (`nslookup <host> 8.8.8.8`) or verify `/etc/resolv.conf`.
- TCP: ensure service listens on port and firewall allows traffic.
- TLS: check certificate chain and enable TLS1.3 / modern ciphers.
- HTTP: verify application endpoint (maybe not `/health`).

If you need more detail, run the specific diagnostic commands suggested by the output (e.g. `openssl s_client -connect host:443`).

---

## Contributing

Contributions welcome — see `CONTRIBUTING.md` for the workflow, testing and code style. Keep commits focused, include tests for new behavior and follow the conventional commit types: `feat`, `fix`, `docs`, `chore`, etc.

---

## License

This project is released under the **GPL-3.0** license — see `LICENSE` for details.