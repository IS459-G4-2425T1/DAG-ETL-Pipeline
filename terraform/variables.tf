// root/variables.tf

variable "aws_region" {
  description = "AWS region to deploy resources in"
  type        = string
  default     = "us-east-1"
}

variable "shared_bucket_name" {
  description = "Name of the shared S3 bucket"
  type        = string
}

variable "environment" {
  description = "Deployment environment (e.g., dev, staging, prod)"
  type        = string
}

variable "quicksight_user_name" {
  description = "QuickSight user name"
  type        = string
}

# variable "flow1_quicksight_data_set_arn" {
#   description = "ARN of the externally managed Flow 1 QuickSight Data Set"
#   type        = string
# }

# variable "flow2_quicksight_data_set_arn" {
#   description = "ARN of the externally managed Flow 2 QuickSight Data Set"
#   type        = string
# }

# variable "flow3_quicksight_data_set_arn" {
#   description = "ARN of the externally managed Flow 3 QuickSight Data Set"
#   type        = string
# }

# Flow 1 Variables
variable "flow1_raw_data_bucket_name" {
  description = "Name of the S3 bucket for Flow 1 raw data"
  type        = string
}

variable "flow1_glue_job_historic_name" {
  description = "Name of the Glue Historic job for Flow 1"
  type        = string
}

variable "flow1_glue_job_engineering_name" {
  description = "Name of the Glue Engineering job for Flow 1"
  type        = string
}

variable "flow1_glue_airline_historic_etl_script" {
  description = "S3 path to the Glue ETL script for Flow 1"
  type        = string
}

variable "flow1_glue_engineering_job_script" {
  description = "S3 path to the Engineering Job script"
  type        = string
}

variable "flow1_glue_temp_dir" {
  description = "Temporary directory for Glue job in Flow 1"
  type        = string
}

variable "flow1_glue_spark_logs_dir" {
  description = "Directory for Glue SPark Logs in Flow 1"
  type        = string
}

variable "flow1_sagemaker_model_name" {
  description = "The name of the SageMaker model for Flow 1"
  type        = string
}

variable "flow1_sagemaker_training_job_name" {
  description = "Name of the SageMaker training job for Flow 1"
  type        = string
}

variable "flow1_sagemaker_training_image" {
  description = "URI of the SageMaker training image for Flow 1 (use AWS-managed images)"
  type        = string
}

variable "flow1_sagemaker_model_data_url" {
  description = "S3 URI where the trained model artifacts are stored for Flow1."
  type        = string
}

variable "flow1_training_data_s3_uri" {
  description = "S3 URI for training data in Flow 1"
  type        = string
}

variable "flow1_sagemaker_output_path" {
  description = "S3 path for SageMaker output in Flow 1"
  type        = string
}

variable "flow1_quicksight_data_source_name" {
  description = "QuickSight Data Source name for Flow 1"
  type        = string
}

variable "flow1_quicksight_data_set_name" {
  description = "QuickSight Data Set name for Flow 1"
  type        = string
}

variable "flow1_quicksight_dashboard_name" {
  description = "QuickSight Dashboard name for Flow 1"
  type        = string
}

# Flow 2 Variables
variable "flow2_raw_api_data_bucket_name" {
  description = "Name of the S3 bucket for Flow 2 raw API data"
  type        = string
}

variable "flow2_lambda_function_zip" {
  description = "Lambda function zip file name for Flow 2"
  type        = string
}

variable "flow2_lambda_function_name" {
  description = "Lambda function name for Flow 2"
  type        = string
}

variable "flow2_lambda_handler" {
  description = "Lambda handler name for Flow 2"
  type        = string
}

variable "flow2_lambda_runtime" {
  description = "Lambda function runtime for Flow 2"
  type        = string
}

variable "flow2_event_rule_name" {
  description = "EventBridge rule name for Flow 2"
  type        = string
}

variable "flow2_schedule_expression" {
  description = "Schedule expression for Flow 2 (e.g., rate(5 minutes))"
  type        = string
}

variable "flow2_glue_database_name" {
  description = "Glue database name for Flow 2"
  type        = string
}

variable "flow2_glue_crawler_name" {
  description = "Glue crawler name for Flow 2"
  type        = string
}

variable "flow2_glue_crawler_schedule" {
  description = "Glue crawler schedule for Flow 2 (e.g., cron expression)"
  type        = string
}

variable "flow2_glue_job_name" {
  description = "Glue job name for Flow 2"
  type        = string
}

variable "flow2_glue_script_location" {
  description = "S3 path to the Glue ETL script for Flow 2"
  type        = string
}

variable "flow2_glue_temp_dir" {
  description = "Temporary directory for Glue job in Flow 2"
  type        = string
}

variable "flow2_athena_database_name" {
  description = "Athena database name for Flow 2"
  type        = string
}

variable "flow2_athena_query_results_bucket_name" {
  description = "S3 bucket for Athena query results for Flow 2"
  type        = string
}

variable "flow2_athena_workgroup_name" {
  description = "Athena workgroup name for Flow 2"
  type        = string
}

variable "flow2_quicksight_data_source_name" {
  description = "QuickSight Data Source name for Flow 2"
  type        = string
}

variable "flow2_quicksight_data_set_name" {
  description = "QuickSight Data Set name for Flow 2"
  type        = string
}

variable "flow2_quicksight_dashboard_name" {
  description = "QuickSight Dashboard name for Flow 2"
  type        = string
}

# Flow 3 Variables
variable "flow3_user_input_data_bucket_name" {
  description = "Name of the S3 bucket for Flow 3 user input data"
  type        = string
}

variable "flow3_api_name" {
  description = "API Gateway name for Flow 3"
  type        = string
}

variable "flow3_lambda_function_zip" {
  description = "Lambda function zip file name for Flow 3"
  type        = string
}

variable "flow3_lambda_function_name" {
  description = "Lambda function name for Flow 3"
  type        = string
}

variable "flow3_lambda_handler" {
  description = "Lambda handler name for Flow 3"
  type        = string
}

variable "flow3_lambda_runtime" {
  description = "Lambda runtime for Flow 3"
  type        = string
}

variable "flow3_trigger_lambda_zip" {
  description = "Trigger Lambda function zip file name for Flow 3"
  type        = string
}

variable "flow3_trigger_lambda_name" {
  description = "Trigger Lambda function name for Flow 3"
  type        = string
}

variable "flow3_trigger_lambda_handler" {
  description = "Trigger Lambda handler name for Flow 3"
  type        = string
}

variable "flow3_invoke_sagemaker_lambda_zip" {
  description = "Lambda invoking SageMaker zip file name for Flow 3"
  type        = string
}

variable "flow3_invoke_sagemaker_lambda_name" {
  description = "Lambda invoking SageMaker function name for Flow 3"
  type        = string
}

variable "flow3_invoke_sagemaker_lambda_handler" {
  description = "Lambda invoking SageMaker handler name for Flow 3"
  type        = string
}

variable "flow3_glue_job_name" {
  description = "Glue job name for Flow 3"
  type        = string
}

variable "flow3_glue_script_location" {
  description = "S3 path to the Glue ETL script for Flow 3"
  type        = string
}

variable "flow3_glue_temp_dir" {
  description = "Temporary directory for Glue job in Flow 3"
  type        = string
}

variable "flow3_sagemaker_model_name" {
  description = "SageMaker model name for Flow 3"
  type        = string
}

variable "flow3_sagemaker_image_uri" {
  description = "URI of the SageMaker image for Flow 3 (use AWS-managed images)"
  type        = string
}

variable "flow3_sagemaker_model_data_url" {
  description = "S3 URI where the trained model artifacts are stored for Flow 3."
  type        = string
}

variable "flow3_sagemaker_endpoint_config_name" {
  description = "SageMaker endpoint configuration name for Flow 3"
  type        = string
}

variable "flow3_sagemaker_endpoint_name" {
  description = "SageMaker endpoint name for Flow 3"
  type        = string
}

variable "flow3_quicksight_data_source_name" {
  description = "QuickSight Data Source name for Flow 3"
  type        = string
}

variable "flow3_quicksight_data_set_name" {
  description = "QuickSight Data Set name for Flow 3"
  type        = string
}

variable "flow3_quicksight_dashboard_name" {
  description = "QuickSight Dashboard name for Flow 3"
  type        = string
}