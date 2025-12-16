from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from database import get_db
from models import LogEntry, SeverityLevel
from services.elasticsearch_service import index_log
from services.ml_service import detector, extract_features
from tasks.alert_tasks import analyze_log_and_create_alert

# Import manager function - will be set by main.py
_manager = None

def set_manager(manager):
    """Set the WebSocket manager from main.py"""
    global _manager
    _manager = manager

def get_manager():
    """Get the WebSocket manager"""
    return _manager

router = APIRouter(prefix="/api/logs", tags=["logs"])

class LogCreate(BaseModel):
    source_ip: str
    destination_ip: str
    log_type: str
    raw_log: str
    message: Optional[str] = None

class LogResponse(BaseModel):
    id: int
    source_ip: str
    destination_ip: str
    timestamp: datetime
    log_type: str
    message: str
    severity: str
    is_anomaly: bool
    anomaly_score: Optional[str] = None

    class Config:
        from_attributes = True

@router.post("/ingest", response_model=LogResponse)
async def ingest_log(log: LogCreate, db: Session = Depends(get_db)):
    """Ingest a log entry and analyze it for anomalies"""
    try:
        # Extract features for ML analysis
        features = extract_features({
            'timestamp': datetime.utcnow(),
            'source_ip': log.source_ip,
            'destination_ip': log.destination_ip,
            'raw_log': log.raw_log
        })
        
        # Run ML prediction
        prediction = detector.predict(features)
        
        # Determine severity based on anomaly detection
        severity = SeverityLevel.LOW
        if prediction['is_anomaly']:
            if prediction['confidence'] > 0.8:
                severity = SeverityLevel.CRITICAL
            elif prediction['confidence'] > 0.6:
                severity = SeverityLevel.HIGH
            elif prediction['confidence'] > 0.4:
                severity = SeverityLevel.MEDIUM
            else:
                severity = SeverityLevel.LOW
        
        # Create log entry in database
        db_log = LogEntry(
            source_ip=log.source_ip,
            destination_ip=log.destination_ip,
            timestamp=datetime.utcnow(),
            log_type=log.log_type,
            raw_log=log.raw_log,
            message=log.message or log.raw_log,
            severity=severity,
            is_anomaly=prediction['is_anomaly'],
            anomaly_score=str(prediction['anomaly_score']),
            parsed_data={
                'features': features,
                'prediction': prediction
            }
        )
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        
        # Index in Elasticsearch
        try:
            index_log({
                'timestamp': db_log.timestamp.isoformat(),
                'source_ip': db_log.source_ip,
                'destination_ip': db_log.destination_ip,
                'log_type': db_log.log_type,
                'raw_log': db_log.raw_log,
                'message': db_log.message,
                'severity': db_log.severity.value if db_log.severity else 'low'
            })
        except Exception as e:
            print(f"Elasticsearch indexing error: {e}")
        
        # Send to background task for alert generation if anomaly
        if prediction['is_anomaly']:
            analyze_log_and_create_alert.delay({
                'log_id': db_log.id,
                'source_ip': log.source_ip,
                'destination_ip': log.destination_ip,
                'raw_log': log.raw_log,
                'log_type': log.log_type,
                'anomaly_score': prediction['anomaly_score'],
                'confidence': prediction['confidence']
            })
        
        # Broadcast via WebSocket
        manager = get_manager()
        await manager.broadcast({
            'type': 'new_log',
            'data': {
                'id': db_log.id,
                'source_ip': db_log.source_ip,
                'destination_ip': db_log.destination_ip,
                'log_type': db_log.log_type,
                'message': db_log.message,
                'severity': db_log.severity.value if db_log.severity else 'low',
                'is_anomaly': db_log.is_anomaly,
                'timestamp': db_log.timestamp.isoformat()
            }
        })
        
        return LogResponse(
            id=db_log.id,
            source_ip=db_log.source_ip,
            destination_ip=db_log.destination_ip,
            timestamp=db_log.timestamp,
            log_type=db_log.log_type,
            message=db_log.message,
            severity=db_log.severity.value if db_log.severity else 'low',
            is_anomaly=db_log.is_anomaly,
            anomaly_score=db_log.anomaly_score
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[LogResponse])
async def get_logs(
    skip: int = 0,
    limit: int = 100,
    severity: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get logs with optional filtering"""
    query = db.query(LogEntry)
    
    if severity:
        try:
            severity_enum = SeverityLevel[severity.upper()]
            query = query.filter(LogEntry.severity == severity_enum)
        except KeyError:
            pass
    
    logs = query.order_by(LogEntry.timestamp.desc()).offset(skip).limit(limit).all()
    return [
        LogResponse(
            id=log.id,
            source_ip=log.source_ip,
            destination_ip=log.destination_ip,
            timestamp=log.timestamp,
            log_type=log.log_type,
            message=log.message or log.raw_log,
            severity=log.severity.value if log.severity else 'low',
            is_anomaly=log.is_anomaly,
            anomaly_score=log.anomaly_score
        )
        for log in logs
    ]

@router.get("/{log_id}", response_model=LogResponse)
async def get_log(log_id: int, db: Session = Depends(get_db)):
    """Get a specific log entry"""
    log = db.query(LogEntry).filter(LogEntry.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    
    return LogResponse(
        id=log.id,
        source_ip=log.source_ip,
        destination_ip=log.destination_ip,
        timestamp=log.timestamp,
        log_type=log.log_type,
        message=log.message or log.raw_log,
        severity=log.severity.value if log.severity else 'low',
        is_anomaly=log.is_anomaly,
        anomaly_score=log.anomaly_score
    )

