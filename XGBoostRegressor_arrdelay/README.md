# Airline Arrival Delay Prediction

## Overview
This project contains a Jupyter notebook used to train an XGBoostRegressor model to predict airline arrival delays. The notebook is designed to run on Amazon SageMaker, utilizing its managed notebook environment for efficient model training and deployment. Additionally, we include a Lambda function to deploy the model as an API for real-time predictions on live flight data.

## File Description

- **`airlines-xgboostregressor-arrdelay.ipynb`**  
  This Jupyter notebook implements the following:
  - **Data Loading and Preprocessing**: Loads the airline dataset and prepares features for training the arrival delay prediction model.
  - **Model Training**: Uses the XGBoostRegressor algorithm to train a predictive model on the processed data.
  - **Model Evaluation**: Assesses the model’s performance, tuning hyperparameters as needed to optimize for accuracy in predicting arrival delays.
  - **Deployment**: In this project, the trained model is saved as a `.pkl` file, along with the feature columns, and uploaded to AWS S3. An AWS Lambda function is used to load the model and perform predictions, which are then exposed via an AWS API Gateway endpoint for external access.

- **`lambda_function.py`**  
  The Lambda function script for making predictions:
  - **Model Loading**: The script loads the model and feature columns from S3 when the Lambda function is triggered.
  - **Prediction**: It processes clean live flight data from an S3 bucket and uses the loaded model to generate arrival delay predictions.
  - **Output**: Returns the predicted arrival delay in json.
  - **API Integration**: This Lambda function is hosted on AWS API Gateway, allowing us to send a POST request to retrieve arrival delay predictions.

- **`Dockerfile`**  
  The Dockerfile used to containerize the Lambda function. By deploying the function as a Docker image, we can use custom dependencies and configurations that fit our model’s requirements. This Docker image is uploaded to AWS Lambda to provide a scalable and flexible environment for the model inference.

## Our Deployment Process

For our deployment setup:
1. **Model Storage**: The trained model file (`.pkl`) and a reference to the feature columns are saved in an S3 bucket.
2. **AWS Lambda for Predictions**: A Lambda function is configured to load the model and perform predictions. This function retrieves the model file and features from S3, together with the cleaned live flight data as model input.
3. **API Gateway**: An AWS API Gateway is configured to expose the Lambda function as a REST API, allowing external applications to send requests and receive arrival delay predictions in real-time.

## Requirements
- **Amazon SageMaker**: The notebook is designed to be run on a SageMaker-managed notebook instance. (For building of models using the `airlines-xgboostregressor-arrdelay.ipynb` file)
- **AWS Lambda**: The Lambda function allows for real-time predictions based on live data.
- **API Gateway**: Exposes the Lambda function as an API endpoint.
