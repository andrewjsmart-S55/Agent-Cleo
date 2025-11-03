"""
Todoist Integration for Agent-Cleo
Allows agents to create and manage tasks in Todoist for Andrew
"""
import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task, Project
import json


class TodoistIntegration:
    """
    Todoist Integration for Agent-Cleo system
    Enables agents to create tasks, organize by projects, and manage priorities
    """

    def __init__(self, api_token: str = None):
        """
        Initialize Todoist integration

        Args:
            api_token: Todoist API token (if not provided, reads from environment variable TODOIST_API_TOKEN)
        """
        self.api_token = api_token or os.getenv('TODOIST_API_TOKEN')

        if not self.api_token:
            raise ValueError(
                "Todoist API token not provided. Set TODOIST_API_TOKEN environment variable "
                "or pass api_token parameter."
            )

        self.api = TodoistAPI(self.api_token)
        self._projects_cache = None
        self._cache_timestamp = None

    def get_projects(self, force_refresh: bool = False) -> List[Project]:
        """
        Get all Todoist projects (cached for 5 minutes)

        Args:
            force_refresh: Force refresh the cache

        Returns:
            List of Todoist Project objects
        """
        now = datetime.now()

        # Refresh cache if older than 5 minutes or forced
        if (force_refresh or
            self._projects_cache is None or
            self._cache_timestamp is None or
            (now - self._cache_timestamp).seconds > 300):

            try:
                self._projects_cache = self.api.get_projects()
                self._cache_timestamp = now
            except Exception as e:
                print(f"Error fetching projects: {e}")
                return []

        return self._projects_cache

    def get_project_by_name(self, project_name: str) -> Optional[Project]:
        """
        Find a project by name (case-insensitive)

        Args:
            project_name: Name of the project to find

        Returns:
            Project object if found, None otherwise
        """
        projects = self.get_projects()

        for project in projects:
            if project.name.lower() == project_name.lower():
                return project

        return None

    def create_task(
        self,
        content: str,
        description: str = "",
        project_name: str = None,
        priority: int = 1,
        due_string: str = None,
        labels: List[str] = None,
        agent_name: str = None
    ) -> Dict:
        """
        Create a task in Todoist

        Args:
            content: Task title/content (required)
            description: Task description
            project_name: Name of the project (e.g., "DecideWright", "Studio55")
            priority: Priority level (1=normal, 2=medium, 3=high, 4=urgent)
            due_string: Due date in natural language (e.g., "today", "tomorrow", "next Monday")
            labels: List of label names to add to the task
            agent_name: Name of the agent creating the task (added to description)

        Returns:
            Dictionary with task details and status
        """
        try:
            # Find project ID if project_name provided
            project_id = None
            if project_name:
                project = self.get_project_by_name(project_name)
                if project:
                    project_id = project.id
                else:
                    print(f"Warning: Project '{project_name}' not found. Creating task in Inbox.")

            # Add agent attribution to description
            full_description = description
            if agent_name:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                full_description = f"**Created by {agent_name}** at {timestamp}\n\n{description}"

            # Create the task
            task = self.api.add_task(
                content=content,
                description=full_description,
                project_id=project_id,
                priority=priority,
                due_string=due_string,
                labels=labels or []
            )

            return {
                'success': True,
                'task_id': task.id,
                'content': task.content,
                'project': project_name if project_id else "Inbox",
                'url': task.url,
                'message': f"Task created successfully in {project_name or 'Inbox'}"
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to create task: {str(e)}"
            }

    def create_tasks_batch(
        self,
        tasks: List[Dict],
        agent_name: str = None
    ) -> Dict:
        """
        Create multiple tasks in batch

        Args:
            tasks: List of task dictionaries with fields:
                   - content (required)
                   - description (optional)
                   - project_name (optional)
                   - priority (optional)
                   - due_string (optional)
                   - labels (optional)
            agent_name: Name of the agent creating tasks

        Returns:
            Dictionary with results summary
        """
        results = {
            'success': True,
            'created': [],
            'failed': [],
            'total': len(tasks)
        }

        for task_data in tasks:
            result = self.create_task(
                content=task_data.get('content'),
                description=task_data.get('description', ''),
                project_name=task_data.get('project_name'),
                priority=task_data.get('priority', 1),
                due_string=task_data.get('due_string'),
                labels=task_data.get('labels'),
                agent_name=agent_name
            )

            if result['success']:
                results['created'].append(result)
            else:
                results['failed'].append(result)

        if results['failed']:
            results['success'] = False

        results['message'] = f"Created {len(results['created'])} of {results['total']} tasks"

        return results

    def create_project_tasks(
        self,
        project_name: str,
        tasks: List[str],
        agent_name: str = None,
        priority: int = 1
    ) -> Dict:
        """
        Convenience method to create multiple tasks for a specific project

        Args:
            project_name: Name of the Todoist project
            tasks: List of task content strings
            agent_name: Name of the agent creating tasks
            priority: Priority level for all tasks

        Returns:
            Dictionary with results summary
        """
        task_list = [
            {
                'content': task,
                'project_name': project_name,
                'priority': priority
            }
            for task in tasks
        ]

        return self.create_tasks_batch(task_list, agent_name=agent_name)

    def list_projects(self) -> List[Dict]:
        """
        Get a list of all projects with basic info

        Returns:
            List of dictionaries with project information
        """
        projects = self.get_projects(force_refresh=True)

        return [
            {
                'id': p.id,
                'name': p.name,
                'color': p.color,
                'is_favorite': p.is_favorite
            }
            for p in projects
        ]


# Convenience functions for agents to use
def create_task_for_andrew(
    content: str,
    description: str = "",
    project: str = None,
    priority: int = 1,
    due: str = None,
    labels: List[str] = None,
    agent: str = "Agent-Cleo"
) -> Dict:
    """
    Quick function for agents to create a task for Andrew

    Args:
        content: Task title
        description: Task description
        project: Project name (DecideWright, Studio55, SparkwireMedia, ThinTanks, Ascendore, Personal)
        priority: 1=normal, 2=medium, 3=high, 4=urgent
        due: Due date ("today", "tomorrow", "next week", "Nov 15", etc.)
        labels: List of labels
        agent: Name of the agent creating the task

    Returns:
        Result dictionary
    """
    integration = TodoistIntegration()

    return integration.create_task(
        content=content,
        description=description,
        project_name=project,
        priority=priority,
        due_string=due,
        labels=labels,
        agent_name=agent
    )


def create_weekly_plan_tasks(
    tasks: List[Dict],
    agent: str = "Coach-Cleo"
) -> Dict:
    """
    Create tasks from Coach-Cleo's weekly planning session

    Args:
        tasks: List of task dictionaries with content, project, priority, due
        agent: Agent name

    Returns:
        Result dictionary
    """
    integration = TodoistIntegration()

    return integration.create_tasks_batch(tasks, agent_name=agent)


def get_available_projects() -> List[str]:
    """
    Get list of available Todoist projects

    Returns:
        List of project names
    """
    try:
        integration = TodoistIntegration()
        projects = integration.list_projects()
        return [p['name'] for p in projects]
    except Exception as e:
        print(f"Error fetching projects: {e}")
        return []


# Example usage templates for agents
EXAMPLE_USAGE = """
# Todoist Integration Examples for Agents

## Single Task Creation

```python
from todoist_integration import create_task_for_andrew

# Simple task
result = create_task_for_andrew(
    content="Complete DecideWright website homepage",
    project="DecideWright",
    priority=3,
    due="Friday"
)

# Task with description and labels
result = create_task_for_andrew(
    content="Review QRA Playbook pricing strategy",
    description="Need to finalize pricing tiers and compare with competitors",
    project="DecideWright",
    priority=2,
    due="tomorrow",
    labels=["sales", "pricing"],
    agent="Agent-CMO"
)
```

## Batch Task Creation (e.g., from Coach-Cleo weekly plan)

```python
from todoist_integration import create_weekly_plan_tasks

tasks = [
    {
        "content": "Create DecideWright one-page offer",
        "project_name": "DecideWright",
        "priority": 4,
        "due_string": "Wednesday"
    },
    {
        "content": "Outreach to 20 target organizations",
        "project_name": "DecideWright",
        "priority": 3,
        "due_string": "Friday",
        "labels": ["sales", "outreach"]
    },
    {
        "content": "Book 5 customer conversations",
        "project_name": "DecideWright",
        "priority": 4,
        "due_string": "Friday"
    }
]

result = create_weekly_plan_tasks(tasks, agent="Coach-Cleo")
print(f"{result['message']}")
```

## Project-Based Tasks

```python
from todoist_integration import TodoistIntegration

integration = TodoistIntegration()

# Create multiple tasks for Studio55
studio55_tasks = [
    "Create AI services landing page",
    "Draft 10 AI consulting case studies",
    "Identify 10 target organizations",
    "Schedule discovery calls"
]

result = integration.create_project_tasks(
    project_name="Studio55",
    tasks=studio55_tasks,
    agent_name="Agent-CPO",
    priority=3
)
```

## Get Available Projects

```python
from todoist_integration import get_available_projects

projects = get_available_projects()
print(f"Available projects: {', '.join(projects)}")
```
"""


if __name__ == "__main__":
    # Test script
    print("Todoist Integration Test")
    print("=" * 50)

    try:
        integration = TodoistIntegration()

        # List projects
        print("\nAvailable Projects:")
        projects = integration.list_projects()
        for project in projects:
            print(f"  - {project['name']}")

        # Test creating a task
        print("\nCreating test task...")
        result = create_task_for_andrew(
            content="Test task from Agent-Cleo integration",
            description="This is a test task to verify Todoist integration is working",
            project="Ascendore",
            priority=1,
            agent="Agent-Cleo (Test)"
        )

        if result['success']:
            print(f"✓ Task created successfully!")
            print(f"  - Content: {result['content']}")
            print(f"  - Project: {result['project']}")
            print(f"  - URL: {result['url']}")
        else:
            print(f"✗ Failed to create task: {result['error']}")

    except Exception as e:
        print(f"\n✗ Integration test failed: {e}")
        print("\nMake sure to set TODOIST_API_TOKEN environment variable")
