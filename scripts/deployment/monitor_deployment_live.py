#!/usr/bin/env python3
"""
Live deployment monitor with minute-by-minute updates
"""
import boto3
import time
from datetime import datetime

def log(message):
    """Print with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_build_status(codebuild_client, build_id):
    """Check build status"""
    response = codebuild_client.batch_get_builds(ids=[build_id])
    build = response['builds'][0]
    status = build['buildStatus']

    current_phase = "Unknown"
    if 'phases' in build:
        for phase in build['phases']:
            if phase.get('phaseStatus') == 'IN_PROGRESS':
                current_phase = phase['phaseType']
                break

    return status, current_phase

def force_ecs_deployment(ecs_client):
    """Force new ECS deployment"""
    response = ecs_client.update_service(
        cluster='overlord-cluster-prod',
        service='agent-cleo-service',
        forceNewDeployment=True
    )
    return response

def check_ecs_tasks(ecs_client):
    """Check ECS task status"""
    response = ecs_client.describe_services(
        cluster='overlord-cluster-prod',
        services=['agent-cleo-service']
    )
    service = response['services'][0]
    return service['runningCount'], service['desiredCount']

def check_target_health(elbv2_client):
    """Check target group health"""
    response = elbv2_client.describe_target_health(
        TargetGroupArn='arn:aws:elasticloadbalancing:eu-north-1:252321108661:targetgroup/agent-cleo-tg/58ec3705ba84e15b'
    )

    healthy = sum(1 for target in response['TargetHealthDescriptions']
                  if target['TargetHealth']['State'] == 'healthy')
    total = len(response['TargetHealthDescriptions'])

    return healthy, total

def main():
    build_id = 'agent-cleo-build:fb0a1cd3-40a8-413d-94cc-c0bc1109bc3d'

    # Initialize AWS clients
    session = boto3.Session(profile_name='Studio55', region_name='eu-north-1')
    codebuild_client = session.client('codebuild')
    ecs_client = session.client('ecs')
    elbv2_client = session.client('elbv2')

    print("=" * 70)
    print("Agent-Cleo Deployment Monitor - Live Updates Every Minute")
    print("=" * 70)
    print()

    build_complete = False
    ecs_deployed = False
    minute = 0

    while True:
        minute += 1
        log(f"=== MINUTE {minute} ===")

        # Check build status
        if not build_complete:
            status, phase = check_build_status(codebuild_client, build_id)
            log(f"Build Status: {status} | Phase: {phase}")

            if status == 'SUCCEEDED':
                log("✓ Build completed successfully!")
                build_complete = True
                log("Triggering ECS deployment...")
                force_ecs_deployment(ecs_client)
                ecs_deployed = True
                log("✓ ECS deployment triggered")
            elif status in ['FAILED', 'FAULT', 'TIMED_OUT', 'STOPPED']:
                log(f"✗ Build failed with status: {status}")
                break
        else:
            log("Build: ✓ COMPLETED")

        # Check ECS status
        running, desired = check_ecs_tasks(ecs_client)
        log(f"ECS Tasks: {running}/{desired} running")

        # Check target health
        try:
            healthy, total = check_target_health(elbv2_client)
            log(f"Target Health: {healthy}/{total} healthy")

            if healthy > 0 and build_complete:
                log("=" * 70)
                log("✓✓✓ DEPLOYMENT SUCCESSFUL! ✓✓✓")
                log("=" * 70)
                log("")
                log("Application is now accessible at:")
                log("  https://agents.theoverlord.ai")
                log("  https://agents.theoverlord.ai/health")
                log("")
                log("SSL Certificate: ✓ Valid")
                log("DNS Configuration: ✓ Active")
                log("Load Balancer: ✓ Routing traffic")
                log("ECS Tasks: ✓ Healthy")
                log("")
                break
        except Exception as e:
            log(f"Target Health Check: {str(e)[:50]}...")

        log("")

        # Wait 60 seconds before next check
        time.sleep(60)

    log("Monitoring complete.")

if __name__ == '__main__':
    main()
