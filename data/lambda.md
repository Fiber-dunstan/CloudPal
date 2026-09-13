# AWS Lambda

AWS Lambda is a serverless compute service that runs code in response to events without provisioning or managing servers, billed per millisecond of execution.

## How It Works
A Lambda function is code plus a handler. It can be triggered by API Gateway, S3 events, DynamoDB Streams, EventBridge, SQS, and more, scaling automatically from one request to thousands of concurrent invocations.

## Execution Model
A cold start happens when Lambda initializes a new environment, adding latency; a warm start reuses one. Provisioned Concurrency keeps environments warm for latency-sensitive workloads. Reserved concurrency caps how many instances of a function can run at once, protecting downstream systems.

## Configuration and Cost
Memory (128 MB–10,240 MB) also scales CPU proportionally, and timeout can be set up to 15 minutes. Lambda Layers let you share common code or dependencies across functions without repackaging them each time. Cost is driven by number of invocations plus GB-seconds of compute used — there's no charge when the function isn't running.

## Common Patterns
API backends with API Gateway, event-driven processing of S3 uploads or queue messages, scheduled tasks via EventBridge, orchestration with Step Functions, and auto-remediation logic reacting to CloudWatch alarms.