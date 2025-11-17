#!/usr/bin/env python3
"""Check recent CloudWatch logs for Agent-Cleo startup"""
import boto3
from datetime import datetime, timedelta

session = boto3.Session(profile_name='Studio55', region_name='eu-north-1')
logs_client = session.client('logs')

log_group = '/ecs/agent-cleo-prod'

print("=" * 70)
print("Agent-Cleo Recent Startup Logs")
print("=" * 70)
print()

# Get logs from last 15 minutes
start_time = int((datetime.now() - timedelta(minutes=15)).timestamp() * 1000)
end_time = int(datetime.now().timestamp() * 1000)

try:
    response = logs_client.filter_log_events(
        logGroupName=log_group,
        startTime=start_time,
        endTime=end_time,
        limit=1000
    )

    events = response.get('events', [])

    if not events:
        print("No logs found in the last 15 minutes")
        print()
        print("Checking last 100 events from any time...")
        response = logs_client.filter_log_events(
            logGroupName=log_group,
            limit=100
        )
        events = response.get('events', [])

    print(f"Found {len(events)} log events")
    print()

    # Look for startup messages
    startup_found = False
    agent_discovery_found = False

    for event in events:
        message = event['message'].strip()
        timestamp = datetime.fromtimestamp(event['timestamp'] / 1000)

        # Print startup banner
        if 'Agent-Cleo v2.0' in message:
            startup_found = True
            print(f"[{timestamp}] {message}")

        # Print database initialization
        elif 'Initializing database' in message or 'Database initialized' in message:
            print(f"[{timestamp}] {message}")

        # Print agent discovery messages
        elif 'Discovering agents' in message or 'Discovered' in message or 'agents_cache' in message:
            agent_discovery_found = True
            # Handle potential unicode issues
            try:
                print(f"[{timestamp}] {message}")
            except UnicodeEncodeError:
                print(f"[{timestamp}] {message.encode('utf-8', errors='replace').decode('utf-8')}")

        # Print errors
        elif 'ERROR' in message or 'Error' in message or 'Failed' in message:
            try:
                print(f"[{timestamp}] ERROR: {message}")
            except UnicodeEncodeError:
                print(f"[{timestamp}] ERROR: {message.encode('utf-8', errors='replace').decode('utf-8')}")

        # Print warnings
        elif 'WARNING' in message or 'Warning' in message:
            try:
                print(f"[{timestamp}] WARNING: {message}")
            except UnicodeEncodeError:
                print(f"[{timestamp}] WARNING: {message.encode('utf-8', errors='replace').decode('utf-8')}")

    print()
    print("=" * 70)
    print("Summary:")
    print(f"  Startup banner found: {'✓' if startup_found else '✗'}")
    print(f"  Agent discovery found: {'✓' if agent_discovery_found else '✗'}")
    print("=" * 70)

except Exception as e:
    print(f"Error reading logs: {e}")
