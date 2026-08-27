# Future Production Deployment Architecture & Security

## 1. Production Deployment Strategy
- **Control Plane**: Stateless FastAPI replicas behind an AWS ALB or Cloudflare Load Balancer.
- **Background Workers**: Autoscaling Celery/ARQ worker instances consuming evaluation jobs from Redis cluster.
- **Relational Database**: Managed PostgreSQL (AWS RDS / GCP Cloud SQL) with read replicas and automated backups.
- **Tracing Storage**: High-volume trace event stream offloading to ClickHouse and S3 object storage.

## 2. Security & Compliance Foundation
- **Secrets Management**: Integration with AWS Secrets Manager / HashiCorp Vault. Never commit secrets to Git.
- **TLS & Encryption**: End-to-end TLS 1.3 encryption in transit; AES-256 encryption at rest.
- **Tenant Isolation**: Mandatory `organization_id` filters enforced across all DB repositories and cache key namespaces.
- **PII & Data Retention**: Automatic masking of sensitive prompt tokens; configurable organization retention windows.
