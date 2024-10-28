// modules/flow2/outputs.tf

output "raw_api_data_bucket_arn" {
  description = "ARN of the raw API data S3 bucket"
  value       = aws_s3_bucket.external_api_raw_data.arn
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.external_api_retrieval.function_name
}

output "glue_job_name" {
  description = "Name of the Glue ETL job"
  value       = aws_glue_job.external_api_etl.name
}
