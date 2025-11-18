#!/usr/bin/env python3
"""Check CloudWatch logs for ALB health checks (non-localhost)"""
import boto3
from datetime import datetime, timedelta

session = boto3.Session(profile_name='Studio55', region_name='eu-north-1')
logs_client = session.client('logs')

log_group = '/ecs/agent-cleo-prod'
start_time = int((datetime.now() - timedelta(minutes=5)).timestamp() * 1000)

try:
    response = logs_client.filter_log_events(
        logGroupName=log_group,
        startTime=start_time,
        limit=50
    )

    print("Recent logs (last 5 minutes):")
    print("=" * 70)

    alb_health_checks = []
    localhost_health_checks = []

    for event in response['events']:
        message = event['message']
        if 'GET /health' in message:
            if '127.0.0.1' in message:
                localhost_health_checks.append(message)
            else:
                alb_health_checks.append(message)
                timestamp = datetime.fromtimestamp(event['timestamp'] / 1000)
                print(f"[{timestamp}] {message}")

    print("=" * 70)
    print(f"Localhost health checks: {len(localhost_health_checks)}")
    print(f"ALB health checks (non-localhost): {len(alb_health_checks)}")

    if len(alb_health_checks) == 0:
        print("\n[!] NO ALB HEALTH CHECKS FOUND!")
        print("[!] ALB cannot reach the tasks - likely a networking issue")

except Exception as e:
    print(f"Error: {e}")
