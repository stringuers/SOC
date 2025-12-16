from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

from database import Base

class SeverityLevel(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertStatus(enum.Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"

class IncidentStatus(enum.Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    CLOSED = "closed"

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    severity = Column(Enum(SeverityLevel), nullable=False)
    source = Column(String(100))
    source_ip = Column(String(45))
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    is_resolved = Column(Boolean, default=False)
    status = Column(Enum(AlertStatus), default=AlertStatus.OPEN)
    assigned_to = Column(String(100), nullable=True)
    category = Column(String(100), nullable=True)
    threat_intel = Column(JSON, nullable=True)  # Store threat intelligence data
    anomaly_score = Column(String(50), nullable=True)

class Incident(Base):
    __tablename__ = "incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    severity = Column(Enum(SeverityLevel), nullable=False)
    status = Column(Enum(IncidentStatus), default=IncidentStatus.OPEN)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    assigned_to = Column(String(100), nullable=True)
    playbook_executed = Column(Boolean, default=False)
    playbook_results = Column(JSON, nullable=True)

class LogEntry(Base):
    __tablename__ = "log_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    source_ip = Column(String(45), index=True)
    destination_ip = Column(String(45), index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    log_type = Column(String(50))
    raw_log = Column(Text)
    message = Column(Text)
    parsed_data = Column(JSON)  # JSON field for parsed log data
    severity = Column(Enum(SeverityLevel), default=SeverityLevel.LOW)
    is_anomaly = Column(Boolean, default=False)
    anomaly_score = Column(String(50), nullable=True)

