"""
Database models for AI Agent Job Management System
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Agent(db.Model):
    """Represents an AI Assistant agent"""
    __tablename__ = 'agents'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    folder_name = Column(String(100), nullable=False, unique=True)
    path = Column(String(500), nullable=False)
    context_summary = Column(Text)
    is_master = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    jobs = relationship('Job', back_populates='agent', cascade='all, delete-orphan')
    activities = relationship('Activity', back_populates='agent', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'folder_name': self.folder_name,
            'path': self.path,
            'context_summary': self.context_summary,
            'is_master': self.is_master,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Job(db.Model):
    """Represents a job/task for an AI agent"""
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    frequency = Column(String(50))  # daily, weekly, monthly, once, manual
    cron_expression = Column(String(100))  # For custom schedules
    sop = Column(Text)  # Standard Operating Procedure
    status = Column(String(20), default='active')  # active, paused, completed, failed
    last_run = Column(DateTime)
    next_run = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    agent = relationship('Agent', back_populates='jobs')
    activities = relationship('Activity', back_populates='job', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'agent_name': self.agent.name if self.agent else None,
            'name': self.name,
            'description': self.description,
            'frequency': self.frequency,
            'cron_expression': self.cron_expression,
            'sop': self.sop,
            'status': self.status,
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'next_run': self.next_run.isoformat() if self.next_run else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Activity(db.Model):
    """Represents an activity/output from a job execution"""
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=True)
    title = Column(String(200), nullable=False)
    summary = Column(Text)
    output_files = Column(Text)  # JSON array of file paths
    status = Column(String(20), default='success')  # success, failed, in_progress
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    agent = relationship('Agent', back_populates='activities')
    job = relationship('Job', back_populates='activities')

    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'agent_name': self.agent.name if self.agent else None,
            'job_id': self.job_id,
            'job_name': self.job.name if self.job else None,
            'title': self.title,
            'summary': self.summary,
            'output_files': self.output_files,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
