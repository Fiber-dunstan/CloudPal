# Containers on AWS: ECS, EKS, and Fargate

AWS offers two main ways to run containers: ECS (Amazon's own orchestrator) and EKS (managed Kubernetes), both of which can run on EC2 instances you manage or on Fargate, a serverless compute engine for containers.

## Amazon ECS
ECS uses Task Definitions to describe how containers should run (image, CPU/memory, networking). A Service keeps a specified number of tasks running and can integrate with a load balancer for zero-downtime deployments.

## Amazon EKS
EKS runs upstream, standard Kubernetes, so existing Kubernetes manifests, Helm charts, and tooling work largely unchanged. It suits teams that already have Kubernetes expertise or need to stay cloud-portable.

## Fargate
Fargate removes the need to provision or manage EC2 instances for your containers — you specify CPU and memory per task, and AWS handles the underlying infrastructure. It trades some cost efficiency at scale for significantly less operational overhead.

## ECR
Amazon ECR (Elastic Container Registry) is a managed Docker image registry, tightly integrated with IAM for access control and commonly used as the image source for both ECS and EKS deployments.

## Choosing Between Them
ECS is simpler to operate and AWS-native; EKS suits teams needing Kubernetes portability or already invested in the Kubernetes ecosystem. Fargate is a compute option layered on top of either.