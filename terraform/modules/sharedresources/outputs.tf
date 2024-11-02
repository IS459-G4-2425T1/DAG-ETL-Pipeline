output "shared_bucket_arn" {
  description = "ARN of the shared S3 bucket"
  value       = aws_s3_bucket.shared_bucket.arn
}

output "lambda_role_arn" {
  description = "ARN of the shared Lambda execution role"
  value       = aws_iam_role.lambda_role.arn
}