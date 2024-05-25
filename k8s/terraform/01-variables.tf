variable "credentials" {
  type    = string
  default = "credentials.json"
}

variable "project" {
  type    = string
  default = "braided-complex-416718"
}

variable "region" {
  type    = string
  default = "us-central1" # us-east1
}

variable "zone" {
  type    = string
  default = "us-central1-a" # us-east1-b
}

variable "bucket_name" {
  type = string
  default = "sobel"
}

