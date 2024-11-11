# Data Scraper Overview

This repository contains files for scraping the latest active carriers from the following site: https://www.transtats.bts.gov/OT_Delay/OT_DelayCause1.asp

## File Descriptions

- **`main.py`**:  
  The main script for the scraping the latest month of active carriers. The script utilises headless chrome to perform the scraping and uploads the data in an S3 bucket. It is set to run every month and is invoked automatically by AWS EventBridge.

- **`Dockerfile`**:  
  The docker file to dockerise main.py into a docker image. Due to size limitations on AWS Lambda and the multiple dependencies, main.py and its libraries are dockerised and uploaded to Amazon ECR, which is linked to AWS Lambda.
