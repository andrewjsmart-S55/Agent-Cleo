"""
Database models and setup for Agent-Cleo
SQLAlchemy ORM for agent orchestration
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum

from src.config import settings

# Create database engine
engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ============================================================================
# ENUMS
# ============================================================================

class AgentTierEnum(str, enum.Enum):
    MASTER = "master"
    PERSONAL = "personal"
    TEAM = "team"
    WORKER = "worker"
    EXPERT = "expert"


class AgentStatusEnum(str, enum.Enum):
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    ERROR = "error"
    OFFLINE = "offline"


class JobStatusEnum(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


# ============================================================================
# DATABASE MODELS
# ============================================================================

class AgentDB(Base):
    """Agent database model"""
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    folder_name = Column(String(200), unique=True, nullable=False)
    path = Column(String(500), nullable=False)
    tier = Column(Enum(AgentTierEnum), nullable=False)
    description = Column(Text)
    capabilities = Column(JSON)  # List of capabilities
    status = Column(Enum(AgentStatusEnum), default=AgentStatusEnum.IDLE)
    context_summary = Column(Text)
    reports_to = Column(Integer, ForeignKey('agents.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active = Column(DateTime)

    # Relationships
    jobs = relationship("JobDB", back_populates="agent", cascade="all, delete-orphan")
    activities = relationship("ActivityDB", back_populates="agent", cascade="all, delete-orphan")
    subordinates = relationship("AgentDB", backref="manager", remote_side=[id])


class JobDB(Base):
    """Job database model"""
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    frequency = Column(String(50), default="manual")
    cron_expression = Column(String(100))
    sop = Column(Text)
    status = Column(Enum(JobStatusEnum), default=JobStatusEnum.ACTIVE)
    last_run = Column(DateTime)
    next_run = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    agent = relationship("AgentDB", back_populates="jobs")
    activities = relationship("ActivityDB", back_populates="job", cascade="all, delete-orphan")


class ActivityDB(Base):
    """Activity database model"""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=True)
    title = Column(String(200), nullable=False)
    summary = Column(Text)
    output_files = Column(JSON)  # List of file info
    status = Column(String(20), default="success")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    agent = relationship("AgentDB", back_populates="activities")
    job = relationship("JobDB", back_populates="activities")


class ChatSessionDB(Base):
    """Chat session database model"""
    __tablename__ = "chat_sessions"

    id = Column(String(100), primary_key=True)
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False)
    messages = Column(JSON)  # List of messages
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DocumentDB(Base):
    """Document database model (for RAG)"""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(500), nullable=False)
    original_filename = Column(String(500), nullable=False)
    file_path = Column(String(1000), nullable=False)
    file_size = Column(Integer)
    mime_type = Column(String(100))
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=True)
    uploaded_by = Column(String(200))
    chunk_count = Column(Integer, default=0)
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============================================================================
# DATABASE UTILITIES
# ============================================================================

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine, checkfirst=True)
    except Exception as e:
        # Handle race condition when multiple workers try to create tables simultaneously
        if "already exists" in str(e).lower():
            # Tables already created by another worker, this is fine
            pass
        else:
            # Re-raise if it's a different error
            raise


def drop_db():
    """Drop all database tables (use with caution!)"""
    Base.metadata.drop_all(bind=engine)
