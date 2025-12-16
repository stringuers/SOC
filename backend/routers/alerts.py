from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
from models import Alert, SeverityLevel, AlertStatus

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

class AlertResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    severity: str
    source: Optional[str]
    source_ip: Optional[str]
    timestamp: str
    status: str
    is_resolved: bool
    assigned_to: Optional[str]
    category: Optional[str]
    anomaly_score: Optional[str] = None

    class Config:
        from_attributes = True

class AlertUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    is_resolved: Optional[bool] = None

@router.get("/", response_model=List[AlertResponse])
async def get_alerts(
    skip: int = 0,
    limit: int = 100,
    severity: Optional[str] = None,
    status: Optional[str] = None,
    resolved: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get alerts with optional filtering"""
    query = db.query(Alert)
    
    if severity:
        try:
            severity_enum = SeverityLevel[severity.upper()]
            query = query.filter(Alert.severity == severity_enum)
        except KeyError:
            pass
    
    if status:
        try:
            status_enum = AlertStatus[status.upper()]
            query = query.filter(Alert.status == status_enum)
        except KeyError:
            pass
    
    if resolved is not None:
        query = query.filter(Alert.is_resolved == resolved)
    
    alerts = query.order_by(Alert.timestamp.desc()).offset(skip).limit(limit).all()
    
    return [
        AlertResponse(
            id=alert.id,
            title=alert.title,
            description=alert.description,
            severity=alert.severity.value if alert.severity else 'low',
            source=alert.source,
            source_ip=alert.source_ip,
            timestamp=alert.timestamp.isoformat(),
            status=alert.status.value if alert.status else 'open',
            is_resolved=alert.is_resolved,
            assigned_to=alert.assigned_to,
            category=alert.category,
            anomaly_score=alert.anomaly_score
        )
        for alert in alerts
    ]

@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: int, db: Session = Depends(get_db)):
    """Get a specific alert"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return AlertResponse(
        id=alert.id,
        title=alert.title,
        description=alert.description,
        severity=alert.severity.value if alert.severity else 'low',
        source=alert.source,
        source_ip=alert.source_ip,
        timestamp=alert.timestamp.isoformat(),
        status=alert.status.value if alert.status else 'open',
        is_resolved=alert.is_resolved,
        assigned_to=alert.assigned_to,
        category=alert.category,
        anomaly_score=alert.anomaly_score
    )

@router.patch("/{alert_id}")
async def update_alert(
    alert_id: int,
    update: AlertUpdate,
    db: Session = Depends(get_db)
):
    """Update an alert"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    if update.status:
        try:
            alert.status = AlertStatus[update.status.upper()]
        except KeyError:
            raise HTTPException(status_code=400, detail="Invalid status")
    
    if update.assigned_to is not None:
        alert.assigned_to = update.assigned_to
    
    if update.is_resolved is not None:
        alert.is_resolved = update.is_resolved
        if update.is_resolved:
            alert.status = AlertStatus.RESOLVED
    
    db.commit()
    db.refresh(alert)
    
    return AlertResponse(
        id=alert.id,
        title=alert.title,
        description=alert.description,
        severity=alert.severity.value if alert.severity else 'low',
        source=alert.source,
        source_ip=alert.source_ip,
        timestamp=alert.timestamp.isoformat(),
        status=alert.status.value if alert.status else 'open',
        is_resolved=alert.is_resolved,
        assigned_to=alert.assigned_to,
        category=alert.category,
        anomaly_score=alert.anomaly_score
    )

@router.patch("/{alert_id}/resolve")
async def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    """Resolve an alert"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.is_resolved = True
    alert.status = AlertStatus.RESOLVED
    db.commit()
    
    return {"status": "resolved", "alert_id": alert_id}

@router.get("/stats/summary")
async def get_alert_stats(db: Session = Depends(get_db)):
    """Get alert statistics"""
    total = db.query(Alert).count()
    unresolved = db.query(Alert).filter(Alert.is_resolved == False).count()
    critical = db.query(Alert).filter(Alert.severity == SeverityLevel.CRITICAL).count()
    high = db.query(Alert).filter(Alert.severity == SeverityLevel.HIGH).count()
    medium = db.query(Alert).filter(Alert.severity == SeverityLevel.MEDIUM).count()
    low = db.query(Alert).filter(Alert.severity == SeverityLevel.LOW).count()
    
    return {
        "total_alerts": total,
        "unresolved": unresolved,
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low
    }

