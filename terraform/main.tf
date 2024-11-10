data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "sagemaker_model_bucket" {
  bucket = "cascade-sagemaker-model-bucket"
}

resource "aws_s3_object" "model_artifact" {
  bucket = aws_s3_bucket.sagemaker_model_bucket.id
  key    = "models/xgboost/model.tar.gz"
  source = "./model.tar.gz"
}


resource "aws_iam_role" "sagemaker_execution_role" {
  name = "sagemaker-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "sagemaker.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_policy" "sagemaker_policy" {
  name        = "sagemaker-policy"
  description = "Policy for SageMaker to access S3 and CloudWatch"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "${aws_s3_bucket.sagemaker_model_bucket.arn}/*"
      },
      {
        Effect   = "Allow"
        Action   = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect   = "Allow"
        Action   = [
          "cloudwatch:PutMetricData"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "sagemaker_attach_policy" {
  role       = aws_iam_role.sagemaker_execution_role.name
  policy_arn = aws_iam_policy.sagemaker_policy.arn
}

resource "aws_sagemaker_model" "xgboost_model" {
  name                = "xgboost-model"
  execution_role_arn  = aws_iam_role.sagemaker_execution_role.arn

  primary_container {
    image          = "683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost:1.7-1"
    model_data_url = "s3://${aws_s3_object.model_artifact.bucket}/${aws_s3_object.model_artifact.key}"
  }
}

resource "aws_sagemaker_endpoint_configuration" "xgboost_endpoint_config" {
  name = "xgboost-endpoint-config"

  production_variants {
    variant_name           = "AllTraffic"
    model_name             = aws_sagemaker_model.xgboost_model.name
    initial_instance_count = 1
    instance_type          = "ml.m5.large"
    initial_variant_weight = 1
  }
}

resource "aws_sagemaker_endpoint" "xgboost_endpoint" {
  name = "xgboost-iris-endpoint"
  endpoint_config_name = aws_sagemaker_endpoint_configuration.xgboost_endpoint_config.name
}


resource "aws_sfn_state_machine" "datapipeline1" {
  name     = "Datapipeline1-tf"
  role_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/service-role/StepFunctions-Datapipeline2-role-se2vhksnd"
  type     = "STANDARD"
  publish  = false
  
  definition = templatefile("${path.module}/stepfunction_pipeline1.json", {})

    logging_configuration {
        include_execution_data = false
        level                  = "OFF"
    }

    tracing_configuration {
        enabled = false
        }
}

resource "aws_sfn_state_machine" "datapipeline2" {
  name     = "Datapipeline2-tf"
  role_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/service-role/StepFunctions-Datapipeline2-role-se2vhksnd"
  type     = "STANDARD"
  publish  = false
  
  definition = templatefile("${path.module}/stepfunction_pipeline2.json", {})

    logging_configuration {
        include_execution_data = false
        level                  = "OFF"
    }

    tracing_configuration {
        enabled = false
        }
}
