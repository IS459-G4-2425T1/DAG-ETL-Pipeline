// root/main.tf

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

module "shared_resources" {
  source = "./modules/sharedresources"

  shared_bucket_name = var.shared_bucket_name
  environment        = var.environment
}

/////////////////////
// IAM Role Definitions
/////////////////////

// Flow 1 Glue Role
resource "aws_iam_role" "flow1_glue_role" {
  name = "flow1-glue-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "glue.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "flow1_glue_policy" {
  role       = aws_iam_role.flow1_glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

// Flow 1 SageMaker Role
resource "aws_iam_role" "flow1_sagemaker_role" {
  name = "flow1-sagemaker-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "sagemaker.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "flow1_sagemaker_policy" {
  role       = aws_iam_role.flow1_sagemaker_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}

resource "aws_iam_role_policy_attachment" "flow1_sagemaker_ecr_access" {
  role       = aws_iam_role.flow1_sagemaker_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

// Flow 2 Glue Role
resource "aws_iam_role" "flow2_glue_role" {
  name = "flow2-glue-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "glue.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "flow2_glue_policy" {
  role       = aws_iam_role.flow2_glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

// Flow 3 Glue Role
resource "aws_iam_role" "flow3_glue_role" {
  name = "flow3-glue-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "glue.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "flow3_glue_policy" {
  role       = aws_iam_role.flow3_glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

// Flow 3 SageMaker Role
resource "aws_iam_role" "flow3_sagemaker_role" {
  name = "flow3-sagemaker-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "sagemaker.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "flow3_sagemaker_policy" {
  role       = aws_iam_role.flow3_sagemaker_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}

resource "aws_iam_role_policy_attachment" "flow3_sagemaker_ecr_access" {
  role       = aws_iam_role.flow3_sagemaker_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

/////////////////////
// Modules Configuration
/////////////////////

module "flow1" {
  source = "./modules/flow1"

  shared_bucket_arn       = module.shared_resources.shared_bucket_arn
  lambda_role_arn         = module.shared_resources.lambda_role_arn

  raw_data_bucket_name       = var.flow1_raw_data_bucket_name
  glue_job_historic_name              = var.flow1_glue_job_historic_name
  glue_job_engineering_name = var.flow1_glue_job_engineering_name
  glue_role_arn              = aws_iam_role.flow1_glue_role.arn
  glue_airline_historic_etl_script       = var.flow1_glue_airline_historic_etl_script
  glue_spark_logs_dir = var.flow1_glue_spark_logs_dir
  glue_engineering_job_script = var.flow1_glue_engineering_job_script
  glue_temp_dir              = var.flow1_glue_temp_dir
  sagemaker_model_name       = var.flow1_sagemaker_model_name
  sagemaker_role_arn         = aws_iam_role.flow1_sagemaker_role.arn
  sagemaker_training_image   = var.flow1_sagemaker_training_image
  sagemaker_model_data_url   = var.flow1_sagemaker_model_data_url
  training_data_s3_uri       = var.flow1_training_data_s3_uri
  sagemaker_output_path      = var.flow1_sagemaker_output_path
}

module "flow2" {
  source = "./modules/flow2"

  shared_bucket_arn                  = module.shared_resources.shared_bucket_arn
  lambda_role_arn                    = module.shared_resources.lambda_role_arn

  raw_api_data_bucket_name           = var.flow2_raw_api_data_bucket_name
  lambda_function_zip                = var.flow2_lambda_function_zip
  lambda_function_name               = var.flow2_lambda_function_name
  lambda_handler                     = var.flow2_lambda_handler
  lambda_runtime                     = var.flow2_lambda_runtime
  event_rule_name                    = var.flow2_event_rule_name
  schedule_expression                = var.flow2_schedule_expression
  glue_database_name                 = var.flow2_glue_database_name
  glue_crawler_name                  = var.flow2_glue_crawler_name
  glue_crawler_schedule              = var.flow2_glue_crawler_schedule
  glue_job_name                      = var.flow2_glue_job_name
  glue_role_arn                      = aws_iam_role.flow2_glue_role.arn
  glue_script_location               = var.flow2_glue_script_location
  glue_temp_dir                      = var.flow2_glue_temp_dir
  athena_database_name               = var.flow2_athena_database_name
  athena_query_results_bucket_name   = var.flow2_athena_query_results_bucket_name
  athena_workgroup_name              = var.flow2_athena_workgroup_name
}

module "flow3" {
  source = "./modules/flow3"

  shared_bucket_arn                    = module.shared_resources.shared_bucket_arn
  lambda_role_arn                      = module.shared_resources.lambda_role_arn

  user_input_data_bucket_name          = var.flow3_user_input_data_bucket_name
  api_name                             = var.flow3_api_name
  lambda_function_zip                  = var.flow3_lambda_function_zip
  lambda_function_name                 = var.flow3_lambda_function_name
  lambda_handler                       = var.flow3_lambda_handler
  lambda_runtime                       = var.flow3_lambda_runtime
  trigger_lambda_zip                   = var.flow3_trigger_lambda_zip
  trigger_lambda_name                  = var.flow3_trigger_lambda_name
  trigger_lambda_handler               = var.flow3_trigger_lambda_handler
  invoke_sagemaker_lambda_zip          = var.flow3_invoke_sagemaker_lambda_zip
  invoke_sagemaker_lambda_name         = var.flow3_invoke_sagemaker_lambda_name
  invoke_sagemaker_lambda_handler      = var.flow3_invoke_sagemaker_lambda_handler
  glue_job_name                        = var.flow3_glue_job_name
  glue_role_arn                        = aws_iam_role.flow3_glue_role.arn
  glue_script_location                 = var.flow3_glue_script_location
  glue_temp_dir                        = var.flow3_glue_temp_dir
  sagemaker_model_name                 = var.flow3_sagemaker_model_name
  sagemaker_role_arn                   = aws_iam_role.flow3_sagemaker_role.arn
  sagemaker_image_uri                  = var.flow3_sagemaker_image_uri
  sagemaker_model_data_url             = var.flow3_sagemaker_model_data_url
  sagemaker_endpoint_config_name        = var.flow3_sagemaker_endpoint_config_name
  sagemaker_endpoint_name               = var.flow3_sagemaker_endpoint_name
}

/////////////////////
// Consolidated QuickSight CloudFormation Stack
/////////////////////

resource "aws_cloudformation_stack" "quicksight_consolidated" {
  name          = "quicksight-consolidated-stack"
  template_body = file("${path.root}/quicksight-template.yaml")

  parameters = {
    QuickSightUserName = var.quicksight_user_name

    # Flow 1 QuickSight Parameters
    Flow1DataSourceName = var.flow1_quicksight_data_source_name
    Flow1DataSetName    = var.flow1_quicksight_data_set_name
    Flow1DashboardName  = var.flow1_quicksight_dashboard_name
    # Flow1TemplateArn    = var.flow1_quicksight_data_set_arn

    # Flow 2 QuickSight Parameters
    Flow2DataSourceName = var.flow2_quicksight_data_source_name
    Flow2DataSetName    = var.flow2_quicksight_data_set_name
    Flow2DashboardName  = var.flow2_quicksight_dashboard_name
    # Flow2TemplateArn    = var.flow2_quicksight_data_set_arn

    # Flow 3 QuickSight Parameters
    Flow3DataSourceName = var.flow3_quicksight_data_source_name
    Flow3DataSetName    = var.flow3_quicksight_data_set_name
    Flow3DashboardName  = var.flow3_quicksight_dashboard_name
    # Flow3TemplateArn    = var.flow3_quicksight_data_set_arn
  }

  capabilities = ["CAPABILITY_NAMED_IAM"]

  depends_on = [
    module.flow1,
    module.flow2,
    module.flow3
  ]
}
