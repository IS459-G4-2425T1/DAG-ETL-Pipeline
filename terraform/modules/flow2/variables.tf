// modules/flow2/variables.tf

// Import shared resources
variable "shared_bucket_arn" {
  type        = string
  description = "ARN of the shared S3 bucket from shared module"
}

variable "lambda_role_arn" {
  type        = string
  description = "ARN of the shared Lambda execution role from shared module"
}

variable "raw_api_data_bucket_name" {
  description = "Name of the S3 bucket for raw API data"
  type        = string
}

variable "lambda_function_zip" {
  description = "Path to the zipped Lambda function code"
  type        = string
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "lambda_handler" {
  description = "Handler of the Lambda function"
  type        = string
}

variable "lambda_runtime" {
  description = "Runtime for the Lambda function"
  type        = string
  default     = "python3.8"
}

variable "event_rule_name" {
  description = "Name of the EventBridge rule"
  type        = string
}

variable "schedule_expression" {
  description = "Schedule expression for the EventBridge rule"
  type        = string
}

variable "glue_database_name" {
  description = "Name of the Glue catalog database"
  type        = string
}

variable "glue_crawler_name" {
  description = "Name of the Glue crawler"
  type        = string
}

variable "glue_crawler_schedule" {
  description = "Schedule for the Glue crawler"
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

variable "athena_database_name" {
  description = "Name of the Athena database"
  type        = string
}

variable "athena_query_results_bucket_name" {
  description = "Name of the S3 bucket for Athena query results"
  type        = string
}

variable "athena_workgroup_name" {
  description = "Name of the Athena workgroup"
  type        = string
}