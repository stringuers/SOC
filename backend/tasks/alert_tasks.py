from celery_app import celery_app
from services.ml_service import extract_features
from services.threat_intel_service import ThreatIntelligence
from services.playbook_service import PlaybookEngine
from models import Alert, SeverityLevel, AlertStatus
from database import SessionLocal
import traceback

threat_intel = ThreatIntelligence()
playbook_engine = PlaybookEngine()

def calculate_severity(confidence: float) -> SeverityLevel:
    """Calculate alert severity based on confidence score"""
    if confidence > 0.8:
        return SeverityLevel.CRITICAL
    elif confidence > 0.6:
        return SeverityLevel.HIGH
    elif confidence > 0.4:
        return SeverityLevel.MEDIUM
    else:
        return SeverityLevel.LOW

def detect_threat_type(raw_log: str) -> str:
    """Detect threat type from log content"""
    raw_log_lower = raw_log.lower()
    
    if any(kw in raw_log_lower for kw in ['sql', 'union', 'select', "' or '1'='1", '--']):
        return 'sql_injection'
    elif 'failed login' in raw_log_lower or 'brute force' in raw_log_lower:
        return 'brute_force'
    elif any(kw in raw_log_lower for kw in ['exfiltrat', 'large data', 'gb', 'mb']):
        return 'data_exfiltration'
    elif 'port scan' in raw_log_lower:
        return 'port_scan'
    else:
        return 'unknown'

@celery_app.task
def analyze_log_and_create_alert(log_data: dict):
    """Analyze log and create alert if anomaly detected"""
    try:
        db = SessionLocal()
        
        # Extract threat type
        threat_type = detect_threat_type(log_data.get('raw_log', ''))
        
        # Create alert
        alert = Alert(
            title=f"Anomaly detected from {log_data.get('source_ip', 'unknown')}",
            description=f"Suspicious activity detected: {log_data.get('raw_log', '')[:200]}",
            severity=calculate_severity(log_data.get('confidence', 0.5)),
            source="ML Engine",
            source_ip=log_data.get('source_ip'),
            status=AlertStatus.OPEN,
            category=threat_type.replace('_', ' ').title(),
            anomaly_score=str(log_data.get('anomaly_score', 0))
        )
        
        # Enrich with threat intelligence
        if log_data.get('source_ip'):
            intel = threat_intel.check_ip_reputation(log_data['source_ip'])
            alert.threat_intel = intel
        
        db.add(alert)
        db.commit()
        alert_id = alert.id
        db.refresh(alert)
        
        # Execute playbook if threat type is known
        if threat_type != 'unknown':
            try:
                playbook_results = playbook_engine.execute_playbook(threat_type, {
                    'source_ip': log_data.get('source_ip'),
                    'alert_id': alert_id,
                    'log_data': log_data
                })
                # Store playbook results in alert or incident
            except Exception as e:
                print(f"Playbook execution error: {e}")
        
        db.close()
        
        return {"alert_created": True, "alert_id": alert_id, "threat_type": threat_type}
    except Exception as e:
        print(f"Error creating alert: {e}")
        print(traceback.format_exc())
        return {"alert_created": False, "error": str(e)}

@celery_app.task
def send_alert_notification(alert_id: int):
    """Send email/slack notification for critical alerts"""
    # Implementation for notifications
    # This would integrate with email/Slack APIs
    print(f"Notification sent for alert {alert_id}")
    return {"status": "sent", "alert_id": alert_id}

