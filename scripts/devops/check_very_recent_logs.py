#!/usr/bin/env python3
"""Check CloudWatch logs for Agent-Cleo - only most recent"""
import boto3
from datetime import datetime, timedelta

session = boto3.Session(profile_name='Studio55', region_name='eu-north-1')
logs_client = session.client('logs')

log_group = '/ecs/agent-cleo-prod'
start_time = int((datetime.now() - timedelta(minutes=2)).timestamp() * 1000)

try:
    response = logs_client.filter_log_events(
        logGroupName=log_group,
        startTime=start_time,
        limit=150
    )

    if response['events']:
        print(f"Logs from last 2 minutes:")
        print("=" * 70)
        for event in response['events']:
            timestamp = datetime.fromtimestamp(event['timestamp'] / 1000)
            print(f"[{timestamp}] {event['message']}")
        print("=" * 70)
        print(f"Total events: {len(response['events'])}")
    else:
        print(f"No logs from last 2 minutes. Tasks may still be starting...")

except Exception as e:
    print(f"Error: {e}")
