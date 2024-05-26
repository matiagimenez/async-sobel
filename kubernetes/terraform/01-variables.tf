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
  default = "us-east4" # us-central1
}

variable "zone" {
  type    = string
  default = "us-east4-a" # us-central1-a
}

variable "bucket_name" {
  type    = string
  default = "sobel"
}

