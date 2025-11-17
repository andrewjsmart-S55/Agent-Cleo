#!/usr/bin/env python3
"""
Simple deployment script for Agent-Cleo to Overlord platform
Uploads code to S3, triggers CodeBuild, and deploys to ECS
"""
import boto3
import zipfile
import os
import time
from pathlib import Path

def create_deployment_package():
    """Create a ZIP file with all necessary code"""
    print("[*] Creating deployment package...")

    # Files to include
    files_to_include = [
        'app_new.py',
        'agent_utils.py',
        'todoist_integration.py',
        'Dockerfile',
        'requirements_new.txt',
        'buildspec.yml',
        'ecs-task-definition.json',
        'docker-compose.yml'
    ]

    # Directories to include
    dirs_to_include = [
        'src',
        'static',
        'templates',
        'Personal Agents',
        'Team Agents',
        'Worker Agents',
        'Expert Agents'
    ]

    zip_filename = 'agent-cleo-deployment.zip'

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add files
        for file in files_to_include:
            if os.path.exists(file):
                zipf.write(file)
                print(f"  + Added: {file}")

        # Add directories
        for dir_name in dirs_to_include:
            if os.path.exists(dir_name):
                for root, dirs, files in os.walk(dir_name):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            zipf.write(file_path)
                        except (FileNotFoundError, OSError) as e:
                            print(f"  ! Skipped (path too long or inaccessible): {file_path[:80]}...")
                            continue
                print(f"  + Added directory: {dir_name}")

    print(f"[+] Created: {zip_filename} ({os.path.getsize(zip_filename) / 1024 / 1024:.2f} MB)")
    return zip_filename

def upload_to_s3(s3_client, zip_filename):
    """Upload deployment package to S3"""
    bucket_name = 'agent-cleo-deployments-252321108661'

    # Create bucket if it doesn't exist
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"[*] Using existing S3 bucket: {bucket_name}")
    except:
        print(f"[*] Creating S3 bucket: {bucket_name}")
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'eu-north-1'}
        )

    # Upload ZIP
    key = f"deployments/{int(time.time())}/{zip_filename}"
    print(f"[*] Uploading to S3: s3://{bucket_name}/{key}")

    with open(zip_filename, 'rb') as f:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=f,
            ServerSideEncryption='AES256'
        )

    print(f"[+] Uploaded successfully")
    return bucket_name, key

def trigger_build_from_s3(codebuild_client, bucket, key):
    """Trigger CodeBuild from S3 source"""
    project_name = 'agent-cleo-build'

    print(f"[*] Triggering CodeBuild project: {project_name}")

    try:
        response = codebuild_client.start_build(
            projectName=project_name,
            sourceTypeOverride='S3',
            sourceLocationOverride=f"{bucket}/{key}"
        )

        build_id = response['build']['id']
        print(f"[+] Build started: {build_id}")
        print(f"[*] Monitor at: https://console.aws.amazon.com/codesuite/codebuild/projects/{project_name}")

        return build_id
    except codebuild_client.exceptions.ResourceNotFoundException:
        print(f"[!] CodeBuild project not found: {project_name}")
        print(f"[*] Run 'python setup_codebuild.py' first to create the project")
        return None

def main():
    print("="*70)
    print("Agent-Cleo Deployment Script")
    print("="*70)
    print()

    # Initialize AWS clients
    session = boto3.Session(profile_name='Studio55', region_name='eu-north-1')
    s3_client = session.client('s3')
    codebuild_client = session.client('codebuild')

    # Step 1: Create deployment package
    zip_filename = create_deployment_package()
    print()

    # Step 2: Upload to S3
    bucket, key = upload_to_s3(s3_client, zip_filename)
    print()

    # Step 3: Trigger CodeBuild
    build_id = trigger_build_from_s3(codebuild_client, bucket, key)

    if build_id:
        print()
        print("="*70)
        print("[+] Deployment initiated!")
        print("="*70)
        print()
        print(f"Build ID: {build_id}")
        print(f"S3 Location: s3://{bucket}/{key}")
        print()
        print("Next steps:")
        print("1. Monitor the build in AWS CodeBuild console")
        print("2. Once build succeeds, Docker image will be in ECR")
        print("3. Register ECS task definition")
        print("4. Create/update ECS service")
    else:
        print()
        print("[!] Could not trigger build - set up CodeBuild project first")
        print("[*] Run: python setup_codebuild.py")

    # Cleanup
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
        print(f"[*] Cleaned up: {zip_filename}")

if __name__ == '__main__':
    main()
