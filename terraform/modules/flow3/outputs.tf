// modules/flow3/outputs.tf

output "user_input_data_bucket_arn" {
  description = "ARN of the user input data S3 bucket"
  value       = aws_s3_bucket.user_input_data.arn
}

output "api_gateway_rest_api_id" {
  description = "ID of the API Gateway REST API"
  value       = aws_api_gateway_rest_api.app_api.id
}

output "sagemaker_endpoint_name" {
  description = "Name of the SageMaker endpoint"
  value       = aws_sagemaker_endpoint.endpoint.name
}
