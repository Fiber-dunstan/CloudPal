# Amazon DynamoDB

DynamoDB is a fully managed, serverless NoSQL key-value and document database designed for single-digit millisecond performance at any scale.

## Data Model
Every table has a primary key: either a simple partition key, or a composite key combining a partition key and a sort key. Partition keys determine how data is distributed across storage partitions, so choosing a high-cardinality key matters for even load distribution.

## Indexes
A Global Secondary Index (GSI) allows queries on non-key attributes with a different partition/sort key than the base table. A Local Secondary Index (LSI) shares the same partition key as the base table but a different sort key, and must be created at table creation time.

## Capacity Modes
On-Demand mode charges per request with no capacity planning needed, ideal for unpredictable traffic. Provisioned mode lets you set read/write capacity units ahead of time at a lower cost for predictable workloads, with optional auto scaling.

## Streams and Consistency
DynamoDB Streams capture a time-ordered sequence of item changes, commonly used to trigger Lambda functions for event-driven processing. Reads can be eventually consistent (default, cheaper) or strongly consistent (guarantees the latest write, costs more).