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

// Airline Historic ETL Job
resource "aws_glue_job" "airline_historic_etl" {
  name     = var.glue_job_historic_name
  role_arn = var.glue_role_arn

  command {
    name            = "glueetl"
    script_location = var.glue_airline_historic_etl_script
    python_version  = "3"
  }

  default_arguments = {
    "--TempDir"                       = var.glue_temp_dir
    "--enable-auto-scaling"           = "true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-glue-datacatalog"       = "true"
    "--enable-job-insights"           = "true"
    "--enable-metrics"                = "true"
    "--enable-observability-metrics"  = "true"
    "--job-bookmark-option"           = "job-bookmark-disable"
    "--job-language"                  = "python"
    "--spark-event-logs-path"         = var.glue_spark_logs_dir
  }

  glue_version      = "4.0"
  number_of_workers = 3
  worker_type       = "G.1X"
  max_retries       = 0
  execution_class   = "STANDARD"
  timeout           = 120

  execution_property {
    max_concurrent_runs = 1
  }
}

// Historic Airline Engineering Job
resource "aws_glue_job" "engineering_job" {
  name     = var.glue_job_engineering_name
  role_arn = var.glue_role_arn

  command {
    name            = "glueetl"
    script_location = var.glue_engineering_job_script
    python_version  = "3"
  }

  default_arguments = {
    "--TempDir"                       = var.glue_temp_dir
    "--enable-auto-scaling"           = "true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-glue-datacatalog"       = "true"
    "--enable-job-insights"           = "true"
    "--enable-metrics"                = "true"
    "--enable-observability-metrics"  = "true"
    "--job-bookmark-option"           = "job-bookmark-disable"
    "--job-language"                  = "python"
    "--spark-event-logs-path"         = var.glue_spark_logs_dir
  }

  glue_version      = "4.0"
  number_of_workers = 3
  worker_type       = "G.1X"
  max_retries       = 0
  execution_class   = "STANDARD"
  timeout           = 120

  execution_property {
    max_concurrent_runs = 1
  }
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
