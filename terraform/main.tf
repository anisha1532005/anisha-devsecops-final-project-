terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1"
}

# Secure S3 Deployment Bucket
resource "aws_s3_bucket" "secure_deployment" {
  bucket        = "anisas-secure-deployment-bucket"
  force_destroy = true
}

resource "aws_s3_bucket_ownership_controls" "owner" {
  bucket = aws_s3_bucket.secure_deployment.id
  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_public_access_block" "block" {
  bucket                  = aws_s3_bucket.secure_deployment.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

output "deployment_bucket_arn" {
  value = aws_s3_bucket.secure_deployment.arn
}