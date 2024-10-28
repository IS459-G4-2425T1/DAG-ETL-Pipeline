// modules/flow3/variables.tf

// Import shared resources
variable "shared_bucket_arn" {
  type        = string
  description = "ARN of the shared S3 bucket from shared module"
}

variable "lambda_role_arn" {
  type        = string
  description = "ARN of the shared Lambda execution role from shared module"
}

variable "user_input_data_bucket_name" {
  description = "Name of the S3 bucket for user input data"
  type        = string
}

variable "api_name" {
  description = "Name of the API Gateway REST API"
  type        = string
}

variable "lambda_function_zip" {
  description = "Path to the zipped Lambda function code for user input handler"
  type        = string
}

variable "lambda_function_name" {
  description = "Name of the Lambda function for user input handler"
  type        = string
}

variable "lambda_handler" {
  description = "Handler of the Lambda function for user input handler"
  type        = string
}

variable "lambda_runtime" {
  description = "Runtime for the Lambda function"
  type        = string
  default     = "python3.8"
}

variable "trigger_lambda_zip" {
  description = "Path to the zipped Lambda function code for triggering Glue job"
  type        = string
}

variable "trigger_lambda_name" {
  description = "Name of the Lambda function for triggering Glue job"
  type        = string
}

variable "trigger_lambda_handler" {
  description = "Handler of the Lambda function for triggering Glue job"
  type        = string
}

variable "invoke_sagemaker_lambda_zip" {
  description = "Path to the zipped Lambda function code for invoking SageMaker endpoint"
  type        = string
}

variable "invoke_sagemaker_lambda_name" {
  description = "Name of the Lambda function for invoking SageMaker endpoint"
  type        = string
}

variable "invoke_sagemaker_lambda_handler" {
  description = "Handler of the Lambda function for invoking SageMaker endpoint"
  type        = string
}

variable "glue_job_name" {
  description = "Name of the Glue ETL job"
  type        = string
}

variable "glue_role_arn" {
  description = "ARN of the IAM role for Glue"
  type        = string
}

variable "glue_script_location" {
  description = "S3 path to the Glue ETL script"
  type        = string
}

variable "glue_temp_dir" {
  description = "Temporary directory for Glue job"
  type        = string
}

variable "sagemaker_model_name" {
  description = "Name of the SageMaker model"
  type        = string
}

variable "sagemaker_role_arn" {
  description = "ARN of the IAM role for SageMaker"
  type        = string
}

variable "sagemaker_image_uri" {
  description = "URI of the Docker image for SageMaker model"
  type        = string
}

variable "sagemaker_model_data_url" {
  description = "S3 URL of the SageMaker model data"
  type        = string
}

variable "sagemaker_endpoint_config_name" {
  description = "Name of the SageMaker endpoint configuration"
  type        = string
}

variable "sagemaker_endpoint_name" {
  description = "Name of the SageMaker endpoint"
  type        = string
}