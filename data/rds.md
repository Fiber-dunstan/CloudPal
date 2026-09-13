# Amazon RDS (Relational Database Service)

RDS manages relational databases in the cloud, handling patching, backups, and hardware provisioning so you can focus on schema and queries.

## Supported Engines
RDS supports MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, and Amazon Aurora (AWS's own MySQL/PostgreSQL-compatible engine, built for higher performance and availability).

## High Availability and Scaling
Multi-AZ deployments maintain a synchronous standby replica in another Availability Zone for automatic failover during outages. Read Replicas serve read-only traffic asynchronously, offloading read load from the primary instance and can even be promoted to standalone databases.

## Operations
RDS takes automated backups within a configurable retention window and supports point-in-time recovery. Parameter groups and option groups let you tune engine-specific settings without modifying the underlying instance directly.

## RDS vs. Aurora
Aurora typically offers higher throughput, faster failover, and auto-scaling storage compared to standard RDS engines, at a higher baseline cost — a common choice for production workloads needing extra performance headroom.