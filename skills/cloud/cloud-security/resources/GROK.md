# Cloud Security

## Overview

Cloud Security encompasses the policies, controls, and practices that protect cloud infrastructure, applications, and data from threats. This skill covers identity management, network security, encryption, compliance frameworks, and threat detection. Cloud security balances accessibility with protection across multi-cloud and hybrid environments.

## Core Capabilities

Identity and Access Management controls who can access what resources with least-privilege principles. Network security controls including security groups, NACLs, and VPC endpoints isolate and protect cloud resources. Encryption at rest and in transit protects data throughout its lifecycle. Compliance frameworks map controls to regulatory requirements like SOC2, HIPAA, and PCI-DSS.

Threat detection services monitor for anomalies and potential attacks. Security monitoring and logging provide visibility into security events. Incident response procedures prepare for security breaches. Disaster recovery planning ensures business continuity.

## Usage Examples

```python
from cloud_security import CloudSecurity

cs = CloudSecurity()

iam_policy = cs.create_iam_policy(
    name="S3ReadOnlyPolicy",
    effect="Allow",
    actions=["s3:GetObject", "s3:ListBucket"],
    resources=["arn:aws:s3:::data-bucket/*", "arn:aws:s3:::data-bucket"]
)

role = cs.create_role(
    role_name="LambdaExecutionRole",
    assume_role_policy={
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    },
    policies=[iam_policy]
)

security_group = cs.create_security_group(
    name="web-sg",
    vpc_id="vpc-12345678",
    rules=[
        {"cidr": "0.0.0.0/0", "protocol": "tcp", "from_port": 443, "to_port": 443},
        {"cidr": "10.0.0.0/16", "protocol": "tcp", "from_port": 5432, "to_port": 5432}
    ]
)

encryption = cs.configure_encryption(
    service="rds",
    key_management="aws_kms",
    encryption_at_rest=True,
    encryption_in_transit=True
)

vpc_endpoint = cs.create_vpc_endpoint(
    service_name="com.amazonaws.region.s3",
    vpc_id="vpc-12345678"
)

waf = cs.configure_waf(
    name="web-waf",
    rules=[
        cs.create_waf_rule(
            rule_name="sqli-protection",
            statement={"byteMatch": {"field_to_match": "BODY", "positionalConstraint": "CONTAINS", "search_string": "' OR '1'='1", "text_transformations": [{"type": "URL_DECODE", "priority": 0}]}},
            action={"block": {}},
            priority=1
        )
    ],
    default_action="allow"
)

shield = cs.configure_shield(protection_level="advanced")

guardduty = cs.configure_guardduty(
    enable=True,
    finding_publishing_frequency="SIX_HOURS"
)

config_rule = cs.create_config_rule(
    rule_name="s3-bucket-public-read-prohibited",
    source={"owner": "AWS", "source_identifier": "S3_BUCKET_PUBLIC_READ_PROHIBITED"},
    scope={"compliance_resource_types": ["AWS::S3::Bucket"]},
    trigger={"configuration_changes": {}}
)

security_hub = cs.configure_security_hub(
    enable=True,
    standards=["AWS Foundational Security Best Practices", "CIS AWS Foundations Benchmark"],
    integrations=["GuardDuty", "Inspector", "Macie"]
)

key_rotation = cs.configure_key_rotation(
    key_id="arn:aws:kms:region:123456789:key/key-id",
    rotation_period_days=365,
    automatic=True
)

network_policy = cs.create_network_policy(
    name="api-network-policy",
    selector={"matchLabels": {"app": "api"}},
    ingress=[{"from": [{"podSelector": {"matchLabels": {"app": "frontend"}}}]}],
    egress=[{"to": [{"ipBlock": {"cidr": "10.0.0.0/16", "except": []}]}]
)

service_mesh = cs.configure_service_mesh_security(
    mtls_enabled=True,
    authorization_policy={"rules": [{"from": {"source": {"principals": ["*"]}}, "to": {"operation": "*"}}]}
)

secrets_policy = cs.create_secrets_policy(
    rotation_enabled=True,
    rotation_period_days=30
)

dlp = cs.configure_dlp_policy(
    name="pii-detection",
    detectors=[
        {"type": "EMAIL_ADDRESS"},
        {"type": "SOCIAL_SECURITY_NUMBER"},
        {"type": "CREDIT_CARD_NUMBER"},
        {"type": "IP_ADDRESS"}
    ],
    actions=[{"quarantine": {"destination": {"quarantine": {}}}}]
)

dr_plan = cs.create_disaster_recovery_plan(
    rpo_hours=4,
    rto_hours=24,
    backup_strategy="continuous"
)

incident_response = cs.create_incident_response_plan(
    escalation_policy={"levels": [1, 2, 3], "timeouts": [15, 30, 60]},
    runbooks=[
        {"name": "initial-assessment", "steps": ["identify", "contain", "assess"]},
        {"name": "containment", "steps": ["isolate", "block", "notify"]},
        {"name": "eradication", "steps": ["remove_threat", "patch", "harden"]}
    ]
)
```

## Best Practices

Implement defense in depth with multiple security layers. Apply least-privilege principles for all access decisions. Encrypt all data at rest and in transit. Enable comprehensive logging and monitoring.

Regularly audit and assess security posture. Automate security scanning in CI/CD pipelines. Train teams on security awareness and procedures. Test incident response plans regularly. Keep up with evolving threats and security best practices.

## Related Skills

- Security Testing (vulnerability assessment)
- Network Engineering (network security)
- Compliance (regulatory requirements)
- DevSecOps (automated security)

## Use Cases

Enterprise cloud security protects sensitive data and regulated workloads. Multi-cloud security provides consistent controls across AWS, Azure, and GCP. Compliance management maps controls to regulatory requirements. DevSecOps integrates security throughout the development lifecycle.
