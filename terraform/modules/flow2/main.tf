// S3 Bucket for Raw API Data
resource "aws_s3_bucket" "external_api_raw_data" {
  bucket = var.raw_api_data_bucket_name
}

resource "aws_s3_bucket_versioning" "external_api_raw_data" {
  bucket = aws_s3_bucket.external_api_raw_data.bucket
  versioning_configuration {
    status = "Enabled"
  }
}

// Lambda Function for Active_Carriers
resource "aws_lambda_function" "selenium_scraper" {
  filename         = var.lambda_function_zip
  function_name    = var.lambda_function_name
  role             = var.lambda_role_arn
  handler          = var.lambda_handler
  runtime          = var.lambda_runtime
  timeout          = 30
  memory_size      = 128
  publish          = true

  # source_code_hash = filebase64sha256(var.lambda_function_zip)
  # To add after source code is created
}

// EventBridge Scheduler to retrieve Active
resource "aws_scheduler_schedule" "get_active_carriers" {
  name                       = "get-active-carriers"  # Reuse the existing name
  description                = "Schedule to trigger the selenium scraper Lambda function at midnight on the first of each month"
  schedule_expression        = "cron(0 0 1 * ? *)"
  schedule_expression_timezone = "Asia/Singapore"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn       = aws_lambda_function.selenium_scraper.arn  # Reference the Lambda function's ARN dynamically
    role_arn  = aws_iam_role.lambda_selenium_scraper_role.arn  # Reference the IAM role dynamically

    retry_policy {
      maximum_event_age_in_seconds = 86400
      maximum_retry_attempts       = 185
    }
  }
}

# IAM Role for EventBridge Scheduler to invoke Lambda
resource "aws_iam_role" "lambda_selenium_scraper_role" {
  name = "lambda-selenium-scraper-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "scheduler.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

// Managed Policy Attachments
resource "aws_iam_role_policy_attachment" "eventbridge_full_access" {
  role       = aws_iam_role.lambda_selenium_scraper_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEventBridgeFullAccess"
}

resource "aws_iam_role_policy_attachment" "scheduler_full_access" {
  role       = aws_iam_role.lambda_selenium_scraper_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEventBridgeSchedulerFullAccess"
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_selenium_scraper_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

// Custom S3 Policy for Access to S3 Bucket
resource "aws_iam_policy" "s3_carriers_data_access" {
  name   = "S3CarriersDataAccess"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::active-carriers-data/*",
          "arn:aws:s3:::active-carriers-data"
        ]
      }
    ]
  })
}

// Attach Custom S3 Policy to Role
resource "aws_iam_role_policy_attachment" "s3_access_policy_attachment" {
  role       = aws_iam_role.lambda_selenium_scraper_role.name
  policy_arn = aws_iam_policy.s3_carriers_data_access.arn
}

// AWS Glue Crawler
resource "aws_glue_catalog_database" "external_api_database" {
  name = var.glue_database_name
}

resource "aws_glue_crawler" "external_api_crawler" {
  name          = var.glue_crawler_name
  role          = var.glue_role_arn
  database_name = aws_glue_catalog_database.external_api_database.name

  s3_target {
    path = "s3://${aws_s3_bucket.external_api_raw_data.bucket}/"
  }

  schedule = var.glue_crawler_schedule
}

// AWS Glue ETL Job
resource "aws_glue_job" "external_api_etl" {
  name     = var.glue_job_name
  role_arn = var.glue_role_arn

  command {
    name            = "glueetl"
    script_location = var.glue_script_location
    python_version  = "3"
  }

  default_arguments = {
    "--TempDir" = var.glue_temp_dir
  }

  glue_version      = "2.0"
  number_of_workers = 2
  worker_type       = "G.1X"
}

// Athena Setup
resource "aws_athena_database" "external_api_athena_db" {
  name = var.athena_database_name
}

resource "aws_s3_bucket" "athena_query_results" {
  bucket = var.athena_query_results_bucket_name
}

resource "aws_athena_workgroup" "primary" {
  name = var.athena_workgroup_name

  configuration {
    result_configuration {
      output_location = "s3://${aws_s3_bucket.athena_query_results.bucket}/"
    }
  }
}
