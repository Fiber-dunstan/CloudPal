# Amazon EC2 (Elastic Compute Cloud)

Amazon EC2 provides resizable compute capacity in the cloud in the form of virtual servers called instances. Instead of buying physical hardware, you launch instances on demand and pay only for what you use.

## Instance Types
EC2 offers instance families optimized for different workloads: general purpose (T3, M6), compute optimized (C6), memory optimized (R6), and storage optimized (I3, D3). Choosing the right family balances cost against CPU, memory, and I/O needs.

## Pricing Models
- On-Demand: pay by the second/hour with no commitment.
- Reserved Instances: commit to 1 or 3 years for a discount over On-Demand.
- Spot Instances: bid for unused capacity at up to 90% off, but can be reclaimed with short notice.
- Savings Plans: flexible usage-based commitment across instance families.

## Key Concepts
An AMI (Amazon Machine Image) is the template used to launch an instance. Security Groups act as virtual firewalls at the instance level. EBS volumes (gp3, io2, st1, sc1) provide persistent block storage, while instance store volumes are ephemeral. User Data scripts run once at first boot to bootstrap configuration.

## Placement and Metadata
Placement groups (cluster, spread, partition) control how instances are physically arranged for performance or fault isolation. The Instance Metadata Service (IMDS) lets code running on an instance query its own configuration, and IMDSv2 (token-based) is the security-hardened default.

## Auto Scaling
EC2 Auto Scaling automatically adjusts the number of running instances based on demand, using scaling policies tied to CloudWatch metrics like CPU utilization, paired with an Elastic Load Balancer for resilient horizontal scaling.