#!/usr/bin/env python3
"""Monitor CodeBuild and trigger ECS deployment when complete"""
import boto3
import time
import sys

def monitor_build(codebuild_client, build_id):
    """Monitor build progress"""
    print(f"Monitoring build: {build_id}")
    print()

    max_wait = 60  # 30 minutes
    checks = 0

    while checks < max_wait:
        checks += 1
        response = codebuild_client.batch_get_builds(ids=[build_id])
        build = response['builds'][0]
        status = build['buildStatus']

        # Get current phase info
        current_phase = None
        if 'phases' in build:
            for phase in build['phases']:
                if phase.get('phaseStatus') == 'IN_PROGRESS':
                    current_phase = phase['phaseType']
                    break

        if current_phase:
            print(f"[{checks}/{max_wait}] Status: {status} | Phase: {current_phase}")
        else:
            print(f"[{checks}/{max_wait}] Status: {status}")

        if status == 'SUCCEEDED':
            print()
            print("[+] Build completed successfully!")
            return True
        elif status in ['FAILED', 'FAULT', 'TIMED_OUT', 'STOPPED']:
            print()
            print(f"[!] Build failed with status: {status}")
            if 'phases' in build:
                for phase in build['phases']:
                    if phase.get('phaseStatus') == 'FAILED':
                        print(f"    Failed phase: {phase['phaseType']}")
            return False
        elif status == 'IN_PROGRESS':
            time.sleep(30)
        else:
            time.sleep(10)

    print("[!] Timeout waiting for build")
    return False

def force_ecs_deployment(ecs_client):
    """Force new ECS deployment"""
    print()
    print("="*70)
    print("Updating ECS Service")
    print("="*70)
    print()

    cluster = 'overlord-cluster-prod'
    service = 'agent-cleo-service'

    print(f"[*] Forcing new deployment of {service}...")

    response = ecs_client.update_service(
        cluster=cluster,
        service=service,
        forceNewDeployment=True
    )

    print(f"[+] Deployment triggered")
    print(f"[*] Service: {service}")
    print(f"[*] Desired count: {response['service']['desiredCount']}")
    print()
    print("[*] ECS will pull the new Docker image and redeploy")
    print(f"[*] Monitor at: https://console.aws.amazon.com/ecs/home?region=eu-north-1#/clusters/{cluster}/services/{service}")

def main():
    build_id = 'agent-cleo-build:4d0c8cb2-d65c-4547-9698-2757fa2862fa'

    # Initialize AWS clients
    session = boto3.Session(profile_name='Studio55', region_name='eu-north-1')
    codebuild_client = session.client('codebuild')
    ecs_client = session.client('ecs')

    print("="*70)
    print("Build Monitor and Auto-Deploy")
    print("="*70)
    print()

    # Monitor build
    success = monitor_build(codebuild_client, build_id)

    if success:
        # Trigger ECS deployment
        force_ecs_deployment(ecs_client)

        print()
        print("="*70)
        print("[+] Deployment Complete!")
        print("="*70)
        print()
        print("Wait 2-3 minutes for new tasks to start, then test:")
        print("  https://agents.theoverlord.ai/health")
    else:
        print()
        print("[!] Build failed - skipping ECS deployment")
        print("[*] Check CloudWatch Logs for build errors")
        sys.exit(1)

if __name__ == '__main__':
    main()
