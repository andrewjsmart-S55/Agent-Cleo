#!/usr/bin/env python3
"""Check ECS task definition for volume mounts that might override app code"""
import boto3
import json

session = boto3.Session(profile_name='Studio55', region_name='eu-north-1')
ecs_client = session.client('ecs')

task_def_arn = 'agent-cleo-prod:3'

print("=" * 70)
print("ECS Task Definition Analysis")
print("=" * 70)
print()

response = ecs_client.describe_task_definition(taskDefinition=task_def_arn)
task_def = response['taskDefinition']

# Check for volumes
print("Volumes:")
if task_def.get('volumes'):
    for volume in task_def['volumes']:
        print(f"  - {json.dumps(volume, indent=4)}")
else:
    print("  None")

print()

# Check container mount points
print("Container Configuration:")
for container in task_def['containerDefinitions']:
    print(f"\nContainer: {container['name']}")
    print(f"  Image: {container['image']}")
    print(f"  Working Dir: {container.get('workingDirectory', 'N/A')}")

    if container.get('mountPoints'):
        print(f"  Mount Points:")
        for mp in container['mountPoints']:
            print(f"    - {json.dumps(mp, indent=6)}")
    else:
        print(f"  Mount Points: None")

    # Check environment variables
    if container.get('environment'):
        print(f"  Environment Variables:")
        for env in container['environment']:
            if 'PYTHON' in env['name'] or 'APP' in env['name']:
                print(f"    - {env['name']}: {env['value']}")

print()
print("=" * 70)
