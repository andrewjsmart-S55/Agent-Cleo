#!/usr/bin/env python3
"""Check if Docker build copied the source files correctly"""
import boto3
from datetime import datetime

session = boto3.Session(profile_name='Studio55', region_name='eu-north-1')
logs_client = session.client('logs')
codebuild_client = session.client('codebuild')

# Latest build with bytecode fix
build_id = 'agent-cleo-build:25c9ffee-2073-4508-8541-7fa7ad7ead31'

# Get build details
response = codebuild_client.batch_get_builds(ids=[build_id])
build = response['builds'][0]

print("=" * 70)
print("Docker COPY Step Analysis")
print("=" * 70)
print(f"Build from commit: {build.get('resolvedSourceVersion', 'N/A')[:7]}")
print()

# Get logs
log_group = '/aws/codebuild/agent-cleo'
log_stream = build['logs']['streamName']

try:
    response = logs_client.get_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        limit=2000
    )

    print("Docker build steps:")
    print("=" * 70)

    for event in response['events']:
        message = event['message'].strip()
        # Show numbered build steps and COPY operations
        if (message.startswith('#') and
            ('COPY' in message or 'RUN find' in message or 'production' in message or
             'WORKDIR' in message or 'ENV PYTHON' in message)):
            print(message)

    print("=" * 70)

except Exception as e:
    print(f"Error: {e}")
