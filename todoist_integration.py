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
import re


def convert_relative_to_absolute_date(date_string: str) -> str:
    """
    Convert relative date strings to absolute dates (YYYY-MM-DD format)

    Args:
        date_string: Relative date like "today", "tomorrow", "next Monday", etc.

    Returns:
        Absolute date string in YYYY-MM-DD format, or original string if already absolute
    """
    if not date_string:
        return None

    date_string_lower = date_string.lower().strip()
    now = datetime.now()

    # Already an absolute date (contains year or is in YYYY-MM-DD format)
    if re.match(r'\d{4}-\d{2}-\d{2}', date_string) or '202' in date_string:
        return date_string

    # Handle "today"
    if date_string_lower == "today":
        return now.strftime("%Y-%m-%d")

    # Handle "tomorrow"
    if date_string_lower == "tomorrow":
        return (now + timedelta(days=1)).strftime("%Y-%m-%d")

    # Handle "yesterday" (edge case)
    if date_string_lower == "yesterday":
        return (now - timedelta(days=1)).strftime("%Y-%m-%d")

    # Handle "in X days"
    match = re.match(r'in (\d+) days?', date_string_lower)
    if match:
        days = int(match.group(1))
        return (now + timedelta(days=days)).strftime("%Y-%m-%d")

    # Handle weekday names (Monday, Tuesday, etc.)
    weekdays = {
        'monday': 0, 'mon': 0,
        'tuesday': 1, 'tue': 1, 'tues': 1,
        'wednesday': 2, 'wed': 2,
        'thursday': 3, 'thu': 3, 'thur': 3, 'thurs': 3,
        'friday': 4, 'fri': 4,
        'saturday': 5, 'sat': 5,
        'sunday': 6, 'sun': 6
    }

    # Handle "next Monday", "this Friday", etc.
    for day_name, day_num in weekdays.items():
        if day_name in date_string_lower:
            current_weekday = now.weekday()
            days_ahead = day_num - current_weekday

            # If "next" is explicitly mentioned, always go to next week
            if "next" in date_string_lower and days_ahead >= 0:
                days_ahead += 7
            # If "this" or just the day name, go to next occurrence
            elif days_ahead <= 0:
                days_ahead += 7

            target_date = now + timedelta(days=days_ahead)
            return target_date.strftime("%Y-%m-%d")

    # Handle "next week" - return next Monday
    if "next week" in date_string_lower:
        days_ahead = 7 - now.weekday()
        return (now + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

    # Handle "this week" - return this Friday
    if "this week" in date_string_lower:
        days_ahead = 4 - now.weekday()  # Friday
        if days_ahead < 0:
            days_ahead += 7
        return (now + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

    # If we can't parse it, return the original string
    # Todoist might be able to handle it
    return date_string


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
                # API v3 returns a paginator that yields lists
                projects_paginator = self.api.get_projects()
                self._projects_cache = list(projects_paginator)[0]  # Get the actual list from paginator
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

            # Ensure Agent-Cleo label is included (unless it's a goal with Agent-Cleo-Goals)
            task_labels = labels or []
            if "Agent-Cleo" not in task_labels and "Agent-Cleo-Goals" not in task_labels:
                task_labels = task_labels + ["Agent-Cleo"]

            # Convert relative dates to absolute dates
            absolute_due_date = convert_relative_to_absolute_date(due_string) if due_string else None

            # Create the task
            task = self.api.add_task(
                content=content,
                description=full_description,
                project_id=project_id,
                priority=priority,
                due_string=absolute_due_date,
                labels=task_labels
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

    def get_tasks(self, label: str = None, project_id: str = None) -> List[Dict]:
        """
        Get tasks, optionally filtered by label or project

        Args:
            label: Filter by label name (e.g., "Agent-Cleo")
            project_id: Filter by project ID

        Returns:
            List of task dictionaries
        """
        try:
            # Get all active tasks - API v3 returns a ResultsPaginator
            tasks_paginator = self.api.get_tasks(label=label, project_id=project_id)

            # Convert paginator to list of tasks
            # The paginator yields pages (lists of tasks), so we need to flatten
            all_tasks = []
            for page in tasks_paginator:
                all_tasks.extend(page)

            return [
                {
                    'id': task.id,
                    'content': task.content,
                    'description': task.description,
                    'project_id': task.project_id,
                    'labels': task.labels,
                    'priority': task.priority,
                    'due': task.due.date if task.due else None,
                    'url': task.url,
                    'created_at': task.created_at,
                    'is_completed': task.is_completed
                }
                for task in all_tasks
            ]
        except Exception as e:
            print(f"Error fetching tasks: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_agent_cleo_tasks(self, include_completed: bool = False) -> List[Dict]:
        """
        Get all tasks labeled with "Agent-Cleo"

        Args:
            include_completed: Whether to include completed tasks

        Returns:
            List of task dictionaries
        """
        tasks = self.get_tasks(label="Agent-Cleo")

        if not include_completed:
            tasks = [t for t in tasks if not t['is_completed']]

        return tasks

    def update_task(self, task_id: str, **kwargs) -> Dict:
        """
        Update a task

        Args:
            task_id: Todoist task ID
            **kwargs: Fields to update (content, description, due_string, priority, labels)

        Returns:
            Result dictionary
        """
        try:
            # Convert relative dates to absolute if due_string is provided
            if 'due_string' in kwargs and kwargs['due_string']:
                kwargs['due_string'] = convert_relative_to_absolute_date(kwargs['due_string'])

            task = self.api.update_task(task_id=task_id, **kwargs)

            return {
                'success': True,
                'task_id': task.id,
                'content': task.content,
                'message': 'Task updated successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Failed to update task: {str(e)}'
            }

    def close_task(self, task_id: str) -> Dict:
        """
        Mark a task as complete

        Args:
            task_id: Todoist task ID

        Returns:
            Result dictionary
        """
        try:
            self.api.close_task(task_id=task_id)

            return {
                'success': True,
                'task_id': task_id,
                'message': 'Task completed successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Failed to complete task: {str(e)}'
            }


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


def get_agent_tasks(include_completed: bool = False) -> List[Dict]:
    """
    Get all tasks labeled with "Agent-Cleo"

    Args:
        include_completed: Whether to include completed tasks

    Returns:
        List of task dictionaries
    """
    try:
        integration = TodoistIntegration()
        return integration.get_agent_cleo_tasks(include_completed=include_completed)
    except Exception as e:
        print(f"Error fetching Agent-Cleo tasks: {e}")
        return []


def get_tasks_by_label(label: str) -> List[Dict]:
    """
    Get tasks by label

    Args:
        label: Label name to filter by

    Returns:
        List of task dictionaries
    """
    try:
        integration = TodoistIntegration()
        return integration.get_tasks(label=label)
    except Exception as e:
        print(f"Error fetching tasks by label: {e}")
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
            print(f"[SUCCESS] Task created successfully!")
            print(f"  - Content: {result['content']}")
            print(f"  - Project: {result['project']}")
            print(f"  - URL: {result['url']}")
        else:
            print(f"[ERROR] Failed to create task: {result['error']}")

    except Exception as e:
        print(f"\n[ERROR] Integration test failed: {e}")
        print("\nMake sure to set TODOIST_API_TOKEN environment variable")
