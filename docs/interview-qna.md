# Interview Q&A

| Question | Strong Answer |
|---|---|
| What problem does this project solve? | It solves scattered enterprise data analysis by connecting cloud logs, IoT telemetry, on-prem tickets, and business events into one AI-powered analysis platform. |
| Why did you use a middle layer? | The middle layer validates, masks, routes, and processes data before it reaches storage or AI. This improves security, accuracy, and governance. |
| What is the role of the data lake? | The data lake stores raw and processed events so the platform can perform analytics, search, and AI-based analysis. |
| Why use RAG? | RAG helps the AI answer using trusted enterprise context instead of guessing from general knowledge. |
| How did you handle security? | I added validation, masking, role checks, audit logs, and production recommendations for IAM, KMS, Cognito, WAF, and CloudTrail. |
| How would you deploy this to AWS? | I would deploy the API behind API Gateway, use Lambda or ECS for backend logic, S3 as data lake, DynamoDB for transactions, Bedrock for GenAI, and CloudWatch for monitoring. |
| How would you deploy this to Azure? | I would use Azure App Service or Functions for backend, ADLS Gen2 for data lake, Cosmos DB for transactions, Azure OpenAI for AI, Azure AI Search for RAG, and Application Insights for monitoring. |
| How would you reduce hallucination? | I would retrieve trusted context first, pass only relevant data to the model, use strict prompts, and add response validation. |
| How would you scale it? | I would add event-driven ingestion, queues, Step Functions, OpenSearch or Azure AI Search, ECS/EKS, dashboards, and cloud-native monitoring. |
| What is the business value? | It reduces manual analysis, speeds up root cause investigation, improves reporting, and converts raw enterprise data into actionable insights. |
| What did you learn? | I learned how to combine cloud architecture, data engineering, security, monitoring, and GenAI into an enterprise-ready system. |
