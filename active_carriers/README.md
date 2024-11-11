# Data Scraper Overview

This repository contains files for scraping the latest active carriers from the following site: https://www.transtats.bts.gov/OT_Delay/OT_DelayCause1.asp

## File Descriptions

- **`main.py`**:  
  The main script for the scraping the latest month of active carriers. The script utilises headless chrome to perform the scraping and uploads the data in an S3 bucket. It is set to run every month and is invoked automatically by AWS EventBridge.

- **`Dockerfile`**:  
  The docker file to dockerise main.py into a docker image and uploaded to Amazon ECR.

## Deployment Process
For our deployment set up:
1. **Storage of main scraper file** : Due to size limitations and multiple dependencies, the main scraper file and its dependencies are first dockerised on the local machine. The image is then uploaded to Amazon Elastic Container Registry.
2. **AWS Lambda Configuration**: A Lambda function is created to invoke the Docker image from the previous step. 
3. **AWS EventBridge for monthly invocation**: An EventBridge rule is set to run on the 1st of every month, at 12am (UTC time). This rule invokes the corresponding Lambda function, triggering the dockerised scraping image.
4. **S3 Storage**: Upon successful invocation, the updated list of active carriers are stored in an S3 bucket. Each monthly invocation replaces the previous CSV file.