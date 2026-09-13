# Amazon API Gateway

API Gateway is a fully managed service for creating, publishing, and securing APIs at any scale, commonly used as the front door to serverless applications.

## API Types
REST APIs offer the full feature set including request/response transformation and usage plans. HTTP APIs are a lighter, lower-latency, lower-cost alternative for simpler proxy use cases. WebSocket APIs support persistent, two-way real-time connections.

## Integration Types
Lambda proxy integration passes the entire request to a Lambda function and returns its response directly — the most common pattern for serverless backends. HTTP integration forwards requests to an existing HTTP endpoint, and Mock integration returns a response without an actual backend, useful for testing.

## Security and Throttling
API keys combined with usage plans control and meter access per client, enforcing rate limits and quotas. Authorizers (Lambda-based or Cognito-based) validate tokens before a request reaches your backend. Throttling protects backend services from being overwhelmed by traffic spikes.

## Custom Domains
Custom domain names with ACM-managed TLS certificates let you expose APIs under your own branded domain instead of the default AWS-generated URL.