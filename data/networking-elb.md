# Load Balancing and Route 53

Elastic Load Balancing distributes incoming traffic across multiple targets, and Route 53 handles DNS routing at the domain level.

## Load Balancer Types
An Application Load Balancer (ALB) operates at Layer 7 (HTTP/HTTPS), supporting path- and host-based routing rules — ideal for microservices and web applications. A Network Load Balancer (NLB) operates at Layer 4 (TCP/UDP), handling extreme throughput and preserving client IP addresses, suited for latency-sensitive workloads. The Classic Load Balancer is the legacy option, largely superseded by ALB and NLB.

## Target Groups and Health Checks
Traffic is routed to target groups (EC2 instances, IP addresses, or Lambda functions), and health checks continuously verify targets are responding correctly, automatically removing unhealthy ones from rotation.

## Amazon Route 53
Route 53 is AWS's scalable DNS service, also supporting domain registration and health checking. Routing policies include Simple, Weighted (split traffic by percentage), Latency-based (route to the lowest-latency region), Failover (active-passive), and Geolocation (route based on user location).