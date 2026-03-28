# 🐾 PetMetric: Serverless Image Gallery & Real-time Analytics
A secure, fully serverless web application that demonstrates **AWS Web Identity Federation** (OAuth 2.0 via Google) and an event-driven architecture for real-time image view tracking.
## 🎯 Project Overview
This project allows users to log in using their Google accounts to view images hosted securely on AWS. Instead of creating permanent IAM users, the application uses **AWS Cognito** to exchange Google ID tokens for temporary, least-privilege AWS credentials.
Going beyond standard authentication, this architecture introduces a custom **Event-Driven Analytics Flow**. Every time an image is accessed, an AWS Lambda function is triggered to increment the view count in a DynamoDB table, providing real-time metrics without provisioning any servers.
