// modules/sharedresources/main.tf

// S3 Buckets for Shared Use
resource "aws_s3_bucket" "shared_bucket" {
  bucket = var.shared_bucket_name
}

resource "aws_s3_bucket_versioning" "shared_bucket" {
  bucket = aws_s3_bucket.shared_bucket.bucket
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "shared_bucket" {
  bucket = aws_s3_bucket.shared_bucket.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

// IAM Roles and Policies for Shared Use
// Example: Shared Lambda Execution Role
resource "aws_iam_role" "lambda_role" {
  name = "lambda_execution_role"

  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}

data "aws_iam_policy_document" "lambda_assume_role_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}