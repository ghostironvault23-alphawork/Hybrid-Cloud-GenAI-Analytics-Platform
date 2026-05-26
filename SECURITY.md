# Security Policy

## Security Controls Included

- API key middleware for local demo
- Input validation using Pydantic
- Basic role-based access checks
- Sensitive field masking before storage and AI processing
- No secrets committed to repository
- `.env.example` included for safe configuration

## Production Recommendations

- Replace demo API key with Cognito or enterprise SSO
- Use IAM least privilege
- Encrypt S3, DynamoDB, RDS, and OpenSearch with KMS
- Enable CloudTrail and CloudWatch alarms
- Add WAF for public APIs
- Use VPC endpoints and private networking
- Add Bedrock Guardrails or equivalent safety layer
