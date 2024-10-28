// modules/sharedresources/variables.tf

variable "shared_bucket_name" {
  description = "Name of the shared S3 bucket"
  type        = string
}

variable "environment" {
  description = "Deployment environment (e.g., dev, staging, prod)"
  type        = string
}