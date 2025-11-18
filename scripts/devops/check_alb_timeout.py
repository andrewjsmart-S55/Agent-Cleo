#!/usr/bin/env python3
"""Check ALB and Target Group timeout settings"""
import boto3

session = boto3.Session(profile_name='Studio55', region_name='eu-north-1')
elbv2_client = session.client('elbv2')

print("=" * 70)
print("ALB and Target Group Timeout Configuration")
print("=" * 70)
print()

# Get target groups
try:
    response = elbv2_client.describe_target_groups()
    target_groups = response.get('TargetGroups', [])
except Exception as e:
    print(f"Error getting target groups: {e}")
    target_groups = []

for tg in target_groups:
    if 'agent-cleo' in tg['TargetGroupName']:
        print(f"Target Group: {tg['TargetGroupName']}")
        print(f"  Protocol: {tg['Protocol']}")
        print(f"  Port: {tg['Port']}")
        print(f"  Deregistration Delay: {tg.get('DeregistrationDelay', 'N/A')} seconds")

        # Get target group attributes for more timeout settings
        tg_arn = tg['TargetGroupArn']
        attrs_response = elbv2_client.describe_target_group_attributes(
            TargetGroupArn=tg_arn
        )

        print(f"  Target Group Attributes:")
        for attr in attrs_response['Attributes']:
            if 'timeout' in attr['Key'] or 'delay' in attr['Key']:
                print(f"    - {attr['Key']}: {attr['Value']}")
        print()

# Get load balancers
response = elbv2_client.describe_load_balancers()

for lb in response['LoadBalancers']:
    if 'overlord' in lb['LoadBalancerName'].lower():
        print(f"Load Balancer: {lb['LoadBalancerName']}")
        print(f"  DNS: {lb['DNSName']}")
        print(f"  Scheme: {lb['Scheme']}")

        # Get load balancer attributes
        lb_arn = lb['LoadBalancerArn']
        attrs_response = elbv2_client.describe_load_balancer_attributes(
            LoadBalancerArn=lb_arn
        )

        print(f"  Load Balancer Attributes:")
        for attr in attrs_response['Attributes']:
            if 'timeout' in attr['Key'] or 'idle' in attr['Key']:
                print(f"    - {attr['Key']}: {attr['Value']}")
        print()

print("=" * 70)
