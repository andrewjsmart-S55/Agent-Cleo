"""
Todoist API Routes - Task management integration
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db, AgentDB
from ..models import TodoistTaskCreate, TodoistTaskResponse

router = APIRouter(prefix="/todoist")

# Import Todoist integration if available
try:
    from todoist_integration import create_task_for_andrew
    TODOIST_ENABLED = True
except ImportError:
    TODOIST_ENABLED = False
    create_task_for_andrew = None


@router.post("/task", response_model=TodoistTaskResponse)
async def create_todoist_task(
    task: TodoistTaskCreate,
    db: Session = Depends(get_db)
):
    """Create Todoist task from agent"""
    if not TODOIST_ENABLED:
        return TodoistTaskResponse(
            success=False,
            message="Todoist integration not available"
        )

    agent = db.query(AgentDB).filter(AgentDB.id == task.agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    try:
        result = create_task_for_andrew(
            content=task.content,
            description=task.description,
            project=task.project,
            priority=task.priority,
            due=task.due,
            labels=task.labels,
            agent=agent.name
        )

        if result.get("success"):
            return TodoistTaskResponse(
                success=True,
                task_id=result.get("task_id"),
                url=result.get("url"),
                message=result.get("message")
            )
        else:
            return TodoistTaskResponse(
                success=False,
                message=result.get("message", "Failed to create task")
            )

    except Exception as e:
        return TodoistTaskResponse(
            success=False,
            message=f"Error: {str(e)}"
        )
