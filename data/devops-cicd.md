# DevOps and CI/CD on AWS

AWS provides a native CI/CD toolchain alongside strong support for third-party tools like GitHub Actions and Terraform.

## AWS-Native Pipeline Tools
CodePipeline orchestrates a release process across stages (source, build, test, deploy). CodeBuild compiles code, runs tests, and produces build artifacts. CodeDeploy automates application deployment to EC2, Lambda, or ECS, supporting in-place and blue/green deployment strategies.

## Infrastructure as Code
CloudFormation is AWS's native IaC service, defining resources in JSON or YAML templates that can be versioned and repeatably deployed. Terraform, a third-party tool, offers similar declarative infrastructure management but works across multiple cloud providers, making it a common choice for multi-cloud or cloud-agnostic teams.

## Deployment Strategies
Rolling deployments gradually replace old instances with new ones, minimizing downtime but running mixed versions temporarily. Blue/Green deployments run two full environments and switch traffic all at once, enabling instant rollback. Canary deployments shift a small percentage of traffic to the new version first, limiting blast radius if something goes wrong.

## GitHub Actions with AWS
GitHub Actions can authenticate to AWS using OpenID Connect (OIDC) to assume an IAM role directly, avoiding the need to store long-lived AWS access keys as repository secrets — the current best-practice approach for CI/CD security.