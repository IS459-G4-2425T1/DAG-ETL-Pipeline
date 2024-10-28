// modules/flow2/main.tf

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

// Lambda Function to Retrieve External API Data
resource "aws_lambda_function" "external_api_retrieval" {
  filename         = var.lambda_function_zip
  function_name    = var.lambda_function_name
  role             = var.lambda_role_arn
  handler          = var.lambda_handler
  runtime          = var.lambda_runtime
  timeout          = 30
  memory_size      = 128
  publish          = true

  environment {
    variables = {
      S3_BUCKET = aws_s3_bucket.external_api_raw_data.bucket
    }
  }

  # source_code_hash = filebase64sha256(var.lambda_function_zip)
  # To add after source code is created
}

// EventBridge Rule to Schedule Lambda
resource "aws_cloudwatch_event_rule" "lambda_schedule" {
  name                = var.event_rule_name
  schedule_expression = var.schedule_expression
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.lambda_schedule.name
  target_id = "LambdaFunctionTarget"
  arn       = aws_lambda_function.external_api_retrieval.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.external_api_retrieval.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.lambda_schedule.arn
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
