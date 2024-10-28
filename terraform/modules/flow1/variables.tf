// modules/flow1/variables.tf

// Import shared resources
variable "shared_bucket_arn" {
  type        = string
  description = "ARN of the shared S3 bucket from shared module"
}

variable "lambda_role_arn" {
  type        = string
  description = "ARN of the shared Lambda execution role from shared module"
}

variable "raw_data_bucket_name" {
  description = "Name of the S3 bucket for raw data"
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
  description = "The name of the SageMaker model"
  type        = string
}

variable "sagemaker_role_arn" {
  description = "The ARN of the IAM role for SageMaker"
  type        = string
}

variable "sagemaker_training_image" {
  description = "The URI of the Docker image to use for SageMaker training"
  type        = string
}

variable "sagemaker_model_data_url" {
  description = "The S3 URI where the trained model artifacts are stored"
  type        = string
}

variable "training_data_s3_uri" {
  description = "S3 URI for training data"
  type        = string
}

variable "sagemaker_output_path" {
  description = "S3 path for SageMaker output"
  type        = string
}