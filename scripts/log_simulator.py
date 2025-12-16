"""
Log Simulator for SecureWatch
Generates realistic log entries for testing the SOC platform
"""
import requests
import random
import time
from datetime import datetime

API_URL = "http://localhost:8000/api/logs/ingest"

def generate_normal_traffic():
    """Generate normal traffic log"""
    return {
        "source_ip": f"192.168.1.{random.randint(1, 254)}",
        "destination_ip": f"10.0.0.{random.randint(1, 254)}",
        "log_type": random.choice(["HTTP", "DNS", "System"]),
        "raw_log": random.choice([
            "GET /api/data HTTP/1.1 200 OK",
            "GET /api/health HTTP/1.1 200 OK",
            "Query: google.com A record resolved",
            "Service nginx restarted successfully",
            "User authentication successful",
            "GET /api/users HTTP/1.1 200 OK",
        ]),
        "message": None
    }

def generate_suspicious_traffic():
    """Generate suspicious/anomalous traffic log"""
    attacks = [
        {
            "log_type": "Security",
            "raw_log": "SQL injection attempt: ' OR '1'='1' --",
            "message": "SQL injection attempt detected"
        },
        {
            "log_type": "Security",
            "raw_log": "Port scan detected on ports 1-65535",
            "message": "Port scan detected"
        },
        {
            "log_type": "SSH",
            "raw_log": "Failed password for root from 198.51.100.78 port 54321 ssh2",
            "message": "Multiple failed login attempts"
        },
        {
            "log_type": "Security",
            "raw_log": "Unusual data exfiltration: 10GB uploaded to external host",
            "message": "Large data transfer detected"
        },
        {
            "log_type": "Security",
            "raw_log": "<script>alert('XSS')</script> detected in request",
            "message": "XSS attempt detected"
        },
    ]
    
    attack = random.choice(attacks)
    return {
        "source_ip": f"203.0.113.{random.randint(1, 254)}",
        "destination_ip": "192.168.1.10",
        "log_type": attack["log_type"],
        "raw_log": attack["raw_log"],
        "message": attack["message"]
    }

def send_log(log_data):
    """Send log to API"""
    try:
        response = requests.post(API_URL, json=log_data, timeout=5)
        if response.status_code == 200:
            result = response.json()
            if result.get('is_anomaly'):
                print(f"⚠️  Anomaly detected: {log_data['raw_log'][:50]}...")
            else:
                print(f"✓  Normal log ingested: {log_data['log_type']}")
        else:
            print(f"✗  Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗  Connection error: {e}")

def main():
    """Main simulation loop"""
    print("SecureWatch Log Simulator")
    print("=" * 50)
    print(f"Sending logs to {API_URL}")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            # 90% normal, 10% suspicious
            if random.random() > 0.1:
                log = generate_normal_traffic()
            else:
                log = generate_suspicious_traffic()
            
            send_log(log)
            time.sleep(2)  # Send a log every 2 seconds
    except KeyboardInterrupt:
        print("\n\nSimulator stopped.")

if __name__ == "__main__":
    main()

