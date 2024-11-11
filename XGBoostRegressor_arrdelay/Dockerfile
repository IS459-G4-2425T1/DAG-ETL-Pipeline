# Use the official AWS Lambda Python runtime as the base image
FROM public.ecr.aws/lambda/python:3.8

# Install any required dependencies
RUN pip install pandas joblib boto3 xgboost

# Copy the Lambda function code into the container
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Command to run the Lambda function
CMD ["lambda_function.lambda_handler"]
