# 🏥 Seamless Healthcare Data Pipeline & Dashboard with AWS CI/CD

# Hospital Management System
## Problem Statement 📌

Modern hospitals generate huge amounts of structured and unstructured data from various sources, including electronic health records (EHRs), patient admissions, billing systems, and feedback surveys. Efficient processing and analysis of this data are crucial for optimizing hospital operations, reducing patient wait times, and improving healthcare services.

However, traditional data processing methods face multiple challenges:

✅ Heterogeneous data sources (on-prem databases, JSON, CSV, etc.).

✅ Data inconsistency and missing values lead to inaccurate reporting.

✅ Manual reporting delays decision-making.

✅ Lack of real-time monitoring affects hospital efficiency.

## Solution

This project builds a fully automated cloud-based ETL pipeline using AWS services to extract, transform, and load (ETL) healthcare data into a structured, analytics-ready format. A Power BI dashboard is integrated for data visualization and insights, enabling hospital management to monitor key performance indicators (KPIs) in real-time.

## 3️⃣ Data Extraction (Sources & Methods) 

📌 On-Premises Database Extraction (MySQL to AWS S3)
I developed a Python script that connects to an on-prem MySQL database, extracts structured data (such as patient records), and uploads it to an AWS S3 bucket using the Boto3 library.

Key Steps:

✔ Established a secure connection to the on-prem database using PyMySQL.

✔ Extracted patient and hospital data, converted it into a Pandas DataFrame.

✔ Saved the data as a CSV file and uploaded it to S3.

✔ Automated the extraction process for periodic data refresh.

Technologies Used:
Python (PyMySQL, Pandas, Boto3)

AWS S3 for cloud storage

📌 CSV File Ingestion (AWS Lambda & AWS Glue)

For handling CSV files, I implemented a serverless AWS Lambda function that triggers whenever a new CSV file is uploaded to S3. The function:

✔ Reads the CSV file metadata.

✔ Validates and transforms the data.

✔ Stores it in AWS Glue for ETL processing.

✔ Makes the data queryable via AWS Athena.

📌 JSON File Processing (AWS Lambda + S3 + SNS Alerts)
For handling semi-structured JSON data, I designed an automated data pipeline using:

✔ AWS Lambda – Cleans and transforms JSON files.

✔ AWS S3 – Stores raw and processed JSON files.

✔ AWS CloudWatch – Monitors execution and logs errors.

✔ AWS SNS (Simple Notification Service) – Sends alerts on success/failure

Challenges addressed:
✅ Data freshness: Automates periodic data syncs.

✅ Security: Uses IAM roles & VPN for secure data transfer.

## 🏥 System Architecture 🖥️
The system uses AWS services like Lambda, Glue, S3, Athena, Redshift, and CodePipeline to automate the ETL process for healthcare data. CloudFormation helps set up and manage the infrastructure, while CloudWatch monitors the system's performance. SNS is used for sending alerts, and Power BI provides real-time dashboards for hospital management to track key performance indicators (KPIs).

![Blank diagram (1)](https://github.com/user-attachments/assets/5bd54ffb-0327-4e9b-a476-0d9d2a33cd0c)

## 🛠️ Implementation
Steps:

1️⃣ Moving Data from On-Prem to AWS S3 (Using AWS CLI)
To begin the ETL process, I first uploaded raw hospital data (CSV & JSON files) from an on-premises system to an AWS S3 bucket using the AWS CLI.

Step 1: Verify AWS CLI Configuration

Before transferring data, I ensured that the AWS CLI was configured correctly with the necessary credentials.

![image](https://github.com/user-attachments/assets/22717a0f-2eb8-4ef5-ae9b-c5d45e12264a)


Copy dato to S3 bucket using aws CLI

![image](https://github.com/user-attachments/assets/a9db2d51-a148-4aea-b8c6-fa1ebd3ffe0e)

![image](https://github.com/user-attachments/assets/cf0c08e1-feab-4be7-83ef-007c66024397)

![image](https://github.com/user-attachments/assets/3a4bfc32-afce-4d77-9c16-411508c25ce4)

Successfully Upload all files from different data source to S3 bucket

![image](https://github.com/user-attachments/assets/d9e47d31-e610-49a8-ac3b-e0a445d79b24)


## Data Cataloging with AWS Glue Crawler
After uploading raw hospital data (CSV, JSON, etc.) to S3, I used AWS Glue Crawler to:

Detect Schema:

Automatically scans the data and infers its structure (e.g., column names, data types).

Create Data Catalog:

Generates tables in the Glue Data Catalog, making the data queryable with tools like AWS Athena.

![image](https://github.com/user-attachments/assets/3c580fb2-1186-47af-84e6-d6913ef50dcd)


![image](https://github.com/user-attachments/assets/a128088d-5a50-4cc7-9b89-066ddb4c18be)


![image](https://github.com/user-attachments/assets/4f8bad0f-6759-4bce-8ab9-d3b6239618cf)

The AWS Glue Crawler successfully uploaded the schema structure to the database, and I found that one of the files was in JSON format. To make the data easier to work with, I created a Lambda function that converts the JSON into Parquet format. Parquet is a more efficient format because it saves storage space and speeds up queries, especially for large datasets. This helps make the data ready for further analysis.

## Data Transformation:

An AWS Lambda function is triggered automatically when new files are uploaded to S3.
The Lambda function processes the data (cleans, validates, and transforms it) and converts it into Parquet format.

The transformed data is stored back in S3 for further analysis.

![image](https://github.com/user-attachments/assets/a845ede0-7ac6-48f3-bdea-173f195064e2)

![image](https://github.com/user-attachments/assets/d20d83a1-63e9-46df-8897-f8b3ef5a5da1)


![image](https://github.com/user-attachments/assets/d704818f-04ee-42e7-aa4a-2425ba23ddc0)




![image](https://github.com/user-attachments/assets/af2c91a9-3df8-4944-8d14-b212c426ff7d)





![image](https://github.com/user-attachments/assets/a8b1208c-8e1a-4a09-8fb4-cd3f094a84c0)



Cleaned Data in proper format

![image](https://github.com/user-attachments/assets/13d97e1c-8f26-4052-8040-f77379a38e04)


To ensure smooth monitoring and timely alerts, I implemented AWS SNS (Simple Notification Service)
SNS sends real-time notifications, ensuring that the team is instantly alerted about successful data processing
![image](https://github.com/user-attachments/assets/9e17f352-ee87-4173-b484-ff269f263dac)


![image](https://github.com/user-attachments/assets/7c4b874b-483e-424e-8c3f-62ba3afe2a06)
Once the data is cleaned, transformed, and loaded into S3, it will then be transferred to the Redshift data warehouse for further analysis. This ensures that the data is ready for efficient querying and reporting, enabling deeper insights and informed decision-making.
![image](https://github.com/user-attachments/assets/478a6bd1-3256-4012-92c2-dc06dbd91d87)


Testing Connection
![image](https://github.com/user-attachments/assets/6e2702e3-bdd4-42a6-a1aa-4057a31beff3)


Now create Visual ETL pipeline to load data from s3 to Redshift
![image](https://github.com/user-attachments/assets/ea5d5113-509f-4aa8-9b17-39ac26a264b0)

![image](https://github.com/user-attachments/assets/6182caa4-b766-472e-af5f-f11dd45e2dea)


![image](https://github.com/user-attachments/assets/df0e511f-787c-49cd-a67a-ab3969e16c14)

Before Loading into Redshift
![image](https://github.com/user-attachments/assets/9640f09a-8bd1-4816-b14f-ed7d07813720)

After succesful load

![image](https://github.com/user-attachments/assets/a17f7d03-6b03-4c3c-856c-b40f0b13a399)

# After a successful data load into Redshift, I connected the dataset to Power BI for visual reporting

![image](https://github.com/user-attachments/assets/e3931523-5ba9-489f-bd1f-e48e22a0d1ff)

# The data is then visualized through a custom Power BI dashboard, enabling real-time insights and interactive reporting.

![image](https://github.com/user-attachments/assets/4572e384-4196-47a5-b57f-22f8aec7cfa3)




## Setting Up AWS CodePipeline for CI/CD Integration



![image](https://github.com/user-attachments/assets/72f098b6-da29-40c7-b816-4a6e25b0230f)

To set up CI/CD for my project using AWS CodePipeline, I followed a step-by-step process to ensure a smooth pipeline creation and integration with GitHub, CodeBuild, and deployment stages. Below are the steps I took to set up the pipeline:

Step 1: IAM Role Creation for AWS CodePipeline

![image](https://github.com/user-attachments/assets/0e3a15b0-5d3a-4f48-aefa-aa07262db92c)

![image](https://github.com/user-attachments/assets/ec6488e5-caa0-4696-9409-0e3edbe86715)



Input Bucket: Contains files that the Glue script will read for processing.

Script Bucket: Stores AWS Glue ETL scripts for data extraction, transformation, and loading.

Output Bucket: Holds the processed data after the Glue ETL script runs.

Template Bucket: Stores paths and configuration files, with AWS automatically assigning temporary paths.
![image](https://github.com/user-attachments/assets/c815afb6-c13c-4012-877b-d1e1649bc386)


Creating  Codepipeline


![image](https://github.com/user-attachments/assets/c574e358-2f6b-486c-ab86-7e30c4738627)


Connecting it to github

![image](https://github.com/user-attachments/assets/23abf6cc-d011-4cef-bdca-a32bcf1ae4f7)

![image](https://github.com/user-attachments/assets/d286f1e9-19cb-42a5-b0cf-e89b94dc8de9)


![image](https://github.com/user-attachments/assets/a4953214-f994-43dd-9a82-310c44ea1a76)

once created the pipleine will run the pipeline


![image](https://github.com/user-attachments/assets/77650478-2a52-400b-98ed-b5fc2ef7ceb5)


![image](https://github.com/user-attachments/assets/5a4d8936-7bac-451b-8afe-f591fe13ff78)












