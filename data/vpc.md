# Amazon VPC (Virtual Private Cloud)

Amazon VPC lets you provision a logically isolated section of the AWS cloud, including your own IP ranges, subnets, route tables, and gateways.

## Subnets and Routing
Public subnets route to an Internet Gateway; private subnets reach the internet only via a NAT Gateway. Route tables control traffic flow between subnets and gateways within the VPC.

## Security
Security Groups are stateful firewalls at the instance level, evaluating allow rules only. Network ACLs are stateless firewalls at the subnet level, evaluated in rule-number order, and can explicitly deny traffic.

## Connectivity Options
VPC Peering connects two VPCs privately. VPC Endpoints come in two types: Gateway endpoints (for S3 and DynamoDB) and Interface endpoints, powered by PrivateLink, for most other AWS services — both avoid routing traffic over the public internet. Transit Gateway simplifies connecting many VPCs and on-premises networks through a central hub.

## Monitoring
VPC Flow Logs capture metadata about IP traffic going to and from network interfaces, useful for troubleshooting connectivity issues and security analysis.