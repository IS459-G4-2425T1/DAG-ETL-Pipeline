// root/outputs.tf

output "shared_bucket_arn" {
  description = "ARN of the shared S3 bucket"
  value       = module.shared_resources.shared_bucket_arn
}

output "flow1_raw_data_bucket_arn" {
  description = "ARN of the Flow 1 raw data S3 bucket"
  value       = module.flow1.raw_data_bucket_arn
}

output "flow2_raw_api_data_bucket_arn" {
  description = "ARN of the Flow 2 raw API data S3 bucket"
  value       = module.flow2.raw_api_data_bucket_arn
}

output "flow3_user_input_data_bucket_arn" {
  description = "ARN of the Flow 3 user input data S3 bucket"
  value       = module.flow3.user_input_data_bucket_arn
}

# Optional: Output IAM Role ARNs
output "flow1_glue_role_arn" {
  description = "ARN of Flow 1 Glue IAM Role"
  value       = aws_iam_role.flow1_glue_role.arn
}

output "flow1_sagemaker_role_arn" {
  description = "ARN of Flow 1 SageMaker IAM Role"
  value       = aws_iam_role.flow1_sagemaker_role.arn
}

output "flow2_glue_role_arn" {
  description = "ARN of Flow 2 Glue IAM Role"
  value       = aws_iam_role.flow2_glue_role.arn
}

output "flow3_glue_role_arn" {
  description = "ARN of Flow 3 Glue IAM Role"
  value       = aws_iam_role.flow3_glue_role.arn
}

output "flow3_sagemaker_role_arn" {
  description = "ARN of Flow 3 SageMaker IAM Role"
  value       = aws_iam_role.flow3_sagemaker_role.arn
}
