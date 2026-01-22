# AWS Specialist Agent

## Overview

Expert in AWS cloud services, architecture, and best practices.

## Capabilities

- **EC2 Management**: Instance provisioning and management
- **S3 Storage**: Bucket management and optimization
- **Lambda Functions**: Serverless function development
- **Container Services**: ECS, EKS, and Fargate
- **AWS Security**: IAM, security groups, and compliance

## Usage

```python
from agents.aws-specialist.agent import AWSSpecialistAgent

agent = AWSSpecialistAgent()
instance = agent.provision_ec2(name="web-server", instance_type="t3.micro")
```
