# AWS IAM (Identity and Access Management)

IAM controls who can do what in an AWS account. It manages authentication (who you are) and authorization (what you're allowed to do).

## Core Entities
Users represent individual people or applications. Groups are collections of users sharing the same permissions. Roles are temporary identities assumed by users, applications, or AWS services (like an EC2 instance or Lambda function) — the recommended way to grant permissions instead of long-lived access keys.

## Policies
Policies are JSON documents that define permissions, attached to users, groups, or roles. AWS evaluates policies using an explicit-deny-wins model: an explicit Deny always overrides an Allow, and by default everything is denied unless explicitly allowed.

## Best Practices
Follow least privilege — grant only the permissions needed. Enable MFA (multi-factor authentication) for all users, especially the root account. Use IAM roles instead of embedding access keys in code. AWS IAM Identity Center (formerly SSO) centralizes access across multiple AWS accounts. Service-linked roles are predefined roles that let AWS services perform actions on your behalf.