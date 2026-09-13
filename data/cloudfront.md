# AWS CloudFront##

Amazon CloudFront is a **Content Delivery Network (CDN)** that securely delivers websites, APIs, videos, images, and other content to users with low latency by serving it from AWS edge locations close to them.

## How It Works##

A CloudFront distribution sits between users and an **origin** such as S3, EC2, an Application Load Balancer (ALB), or API Gateway. When a user requests content, CloudFront checks its nearest edge location for a cached copy. If the content is not cached, CloudFront retrieves it from the origin, returns it to the user, and can cache it for future requests.

## Caching and Performance##

CloudFront caches frequently requested content at edge locations around the world, reducing the number of requests sent to the origin and improving response times. Cache behaviors allow you to control which content is cached, how long it remains cached, and which HTTP methods are allowed.

## Security##

CloudFront supports **HTTPS/TLS**, AWS WAF, AWS Shield, and access controls to protect applications and content. With **Origin Access Control (OAC)**, CloudFront can securely access private S3 buckets while preventing users from accessing the S3 content directly.

## Common Patterns##

Serving static websites from S3, accelerating dynamic websites running behind an ALB, delivering videos and images globally, protecting APIs through CloudFront and AWS WAF, and securely connecting CloudFront to private S3 content using Origin Access Control.
