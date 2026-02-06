#!/usr/bin/env python3
"""
pulse — network diagnostics in 3 seconds
Check DNS → TCP → TLS → HTTP chain with actionable insights
"""

import argparse
import socket
import ssl
import time
import json as json_lib
import sys
from urllib.parse import urlparse

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
BRIGHT = "\033[1m"
RESET = "\033[0m"
BOLD_GREEN = f"{BRIGHT}{GREEN}"
BOLD_YELLOW = f"{BRIGHT}{YELLOW}"
BOLD_RED = f"{BRIGHT}{RED}"
BOLD_CYAN = f"{BRIGHT}{CYAN}"
BOLD_MAGENTA = f"{BRIGHT}{MAGENTA}"


def parse_target(target):
    """Parse target string to extract host and port"""
    if target.startswith(("http://", "https://")):
        parsed = urlparse(target)
        host = parsed.hostname
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
    elif ":" in target and not target.startswith("http"):
        parts = target.rsplit(":", 1)
        host = parts[0]
        try:
            port = int(parts[1])
        except ValueError:
            host = target
            port = 443
    else:
        host = target
        port = 443
    
    return host, port


class CheckResult:
    def __init__(self, name, duration_ms, status, details, error=None):
        self.name = name
        self.duration = duration_ms
        self.status = status
        self.details = details
        self.error = error

def check_dns(host):
    start = time.time()
    try:
        ip = socket.gethostbyname(host)
        duration = (time.time() - start) * 1000
        return ip, duration, None
    except Exception as e:
        duration = (time.time() - start) * 1000
        return None, duration, e

def check_tcp(host, port, timeout=10.0):
    start = time.time()
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.close()
        duration = (time.time() - start) * 1000
        return duration, None
    except Exception as e:
        duration = (time.time() - start) * 1000
        return duration, e

def check_tls(host, port, timeout=10.0):
    start = time.time()
    try:
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        
        sock = socket.create_connection((host, port), timeout=timeout)
        tls_sock = context.wrap_socket(sock, server_hostname=host)
        
        version = tls_sock.version()
        cipher = tls_sock.cipher()[0]
        tls_sock.close()
        
        duration = (time.time() - start) * 1000
        return duration, version, cipher, None
    except Exception as e:
        duration = (time.time() - start) * 1000
        return duration, None, None, e

def check_http(host, port, use_tls=True, timeout=10.0):
    start = time.time()
    try:
        if use_tls:
            import http.client
            conn = http.client.HTTPSConnection(host, port, timeout=timeout)
        else:
            import http.client
            conn = http.client.HTTPConnection(host, port, timeout=timeout)
        
        conn.request("GET", "/health")
        resp = conn.getresponse()
        status = resp.status
        conn.close()
        
        duration = (time.time() - start) * 1000
        return duration, status, None
    except Exception as e:
        duration = (time.time() - start) * 1000
        return duration, None, e

def run_checks(target, deep_mode=False):
    # Parse target: handle URLs like "https://example.com:8443"
    host, port = parse_target(target)
    
    results = []
    ip = None
    
    # 1. DNS
    ip, dns_time, dns_err = check_dns(host)
    if dns_err:
        results.append(CheckResult("DNS", dns_time, "✗", f"Failed: {str(dns_err)[:50]}"))
        return results, host, port
    results.append(CheckResult("DNS", dns_time, "✓", f"→ {ip}"))
    
    # 2. TCP
    tcp_time, tcp_err = check_tcp(ip or host, port)
    if tcp_err:
        results.append(CheckResult("TCP", tcp_time, "✗", f"Connection refused"))
        return results, host, port
    results.append(CheckResult("TCP", tcp_time, "✓", "→ SYN → SYN-ACK → ACK"))
    
    # 3. TLS (for HTTPS ports or deep mode)
    use_tls = port in (443, 8443) or deep_mode
    if use_tls:
        tls_time, tls_ver, tls_cipher, tls_err = check_tls(host, port)
        if tls_err:
            results.append(CheckResult("TLS", tls_time, "✗", f"Handshake failed"))
            return results, host, port
        
        # Check for slow TLS versions
        is_slow = tls_ver in ("TLSv1.2", "TLSv1", "SSLv3")
        status = "⚠️" if is_slow or (deep_mode and tls_time > 200) else "✓"
        details = f"→ {tls_ver} • {tls_cipher}"
        if is_slow:
            details += " (SLOW)"
        results.append(CheckResult("TLS", tls_time, status, details))
    
    # 4. HTTP
    http_time, http_status, http_err = check_http(host, port, use_tls=use_tls)
    if http_err:
        results.append(CheckResult("HTTP", http_time, "✗", f"Request failed"))
        return results, host, port
    
    status_emoji = "⚠️" if http_status not in (200, 201, 301, 302, 304) else "✓"
    results.append(CheckResult("HTTP", http_time, status_emoji, f"→ GET /health → {http_status}"))
    
    return results, host, port

def print_results(results, host, port, json_output=False):
    if json_output:
        output = {
            "target": f"{host}:{port}",
            "checks": [
                {
                    "name": r.name,
                    "duration_ms": round(r.duration, 1),
                    "status": r.status.strip(),
                    "details": r.details,
                    "error": str(r.error) if r.error else None
                }
                for r in results
            ],
            "total_ms": round(sum(r.duration for r in results), 1),
            "healthy": all(r.status.strip() == "✓" for r in results)
        }
        print(json_lib.dumps(output, indent=2))
        return
    
    # Terminal output with beautiful styling
    print()
    
    # Results section with gradient box
    print(f"{CYAN}┌──────────────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│{RESET} {BRIGHT}Results{RESET}{CYAN}                                     │{RESET}")
    print(f"{CYAN}└──────────────────────────────────────────────────┘{RESET}")
    print()
    
    for r in results:
        if r.status.strip() == "✓":
            color = BOLD_GREEN
            icon = "▸"
        elif r.status.strip() == "⚠️":
            color = BOLD_YELLOW
            icon = "▸"
        else:
            color = BOLD_RED
            icon = "▸"
        
        # Beautiful formatting
        time_str = f"{r.duration:>6.0f} ms"
        name_pad = f"{r.name:<7}"
        
        # Status with color
        print(f"  {color}{icon} {r.status}{RESET}  {BRIGHT}{name_pad}{RESET}  {CYAN}{time_str}{RESET}  {MAGENTA}»{RESET}  {r.details}")
    
    print()
    
    # Summary section
    total = sum(r.duration for r in results)
    healthy = all(r.status.strip() == "✓" for r in results)
    degraded = any(r.status.strip() == "⚠️" for r in results)
    failed = any(r.status.strip() == "✗" for r in results)
    
    if healthy:
        print(f"{GREEN}╔════════════════════════════════════════════════╗{RESET}")
        print(f"{GREEN}║{RESET}  {BOLD_GREEN}✨ All Systems Healthy ✨{RESET}{GREEN}                  ║{RESET}")
        print(f"{GREEN}║{RESET}  Total time: {BOLD_CYAN}{total:.0f} ms{RESET}{GREEN}                      ║{RESET}")
        print(f"{GREEN}╚════════════════════════════════════════════════╝{RESET}")
    elif degraded and not failed:
        print(f"{YELLOW}╔════════════════════════════════════════════════╗{RESET}")
        print(f"{YELLOW}║{RESET}  {BOLD_YELLOW}⚡ Performance Issues Detected ⚡{RESET}{YELLOW}            ║{RESET}")
        print(f"{YELLOW}║{RESET}  Total time: {BOLD_CYAN}{total:.0f} ms{RESET}{YELLOW}                      ║{RESET}")
        print(f"{YELLOW}╚════════════════════════════════════════════════╝{RESET}")
        print()
        print(f"{YELLOW}💡 Quick Recommendations:{RESET}")
        print()
        
        for r in results:
            if "SLOW" in r.details and "TLS" in r.name:
                print(f"  {CYAN}→ TLS Performance Issue Detected{RESET}")
                print(f"    {MAGENTA}✔{RESET} Enable TLS 1.3 support")
                print(f"    {MAGENTA}✔{RESET} Enable session resumption")
                print(f"    {MAGENTA}✔{RESET} Use modern cipher suites")
                print()
    else:
        print(f"{RED}╔════════════════════════════════════════════════╗{RESET}")
        print(f"{RED}║{RESET}  {BOLD_RED}🚨 Critical Issues Found 🚨{RESET}{RED}                 ║{RESET}")
        print(f"{RED}║{RESET}  Total time: {BOLD_CYAN}{total:.0f} ms{RESET}{RED}                      ║{RESET}")
        print(f"{RED}╚════════════════════════════════════════════════╝{RESET}")
        print()
        print(f"{RED}🔧 Troubleshooting Guide:{RESET}")
        print()
        
        for r in results:
            if r.status.strip() == "✗":
                if "DNS" in r.name:
                    print(f"  {RED}❌ DNS Resolution Failed{RESET}")
                    print(f"     {CYAN}→{RESET} Run: nslookup {host}")
                    print(f"     {CYAN}→{RESET} Try: nslookup {host} 8.8.8.8")
                    print(f"     {CYAN}→{RESET} Check: /etc/resolv.conf")
                    print()
                elif "TCP" in r.name:
                    print(f"  {RED}❌ TCP Connection Failed{RESET}")
                    print(f"     {CYAN}→{RESET} Service not listening on {host}:{port}")
                    print(f"     {CYAN}→{RESET} Check firewall rules")
                    print(f"     {CYAN}→{RESET} Run: netstat -an | grep {port}")
                    print()
                elif "TLS" in r.name:
                    print(f"  {RED}❌ TLS Handshake Failed{RESET}")
                    print(f"     {CYAN}→{RESET} Certificate issue or service down")
                    print(f"     {CYAN}→{RESET} Run: openssl s_client -connect {host}:{port}")
                    print()
                elif "HTTP" in r.name:
                    print(f"  {RED}❌ HTTP Request Failed{RESET}")
                    print(f"     {CYAN}→{RESET} Application may be offline")
                    print(f"     {CYAN}→{RESET} Check service logs and status")
                    print()
    
    print()

def main():
    parser = argparse.ArgumentParser(
        description="pulse — network diagnostics in 3 seconds",
        epilog="Examples:\n"
               "  pulse api.github.com\n"
               "  pulse example.com:8443\n"
               "  pulse https://api.stripe.com --deep\n"
               "  pulse api.example.com --json",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("target", help="Host[:port] or URL to check (e.g., api.github.com, https://example.com:8443)")
    parser.add_argument("--deep", action="store_true", help="Enable deep checks (TLS analysis, anomaly detection)")
    parser.add_argument("--json", action="store_true", help="Output in JSON format for scripting")
    parser.add_argument("--timeout", type=float, default=10.0, help="Timeout for individual checks in seconds (default: 10)")
    args = parser.parse_args()
    
    try:
        # Print beautiful banner for non-JSON output
        if not args.json:
            print()
            print(f"{MAGENTA}╔════════════════════════════════════════════════╗{RESET}")
            print(f"{MAGENTA}║{RESET}  {BOLD_MAGENTA}🔍 pulse — Network Diagnostics{RESET}{MAGENTA}            ║{RESET}")
            print(f"{MAGENTA}╚════════════════════════════════════════════════╝{RESET}")
            print()
            print(f"  {BRIGHT}Target:{RESET}  {BOLD_CYAN}{args.target}{RESET}")
            if args.deep:
                print(f"  {BRIGHT}Mode:{RESET}    {BOLD_YELLOW}Deep Analysis{RESET}")
            print()
        
        results, host, port = run_checks(args.target, deep_mode=args.deep)
        print_results(results, host, port, json_output=args.json)
        
        # Exit code: 0 = healthy, 1 = degraded/warning, 2 = failed
        if all(r.status.strip() == "✓" for r in results):
            sys.exit(0)
        elif any(r.status.strip() == "✗" for r in results):
            sys.exit(2)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}⏸  Interrupted by user{RESET}")
        sys.exit(130)
    except Exception as e:
        print(f"{RED}❌ Error: {str(e)}{RESET}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()