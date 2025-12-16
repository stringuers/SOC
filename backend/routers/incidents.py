from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
from models import Incident, SeverityLevel, IncidentStatus

router = APIRouter(prefix="/api/incidents", tags=["incidents"])

class IncidentResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    severity: str
    status: str
    created_at: str
    updated_at: Optional[str]
    assigned_to: Optional[str]
    playbook_executed: bool

    class Config:
        from_attributes = True

class IncidentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    severity: str
    assigned_to: Optional[str] = None

@router.get("/", response_model=List[IncidentResponse])
async def get_incidents(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get incidents"""
    query = db.query(Incident)
    
    if status:
        try:
            status_enum = IncidentStatus[status.upper()]
            query = query.filter(Incident.status == status_enum)
        except KeyError:
            pass
    
    incidents = query.order_by(Incident.created_at.desc()).offset(skip).limit(limit).all()
    
    return [
        IncidentResponse(
            id=incident.id,
            title=incident.title,
            description=incident.description,
            severity=incident.severity.value if incident.severity else 'low',
            status=incident.status.value if incident.status else 'open',
            created_at=incident.created_at.isoformat(),
            updated_at=incident.updated_at.isoformat() if incident.updated_at else None,
            assigned_to=incident.assigned_to,
            playbook_executed=incident.playbook_executed
        )
        for incident in incidents
    ]

@router.post("/", response_model=IncidentResponse)
async def create_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    """Create a new incident"""
    try:
        severity_enum = SeverityLevel[incident.severity.upper()]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid severity level")
    
    db_incident = Incident(
        title=incident.title,
        description=incident.description,
        severity=severity_enum,
        assigned_to=incident.assigned_to
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    
    return IncidentResponse(
        id=db_incident.id,
        title=db_incident.title,
        description=db_incident.description,
        severity=db_incident.severity.value if db_incident.severity else 'low',
        status=db_incident.status.value if db_incident.status else 'open',
        created_at=db_incident.created_at.isoformat(),
        updated_at=db_incident.updated_at.isoformat() if db_incident.updated_at else None,
        assigned_to=db_incident.assigned_to,
        playbook_executed=db_incident.playbook_executed
    )

