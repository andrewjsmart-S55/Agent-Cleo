#!/usr/bin/env python3
"""Check CodeBuild logs for errors"""
import boto3
from datetime import datetime, timedelta

session = boto3.Session(profile_name='Studio55', region_name='eu-north-1')
logs_client = session.client('logs')

log_group = '/aws/codebuild/agent-cleo-build'
build_id = 'agent-cleo-build:24f2730a-f5ff-42db-822a-fe14869978cf'

# Get logs from last 5 minutes
start_time = int((datetime.now() - timedelta(minutes=5)).timestamp() * 1000)

try:
    response = logs_client.filter_log_events(
        logGroupName=log_group,
        startTime=start_time,
        limit=100
    )

    print("CodeBuild Logs (last 5 minutes):")
    print("=" * 70)

    for event in response['events']:
        timestamp = datetime.fromtimestamp(event['timestamp'] / 1000)
        message = event['message'].strip()
        print(f"[{timestamp.strftime('%H:%M:%S')}] {message}")

    print("=" * 70)

except Exception as e:
    print(f"Error: {e}")
