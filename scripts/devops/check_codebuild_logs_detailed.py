#!/usr/bin/env python3
"""Check CodeBuild logs in detail to see what was actually built"""
import boto3
from datetime import datetime, timedelta

session = boto3.Session(profile_name='Studio55', region_name='eu-north-1')
logs_client = session.client('logs')
codebuild_client = session.client('codebuild')

build_id = 'agent-cleo-build:e069800f-9fc2-4e75-b8af-ace1b0a7965b'

# Get build details
response = codebuild_client.batch_get_builds(ids=[build_id])
build = response['builds'][0]

print("=" * 70)
print("CodeBuild Details")
print("=" * 70)
print(f"Build ID: {build_id}")
print(f"Source Version: {build.get('sourceVersion', 'N/A')}")
print(f"Resolved Source Version: {build.get('resolvedSourceVersion', 'N/A')}")
print(f"Build Status: {build['buildStatus']}")
print()

# Get logs
log_group = '/aws/codebuild/agent-cleo-build'
log_stream = build['logs']['streamName']

print("=" * 70)
print("Build Logs (looking for source download and COPY commands)")
print("=" * 70)

try:
    response = logs_client.get_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        limit=1000
    )

    for event in response['events']:
        message = event['message'].strip()
        # Show lines related to git clone, source download, or COPY commands
        if any(keyword in message.lower() for keyword in ['cloning', 'checkout', 'resolved source', 'copy', 'git', 'download', 'source']):
            timestamp = datetime.fromtimestamp(event['timestamp'] / 1000)
            print(f"[{timestamp.strftime('%H:%M:%S')}] {message}")

    print("=" * 70)

except Exception as e:
    print(f"Error getting logs: {e}")
