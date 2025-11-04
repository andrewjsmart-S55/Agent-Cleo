#!/usr/bin/env python3
"""
Quick script to create a Todoist task
"""
from todoist_integration import create_task_for_andrew

# Create task for tomorrow
result = create_task_for_andrew(
    content="Cancel Freshsales x2",
    due="tomorrow",
    priority=2,
    agent="Agent-Cleo"
)

if result['success']:
    print(f"✓ Task created successfully!")
    print(f"  - Content: {result['content']}")
    print(f"  - Project: {result['project']}")
    print(f"  - URL: {result['url']}")
else:
    print(f"✗ Failed to create task: {result.get('error', 'Unknown error')}")
    print(f"  - Message: {result.get('message', '')}")
