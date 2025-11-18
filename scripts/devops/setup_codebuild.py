#!/usr/bin/env python3
"""
Setup AWS CodeBuild project for Agent-Cleo
Automates the creation of IAM roles, CodeBuild project, and triggers first build
"""
import boto3
import json
import time
import os

def create_codebuild_role(iam_client):
    """Create IAM role for CodeBuild with necessary permissions"""
    role_name = 'agent-cleo-codebuild-role'

    # Trust policy for CodeBuild
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "codebuild.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

    # Check if role exists
    try:
        role = iam_client.get_role(RoleName=role_name)
        print(f"[*] IAM role already exists: {role_name}")
        return role['Role']['Arn']
    except iam_client.exceptions.NoSuchEntityException:
        pass

    # Create role
    print(f"[*] Creating IAM role: {role_name}")
    role = iam_client.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(trust_policy),
        Description='IAM role for Agent-Cleo CodeBuild project',
        Tags=[
            {'Key': 'Project', 'Value': 'Agent-Cleo'},
            {'Key': 'Platform', 'Value': 'Overlord'}
        ]
    )

    # Attach managed policies
    policies = [
        'arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser',
        'arn:aws:iam::aws:policy/CloudWatchLogsFullAccess'
    ]

    for policy_arn in policies:
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
        print(f"[+] Attached policy: {policy_arn}")

    # Create inline policy for additional permissions
    inline_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Resource": "arn:aws:logs:*:*:*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject"
                ],
                "Resource": "arn:aws:s3:::codepipeline-*/*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "secretsmanager:GetSecretValue"
                ],
                "Resource": "arn:aws:secretsmanager:eu-north-1:252321108661:secret:agent-cleo/*"
            }
        ]
    }

    iam_client.put_role_policy(
        RoleName=role_name,
        PolicyName='agent-cleo-codebuild-inline-policy',
        PolicyDocument=json.dumps(inline_policy)
    )
    print("[+] Created inline policy")

    # Wait for role to propagate
    print("[*] Waiting for IAM role to propagate...")
    time.sleep(10)

    return role['Role']['Arn']

def create_codebuild_project(codebuild_client, role_arn):
    """Create CodeBuild project"""
    project_name = 'agent-cleo-build'

    # Check if project exists
    try:
        project = codebuild_client.batch_get_projects(names=[project_name])
        if project['projects']:
            print(f"[*] CodeBuild project already exists: {project_name}")
            return project_name
    except Exception:
        pass

    # Create project
    print(f"[*] Creating CodeBuild project: {project_name}")

    # Load buildspec content
    with open('buildspec.yml', 'r') as f:
        buildspec_content = f.read()

    response = codebuild_client.create_project(
        name=project_name,
        description='Build and push Agent-Cleo Docker image to ECR',
        source={
            'type': 'NO_SOURCE',
            'buildspec': buildspec_content
        },
        artifacts={
            'type': 'NO_ARTIFACTS'
        },
        environment={
            'type': 'LINUX_CONTAINER',
            'image': 'aws/codebuild/standard:7.0',
            'computeType': 'BUILD_GENERAL1_SMALL',
            'environmentVariables': [
                {
                    'name': 'AWS_DEFAULT_REGION',
                    'value': 'eu-north-1',
                    'type': 'PLAINTEXT'
                },
                {
                    'name': 'AWS_ACCOUNT_ID',
                    'value': '252321108661',
                    'type': 'PLAINTEXT'
                },
                {
                    'name': 'IMAGE_REPO_NAME',
                    'value': 'agent-cleo',
                    'type': 'PLAINTEXT'
                },
                {
                    'name': 'IMAGE_TAG',
                    'value': 'latest',
                    'type': 'PLAINTEXT'
                }
            ],
            'privilegedMode': True  # Required for Docker builds
        },
        serviceRole=role_arn,
        tags=[
            {'key': 'Project', 'value': 'Agent-Cleo'},
            {'key': 'Platform', 'value': 'Overlord'}
        ],
        logsConfig={
            'cloudWatchLogs': {
                'status': 'ENABLED',
                'groupName': '/aws/codebuild/agent-cleo'
            }
        },
        cache={
            'type': 'LOCAL',
            'modes': ['LOCAL_DOCKER_LAYER_CACHE']
        }
    )

    print(f"[+] Created CodeBuild project: {project_name}")
    return project_name

def upload_source_to_s3(s3_client):
    """Upload source code to S3 for CodeBuild"""
    bucket_name = f"agent-cleo-build-{int(time.time())}"

    # Create bucket
    try:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'eu-north-1'}
        )
        print(f"[+] Created S3 bucket: {bucket_name}")
    except s3_client.exceptions.BucketAlreadyExists:
        print(f"[*] S3 bucket already exists: {bucket_name}")

    # Upload buildspec.yml
    with open('buildspec.yml', 'r') as f:
        s3_client.put_object(
            Bucket=bucket_name,
            Key='buildspec.yml',
            Body=f.read()
        )

    print("[+] Uploaded buildspec.yml to S3")
    return bucket_name

def start_build(codebuild_client, project_name):
    """Start a CodeBuild build"""
    print(f"[*] Starting build for project: {project_name}")

    # Get current directory path
    source_location = os.getcwd()

    response = codebuild_client.start_build(
        projectName=project_name,
        sourceTypeOverride='CODECOMMIT',  # We'll use local source
        sourceLocationOverride=source_location
    )

    build_id = response['build']['id']
    build_arn = response['build']['arn']

    print(f"[+] Build started!")
    print(f"    Build ID: {build_id}")
    print(f"    Build ARN: {build_arn}")
    print(f"[*] Monitor build at: https://console.aws.amazon.com/codesuite/codebuild/projects/agent-cleo-build/build/{build_id}")

    return build_id

def monitor_build(codebuild_client, build_id):
    """Monitor build progress"""
    print(f"[*] Monitoring build: {build_id}")
    print()

    while True:
        response = codebuild_client.batch_get_builds(ids=[build_id])
        build = response['builds'][0]
        status = build['buildStatus']

        print(f"[*] Build status: {status}")

        if status == 'SUCCEEDED':
            print("[+] Build completed successfully!")
            return True
        elif status in ['FAILED', 'FAULT', 'TIMED_OUT', 'STOPPED']:
            print(f"[!] Build failed with status: {status}")
            if 'phases' in build:
                for phase in build['phases']:
                    if phase.get('phaseStatus') == 'FAILED':
                        print(f"    Failed phase: {phase['phaseType']}")
                        if 'contexts' in phase:
                            for context in phase['contexts']:
                                print(f"      {context.get('message', '')}")
            return False
        elif status == 'IN_PROGRESS':
            print("    Build in progress...")
            time.sleep(30)
        else:
            time.sleep(10)

def main():
    # Set AWS profile and region
    os.environ['AWS_PROFILE'] = 'Studio55'
    region = 'eu-north-1'

    # Initialize AWS clients
    session = boto3.Session(profile_name='Studio55', region_name=region)
    iam_client = session.client('iam')
    codebuild_client = session.client('codebuild')
    s3_client = session.client('s3')

    print("="*70)
    print("Agent-Cleo CodeBuild Setup")
    print("="*70)
    print()

    # Step 1: Create IAM role
    print("[1/4] Creating IAM role for CodeBuild...")
    role_arn = create_codebuild_role(iam_client)
    print(f"[+] Role ARN: {role_arn}")
    print()

    # Step 2: Create CodeBuild project
    print("[2/4] Creating CodeBuild project...")
    project_name = create_codebuild_project(codebuild_client, role_arn)
    print()

    # Step 3: Start build
    print("[3/4] Starting initial build...")
    print("[!] Note: Build will fail if buildspec.yml and Dockerfile aren't in the source")
    choice = input("Do you want to start the build now? (y/n): ")

    if choice.lower() == 'y':
        try:
            build_id = start_build(codebuild_client, project_name)
            print()

            # Step 4: Monitor build
            print("[4/4] Monitoring build progress...")
            success = monitor_build(codebuild_client, build_id)

            if success:
                print()
                print("="*70)
                print("[+] SUCCESS! Docker image pushed to ECR")
                print("="*70)
                print()
                print("Next steps:")
                print("1. Register ECS task definition")
                print("2. Create ECS service")
                print("3. Configure Route 53 DNS")
            else:
                print()
                print("="*70)
                print("[!] Build failed - check CloudWatch Logs for details")
                print("="*70)
        except Exception as e:
            print(f"[!] Error starting build: {e}")
    else:
        print("[*] Skipping build. You can start it manually later:")
        print(f"    aws codebuild start-build --project-name {project_name} --region {region}")

    print()
    print("="*70)
    print("CodeBuild Setup Complete!")
    print("="*70)
    print()
    print(f"Project: {project_name}")
    print(f"Region: {region}")
    print(f"Role: {role_arn}")

if __name__ == '__main__':
    main()
