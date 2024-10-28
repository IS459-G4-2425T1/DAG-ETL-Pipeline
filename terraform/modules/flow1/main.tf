// S3 Bucket for Raw Data
resource "aws_s3_bucket" "raw_data" {
  bucket = var.raw_data_bucket_name
}

resource "aws_s3_bucket_versioning" "raw_data" {
  bucket = aws_s3_bucket.raw_data.bucket
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "raw_data" {
  bucket = aws_s3_bucket.raw_data.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

// Glue ETL Job
resource "aws_glue_job" "historical_data_etl" {
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

// SageMaker Model (for inference)
resource "aws_sagemaker_model" "model" {
  name              = var.sagemaker_model_name
  execution_role_arn = var.sagemaker_role_arn  // Ensure this variable is declared

  primary_container {
    image          = var.sagemaker_training_image
    model_data_url = var.sagemaker_model_data_url  // S3 URI of your trained model artifact
    mode           = "SingleModel"
  }
}

// SageMaker Endpoint Configuration
resource "aws_sagemaker_endpoint_configuration" "model_endpoint_config" {
  name = "${var.sagemaker_model_name}-endpoint-config"

  production_variants {
    variant_name          = "AllTraffic"
    model_name            = aws_sagemaker_model.model.name
    initial_instance_count = 1
    instance_type         = "ml.m5.large"
  }
}

// SageMaker Endpoint (for inference)
resource "aws_sagemaker_endpoint" "model_endpoint" {
  name = "${var.sagemaker_model_name}-endpoint"
  endpoint_config_name = aws_sagemaker_endpoint_configuration.model_endpoint_config.name
}
