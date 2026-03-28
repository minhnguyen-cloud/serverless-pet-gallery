# 🐾 PetMetric: Serverless Image Gallery & Real-time Analytics
A secure, fully serverless web application that demonstrates **AWS Web Identity Federation** (OAuth 2.0 via Google) and an event-driven architecture for real-time image view tracking.
## 🎯 Project Overview
This project allows users to log in using their Google accounts to view images hosted securely on AWS. Instead of creating permanent IAM users, the application uses **AWS Cognito** to exchange Google ID tokens for temporary, least-privilege AWS credentials.
Going beyond standard authentication, this architecture introduces a custom **Event-Driven Analytics Flow**. Every time an image is accessed, an AWS Lambda function is triggered to increment the view count in a DynamoDB table, providing real-time metrics without provisioning any servers.
## 🏗️ Architecture Diagram

```mermaid
graph TD
    %% Define Entities
    User((🧑 User))
    Google[🌐 Google Identity Provider]

    %% AWS Cloud Subgraph
    subgraph AWS Cloud [☁️ AWS Cloud - Serverless App]
        Cognito[🔐 Amazon Cognito<br>Identity Pool]
        CloudFront[⚡ Amazon CloudFront<br>CDN]
        S3[🪣 Amazon S3<br>Pet Images Bucket]
        EventBridge[🎯 Amazon EventBridge<br>Event Bus]
        Lambda[⚙️ AWS Lambda<br>View Counter]
        DynamoDB[📊 Amazon DynamoDB<br>Metrics Table]
    end

    %% Authentication Flow
    User -- "1. Login (OAuth 2.0)" --> Google
    Google -- "2. Returns ID Token" --> User
    User -- "3. Exchanges Token" --> Cognito
    Cognito -- "4. Issues Temp Credentials" --> User

    %% Image Access Flow
    User -- "5. Requests Image" --> CloudFront
    CloudFront -- "Fetch (Cache Miss)" --> S3
    CloudFront -- "Returns Image" --> User

    %% Analytics Flow (Event-Driven)
    S3 -. "6. S3 GetObject Event" .-> EventBridge
    EventBridge -. "7. Triggers" .-> Lambda
    Lambda -. "8. Update View Count (+1)" .-> DynamoDB

    %% Styling
    classDef aws fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:black;
    class Cognito,CloudFront,S3,EventBridge,Lambda,DynamoDB aws;
