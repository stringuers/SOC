# Scripts

## log_simulator.py

Generates realistic log entries for testing the SOC platform.

### Usage

```bash
# Make sure the backend is running
python scripts/log_simulator.py
```

The simulator will:
- Generate 90% normal traffic logs
- Generate 10% suspicious/anomalous traffic logs
- Send logs to the API every 2 seconds
- Display when anomalies are detected

### Requirements

- Backend API running on http://localhost:8000
- `requests` library installed: `pip install requests`

