#!/usr/bin/env python3
"""Check all running tasks and their details"""
import boto3
from datetime import datetime

session = boto3.Session(profile_name='Studio55', region_name='eu-north-1')
ecs_client = session.client('ecs')

cluster = 'overlord-cluster-prod'
service = 'agent-cleo-service'

print("=" * 70)
print("All Running Tasks Analysis")
print("=" * 70)
print()

# Get all tasks
response = ecs_client.list_tasks(cluster=cluster, serviceName=service)
task_arns = response['taskArns']

print(f"Total tasks: {len(task_arns)}")
print()

if task_arns:
    # Get task details
    response = ecs_client.describe_tasks(cluster=cluster, tasks=task_arns)

    for i, task in enumerate(response['tasks'], 1):
        task_id = task['taskArn'].split('/')[-1]
        container = task['containers'][0]

        print(f"Task {i}:")
        print(f"  ID: {task_id}")
        print(f"  Status: {task['lastStatus']}")
        print(f"  Started: {task['startedAt']}")
        print(f"  Image: {container['image']}")
        print(f"  Image Digest: {container.get('imageDigest', 'N/A')}")
        print()

print("=" * 70)
