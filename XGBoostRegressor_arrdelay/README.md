# Airline Arrival Delay Prediction

## Overview
This project contains a Jupyter notebook used to train an XGBoostRegressor model to predict airline arrival delays. The notebook is designed to run on Amazon SageMaker, utilizing its managed notebook environment for efficient model training and deployment.

## File Description

- **`airlines-xgboostregressor-arrdelay.ipynb`**  
  This Jupyter notebook implements the following:
  - **Data Loading and Preprocessing**: Loads the airline dataset and prepares features for training the arrival delay prediction model.
  - **Model Training**: Uses the XGBoostRegressor algorithm to train a predictive model on the processed data.
  - **Model Evaluation**: Assesses the model’s performance, tuning hyperparameters as needed to optimize for accuracy in predicting arrival delays.
  - **Deployment**: In this project, the trained model is saved as a `.pkl` file, along with the feature columns, and uploaded to AWS S3. An AWS Lambda function is used to load the model and perform predictions, which are then exposed via an AWS API Gateway endpoint for external access.

## Our Deployment Process

For our deployment setup:
1. **Model Storage**: The trained model file (`.pkl`) and a reference to the feature columns are saved in an S3 bucket.
2. **AWS Lambda for Predictions**: A Lambda function is configured to load the model and perform predictions. This function retrieves the model file and features from S3.
3. **API Gateway**: An AWS API Gateway is configured to expose the Lambda function as a REST API, allowing external applications to receive arrival delay predictions in real-time.

## Requirements
- **Amazon SageMaker**: The notebook is designed to be run on a SageMaker-managed notebook instance.
