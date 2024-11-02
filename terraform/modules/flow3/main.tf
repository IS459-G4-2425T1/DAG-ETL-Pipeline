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

  # source_code_hash = filebase64sha256(var.lambda_function_zip)
  # To add after source code is created
}


// EventBridge Rule to Schedule Lambda
resource "aws_cloudwatch_event_rule" "daily_trigger" {
  name                = "DailyTrigger"
  description         = "triggers at 8am"
  event_bus_name      = "default"
  state               = "DISABLED"

  schedule_expression = "cron(0 8 * * ? *)"
}

resource "aws_cloudwatch_event_target" "daily_lambda_target" {
  rule      = aws_cloudwatch_event_rule.daily_trigger.name
  target_id = "LambdaFunctionTarget"
  arn       = aws_lambda_function.external_api_retrieval.arn
}

resource "aws_lambda_permission" "allow_eventbridge_daily" {
  statement_id  = "AllowExecutionFromEventBridge_DailyTrigger"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.external_api_retrieval.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_trigger.arn
}


// S3 Bucket for User Input Data
resource "aws_s3_bucket" "user_input_data" {
  bucket = var.user_input_data_bucket_name
}

resource "aws_s3_bucket_versioning" "user_input_data" {
  bucket = aws_s3_bucket.user_input_data.bucket
  versioning_configuration {
    status = "Enabled"
  }
}

// API Gateway Setup
resource "aws_api_gateway_rest_api" "app_api" {
  name = var.api_name
}

resource "aws_api_gateway_resource" "input_resource" {
  rest_api_id = aws_api_gateway_rest_api.app_api.id
  parent_id   = aws_api_gateway_rest_api.app_api.root_resource_id
  path_part   = "input"
}

resource "aws_api_gateway_method" "post_method" {
  rest_api_id   = aws_api_gateway_rest_api.app_api.id
  resource_id   = aws_api_gateway_resource.input_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_lambda_function" "user_input_handler" {
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
      S3_BUCKET = aws_s3_bucket.user_input_data.bucket
    }
  }

  # source_code_hash = filebase64sha256(var.lambda_function_zip)
  # To add after source code is created
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.app_api.id
  resource_id             = aws_api_gateway_resource.input_resource.id
  http_method             = aws_api_gateway_method.post_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.user_input_handler.invoke_arn
}

resource "aws_lambda_permission" "allow_api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.user_input_handler.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.app_api.execution_arn}/*/*"
}

// AWS Glue ETL Job
resource "aws_glue_job" "user_input_etl" {
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
  number_of_workers = 5
  worker_type       = "G.1X"
}

// Lambda Function to Trigger Glue Job
resource "aws_lambda_function" "trigger_user_input_etl" {
  filename         = var.trigger_lambda_zip
  function_name    = var.trigger_lambda_name
  role             = var.lambda_role_arn
  handler          = var.trigger_lambda_handler
  runtime          = var.lambda_runtime
  timeout          = 30
  memory_size      = 128
  publish          = true

  environment {
    variables = {
      GLUE_JOB_NAME = aws_glue_job.user_input_etl.name
    }
  }

  # source_code_hash = filebase64sha256(var.trigger_lambda_zip)
  # To add after source code is created
}

resource "aws_s3_bucket_notification" "user_input_notification" {
  bucket = aws_s3_bucket.user_input_data.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.trigger_user_input_etl.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_s3_event]
}

resource "aws_lambda_permission" "allow_s3_event" {
  statement_id  = "AllowS3Event"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.trigger_user_input_etl.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.user_input_data.arn
}

// Lambda Function to Invoke SageMaker Endpoint
resource "aws_lambda_function" "invoke_sagemaker_endpoint" {
  filename         = var.invoke_sagemaker_lambda_zip
  function_name    = var.invoke_sagemaker_lambda_name
  role             = var.lambda_role_arn
  handler          = var.invoke_sagemaker_lambda_handler
  runtime          = var.lambda_runtime
  timeout          = 60
  memory_size      = 256
  publish          = true

  environment {
    variables = {
      ENDPOINT_NAME = aws_sagemaker_endpoint.endpoint.name
    }
  }

  # source_code_hash = filebase64sha256(var.invoke_sagemaker_lambda_zip)
  # To add after source code is created
}

// SageMaker Endpoint
resource "aws_sagemaker_model" "deployed_model" {
  name              = var.sagemaker_model_name
  execution_role_arn = var.sagemaker_role_arn

  primary_container {
    image          = var.sagemaker_image_uri
    model_data_url = var.sagemaker_model_data_url
  }
}

resource "aws_sagemaker_endpoint_configuration" "endpoint_config" {
  name = var.sagemaker_endpoint_config_name

  production_variants {
    variant_name           = "AllTraffic"
    model_name             = aws_sagemaker_model.deployed_model.name
    initial_instance_count = 1
    instance_type          = "ml.m5.large"
  }
}

resource "aws_sagemaker_endpoint" "endpoint" {
  name                 = var.sagemaker_endpoint_name
  endpoint_config_name = aws_sagemaker_endpoint_configuration.endpoint_config.name
}