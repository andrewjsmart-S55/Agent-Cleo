"""
Pydantic models for Agent-Cleo
Combines agent orchestration with RAG capabilities
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class AgentTier(str, Enum):
    """Agent hierarchy tiers"""
    MASTER = "master"
    PERSONAL = "personal"
    TEAM = "team"
    WORKER = "worker"
    EXPERT = "expert"


class AgentStatus(str, Enum):
    """Agent operational status"""
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    ERROR = "error"
    OFFLINE = "offline"


class JobFrequency(str, Enum):
    """Job scheduling frequencies"""
    MANUAL = "manual"
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"


class JobStatus(str, Enum):
    """Job execution status"""
    PENDING = "pending"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class SearchType(str, Enum):
    """RAG search types"""
    HYBRID = "hybrid"
    VECTOR = "vector"
    KNOWLEDGE_GRAPH = "knowledge_graph"


# ============================================================================
# AGENT MODELS
# ============================================================================

class AgentBase(BaseModel):
    """Base agent model"""
    name: str = Field(..., description="Agent display name")
    folder_name: str = Field(..., description="Agent folder name")
    tier: AgentTier = Field(..., description="Agent tier in hierarchy")
    description: Optional[str] = Field(None, description="Agent description")
    capabilities: List[str] = Field(default_factory=list, description="Agent capabilities")
    status: AgentStatus = Field(default=AgentStatus.IDLE, description="Current status")


class Agent(AgentBase):
    """Full agent model with metadata"""
    id: int
    path: str
    context_summary: Optional[str] = None
    reports_to: Optional[int] = Field(None, description="Parent agent ID")
    manages: List[int] = Field(default_factory=list, description="Subordinate agent IDs")
    created_at: datetime
    updated_at: datetime
    last_active: Optional[datetime] = None

    class Config:
        from_attributes = True


class AgentCreate(AgentBase):
    """Agent creation model"""
    path: str
    reports_to: Optional[int] = None


class AgentUpdate(BaseModel):
    """Agent update model"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[AgentStatus] = None
    capabilities: Optional[List[str]] = None


# ============================================================================
# JOB MODELS
# ============================================================================

class JobBase(BaseModel):
    """Base job model"""
    name: str = Field(..., description="Job name")
    description: Optional[str] = Field(None, description="Job description")
    frequency: JobFrequency = Field(default=JobFrequency.MANUAL, description="Execution frequency")
    sop: Optional[str] = Field(None, description="Standard Operating Procedure")


class Job(JobBase):
    """Full job model"""
    id: int
    agent_id: int
    agent_name: Optional[str] = None
    status: JobStatus = JobStatus.ACTIVE
    cron_expression: Optional[str] = None
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class JobCreate(JobBase):
    """Job creation model"""
    agent_id: int
    cron_expression: Optional[str] = None


class JobUpdate(BaseModel):
    """Job update model"""
    name: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[JobFrequency] = None
    status: Optional[JobStatus] = None
    sop: Optional[str] = None


# ============================================================================
# ACTIVITY MODELS
# ============================================================================

class ActivityBase(BaseModel):
    """Base activity model"""
    title: str = Field(..., description="Activity title")
    summary: Optional[str] = Field(None, description="Activity summary")
    status: str = Field(default="success", description="Activity status")


class Activity(ActivityBase):
    """Full activity model"""
    id: int
    agent_id: int
    agent_name: Optional[str] = None
    job_id: Optional[int] = None
    job_name: Optional[str] = None
    output_files: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime

    class Config:
        from_attributes = True


class ActivityCreate(ActivityBase):
    """Activity creation model"""
    agent_id: int
    job_id: Optional[int] = None
    output_files: Optional[List[Dict[str, Any]]] = None


# ============================================================================
# RAG MODELS (from Studio55IQ)
# ============================================================================

class DocumentUploadResponse(BaseModel):
    """Response for document upload"""
    success: bool
    message: str
    processed_files: List[Dict[str, Any]] = Field(default_factory=list)


class QueryRequest(BaseModel):
    """RAG query request"""
    query: str = Field(..., description="User query")
    agent_id: Optional[int] = Field(None, description="Specific agent to query")
    max_results: int = Field(default=5, description="Maximum results")
    include_sources: bool = Field(default=True, description="Include source citations")
    search_type: SearchType = Field(default=SearchType.HYBRID, description="Search method")


class QueryResponse(BaseModel):
    """RAG query response"""
    answer: str
    sources: List[Dict[str, Any]] = Field(default_factory=list)
    agent_id: Optional[int] = None
    agent_name: Optional[str] = None
    processing_time: float
    search_type: SearchType


# ============================================================================
# CHAT MODELS
# ============================================================================

class ChatMessage(BaseModel):
    """Chat message model"""
    role: str = Field(..., description="Message role (user/agent/system)")
    content: str = Field(..., description="Message content")
    agent_id: Optional[int] = Field(None, description="Agent ID if agent message")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None


class ChatSession(BaseModel):
    """Chat session model"""
    session_id: str
    agent_id: int
    agent_name: str
    messages: List[ChatMessage] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class ChatRequest(BaseModel):
    """Chat request model"""
    agent_id: int = Field(..., description="Agent to chat with")
    message: str = Field(..., description="User message")
    session_id: Optional[str] = Field(None, description="Chat session ID")
    use_rag: bool = Field(default=True, description="Use RAG for knowledge")


class ChatResponse(BaseModel):
    """Chat response model"""
    session_id: str
    agent_id: int
    agent_name: str
    message: str
    sources: Optional[List[Dict[str, Any]]] = None
    timestamp: datetime


# ============================================================================
# VISUALIZATION MODELS
# ============================================================================

class AgentNode(BaseModel):
    """Agent node for visualization"""
    id: int
    name: str
    tier: AgentTier
    status: AgentStatus
    x: Optional[float] = None
    y: Optional[float] = None


class AgentEdge(BaseModel):
    """Agent relationship edge"""
    source: int
    target: int
    type: str = "manages"


class AgentGraph(BaseModel):
    """Agent network graph"""
    nodes: List[AgentNode]
    edges: List[AgentEdge]


class AgentHierarchy(BaseModel):
    """Agent org chart hierarchy"""
    id: int
    name: str
    tier: AgentTier
    status: AgentStatus
    children: List['AgentHierarchy'] = Field(default_factory=list)


# ============================================================================
# TODOIST MODELS
# ============================================================================

class TodoistTaskCreate(BaseModel):
    """Todoist task creation"""
    content: str
    description: Optional[str] = None
    project: Optional[str] = None
    priority: int = Field(default=1, ge=1, le=4)
    due: Optional[str] = None
    labels: Optional[List[str]] = None
    agent_id: int


class TodoistTaskResponse(BaseModel):
    """Todoist task response"""
    success: bool
    task_id: Optional[str] = None
    url: Optional[str] = None
    message: str


# ============================================================================
# HEALTH CHECK
# ============================================================================

class HealthCheck(BaseModel):
    """System health check"""
    status: str
    version: str
    database: bool
    rag_engine: bool
    overlord: bool
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Allow forward references
AgentHierarchy.model_rebuild()
