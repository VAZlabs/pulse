# pulse - Usage Examples

## Basic Checks

### Check GitHub API
```bash
$ python pulse.py api.github.com
✓ DNS       67 ms  → 140.82.121.6
✓ TCP       52 ms  → SYN → SYN-ACK → ACK
✓ TLS      252 ms  → TLSv1.3 • TLS_AES_256_GCM_SHA384
✓ HTTP     341 ms  → GET /health → 200
──────────────────────────────────
Total: 712 ms • Healthy ✅
```

Exit code: `0` (success)

### Check HTTPS service on custom port
```bash
$ python pulse.py api.stripe.com:8443
✓ DNS       45 ms  → 151.139.128.50
✓ TCP       38 ms  → SYN → SYN-ACK → ACK
✓ TLS     145 ms  → TLSv1.3 • TLS_CHACHA20_POLY1305_SHA256
✓ HTTP     89 ms  → GET /health → 200
──────────────────────────────────
Total: 317 ms • Healthy ✅
```

Exit code: `0` (success)

## Deep Analysis (Anomaly Detection)

### Detect slow TLS
```bash
$ python pulse.py api.example-legacy.com --deep
✓ DNS       19 ms  → 93.184.216.34
✓ TCP       41 ms  → SYN → SYN-ACK → ACK
⚠️ TLS      287 ms → TLSv1.2 • ECDHE-RSA-AES256-GCM-SHA384 (SLOW)
✓ HTTP     254 ms  → GET /health → 200
──────────────────────────────────
Total: 601 ms • Degraded ⚠️

💡 Quick fix suggestions:
  • Enable TLS 1.3 and session resumption on server
```

Exit code: `1` (warning)

## Machine-Readable Output

### JSON format for scripting
```bash
$ python pulse.py api.github.com --json
{
  "target": "api.github.com:443",
  "checks": [
    {
      "name": "DNS",
      "duration_ms": 67.3,
      "status": "✓",
      "details": "→ 140.82.121.6",
      "error": null
    },
    {
      "name": "TCP",
      "duration_ms": 52.1,
      "status": "✓",
      "details": "→ SYN → SYN-ACK → ACK",
      "error": null
    },
    {
      "name": "TLS",
      "duration_ms": 252.4,
      "status": "✓",
      "details": "→ TLSv1.3 • TLS_AES_256_GCM_SHA384",
      "error": null
    },
    {
      "name": "HTTP",
      "duration_ms": 341.2,
      "status": "✓",
      "details": "→ GET /health → 200",
      "error": null
    }
  ],
  "total_ms": 712.0,
  "healthy": true
}
```

### Extract specific information with jq
```bash
# Get all check names
$ python pulse.py api.github.com --json | jq '.checks[].name'
"DNS"
"TCP"
"TLS"
"HTTP"

# Get total response time
$ python pulse.py api.github.com --json | jq '.total_ms'
712.0

# Get all check times
$ python pulse.py api.github.com --json | jq '.checks[] | {name, duration_ms}'
{
  "name": "DNS",
  "duration_ms": 67.3
}
{
  "name": "TCP",
  "duration_ms": 52.1
}
...

# Check if service is healthy
$ python pulse.py api.github.com --json | jq '.healthy'
true
```

## Error Cases

### DNS resolution failed
```bash
$ python pulse.py nonexistent-domain-12345.com
✗ DNS       234 ms → Failed: [Errno -2] Name or service not known
──────────────────────────────────
Total: 234 ms • Failed ❌

💡 Troubleshooting steps:
  • DNS Resolution Failed:
    - Check DNS resolver: cat /etc/resolv.conf
    - Try public DNS: nslookup nonexistent-domain-12345.com 8.8.8.8
    - Verify hostname is correct
```

Exit code: `2` (error)

### TCP connection refused
```bash
$ python pulse.py localhost:65432
✓ DNS       12 ms  → 127.0.0.1
✗ TCP       234 ms → Connection refused after 0.2s
──────────────────────────────────
Total: 246 ms • Failed ❌

💡 Troubleshooting steps:
  • TCP Connection Failed:
    - Is service running? Check port listening: netstat -an | grep 65432
    - Check firewall rules: sudo ufw status
    - Verify correct host and port combination
```

Exit code: `2` (error)

### TLS handshake failed
```bash
$ python pulse.py expired-cert.example.com
✓ DNS       45 ms  → 93.184.216.34
✓ TCP       38 ms  → SYN → SYN-ACK → ACK
✗ TLS      123 ms → Handshake failed: certificate verify failed
──────────────────────────────────
Total: 206 ms • Failed ❌

💡 Troubleshooting steps:
  • TLS Handshake Failed:
    - Check certificate validity: openssl s_client -connect expired-cert.example.com:443
    - Verify certificate is not expired
    - Check certificate chain completeness
```

Exit code: `2` (error)

## Scripting Examples

### Monitor service health in cron
```bash
#!/bin/bash
# health-check.sh

SERVICE="api.myapp.com"
LOG="/var/log/health-check.log"

if python pulse.py $SERVICE --json >> $LOG 2>&1; then
    echo "$(date): $SERVICE is healthy" | tee -a $LOG
    exit 0
else
    echo "$(date): $SERVICE is unhealthy - sending alert" | tee -a $LOG
    # Send alert to monitoring system
    curl -X POST https://alerts.example.com/api/incident \
        -d "service=$SERVICE&status=down"
    exit 1
fi
```

### Check multiple services
```bash
#!/bin/bash
# multi-check.sh

services=(
    "api.github.com"
    "api.stripe.com"
    "api.example.com:8443"
    "internal-service.local"
)

for service in "${services[@]}"; do
    echo "Checking $service..."
    python pulse.py "$service" --json
    echo ""
done
```

### Parse JSON response with Python
```python
import json
import subprocess

result = subprocess.run(
    ["python", "pulse.py", "api.github.com", "--json"],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)
print(f"Service: {data['target']}")
print(f"Health: {'✅' if data['healthy'] else '❌'}")
print(f"Total time: {data['total_ms']:.0f}ms")

for check in data['checks']:
    print(f"  {check['name']:6} {check['duration_ms']:>5.0f}ms - {check['status']}")
```

### Integration with monitoring systems

#### Send to Prometheus
```python
from prometheus_client import Gauge, CollectorRegistry, push_to_gateway
import subprocess
import json

registry = CollectorRegistry()
duration = Gauge('pulse_duration_ms', 'Check duration', ['target', 'check'], registry=registry)
healthy = Gauge('pulse_healthy', 'Service healthy', ['target'], registry=registry)

result = subprocess.run(
    ["python", "pulse.py", "api.github.com", "--json"],
    capture_output=True, text=True
)
data = json.loads(result.stdout)

for check in data['checks']:
    duration.labels(target=data['target'], check=check['name']).set(check['duration_ms'])

healthy.labels(target=data['target']).set(1 if data['healthy'] else 0)
push_to_gateway('localhost:9091', job='pulse', registry=registry)
```

#### Send to InfluxDB
```bash
#!/bin/bash
# Send pulse results to InfluxDB

SERVICE="api.github.com"
INFLUX_URL="http://influxdb:8086"
INFLUX_DB="monitoring"

RESULT=$(python pulse.py $SERVICE --json)
TOTAL=$(echo $RESULT | jq '.total_ms')
HEALTHY=$(echo $RESULT | jq '.healthy' | awk '{print ($1=="true")?1:0}')

curl -X POST "$INFLUX_URL/write?db=$INFLUX_DB" \
    --data-binary "pulse,service=$SERVICE total=$TOTAL,healthy=$HEALTHY"
```

## Performance Tips

### Reduce timeout for faster checks
```bash
$ python pulse.py api.github.com --timeout 5
```

### Parallel checking multiple services
```bash
# Using GNU parallel
cat services.txt | parallel python pulse.py {} --json

# Using xargs
cat services.txt | xargs -I {} -P 4 python pulse.py {} --json
```

### Batch checking with aggregation
```bash
#!/bin/bash
for service in $(cat services.txt); do
    python pulse.py $service --json
done | jq -s 'map({target, healthy, total_ms}) | sort_by(.total_ms) | reverse'
```
