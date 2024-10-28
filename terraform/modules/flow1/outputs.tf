// modules/flow1/outputs.tf

output "raw_data_bucket_arn" {
  description = "ARN of the raw data S3 bucket"
  value       = aws_s3_bucket.raw_data.arn
}

output "glue_job_name" {
  description = "Name of the Glue ETL job"
  value       = aws_glue_job.historical_data_etl.name
}