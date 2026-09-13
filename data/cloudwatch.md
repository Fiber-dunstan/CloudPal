# Amazon CloudWatch

Amazon CloudWatch is AWS's monitoring and observability service, collecting metrics, logs, and events from AWS resources and applications.

## Metrics and Alarms
CloudWatch automatically collects metrics like CPU utilization and network I/O. A CloudWatch Alarm watches a metric and triggers an action — like an SNS notification, an Auto Scaling action, or a Lambda function — when a threshold is breached. Composite Alarms combine multiple alarms with AND/OR logic to reduce noisy alerting.

## Logs
CloudWatch Logs centralizes log data from EC2, Lambda, and ECS. Metric filters extract numeric values from log lines to create custom metrics, useful for counting error occurrences over time.

## Anomaly Detection and Dashboards
CloudWatch Anomaly Detection uses machine learning to build an expected value band for a metric based on historical patterns, triggering alarms on unusual deviations rather than fixed thresholds. Dashboards combine metrics from multiple services into a single customizable view for at-a-glance health monitoring.

## CloudTrail vs. CloudWatch
CloudTrail records API calls for auditing ("who did what"); CloudWatch focuses on performance ("how is it performing"). They're often used together for full observability.