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
  default = "us-east1"
}

variable "zone" {
  type    = string
  default = "us-east1-b"
}


variable "metadata_startup_script" {
  type    = string
  default = "./scripts/init.sh"
}

# Instance Template
variable "prefix" {
  type    = string
  default = "sobel-worker-"
}

variable "desc" {
  type    = string
  default = "This template is used to create sobel worker instances"
}

variable "tags" {
  type    = string
  default = "worker"
}

variable "desc_inst" {
  type    = string
  default = "Sobel worker instance"
}

variable "machine_type" {
  type    = string
  default = "e2-highcpu-4"
}

# This is the family tag used when building the Golden Image with Packer.
variable "source_image" {
  type    = string
  default = "async-sobel-docker-1715903966"
}

variable "network" {
  type    = string
  default = "default"
}

# Managed Instace Group
variable "rmig_name" {
  default = "sobel-rmig"
  type    = string
}

variable "base_instance_name" {
  type    = string
  default = "custom-sobel"
}

# Healthcheck
variable "hc_name" {
  type    = string
  default = "sobel-healthcheck"
}

variable "hc_port" {
  type    = string
  default = "80"
}

# Backend
variable "be_name" {
  type    = string
  default = "http-backend"
}

variable "be_protocol" {
  type    = string
  default = "HTTP"
}

variable "be_port_name" {
  type    = string
  default = "http"
}

variable "be_timeout" {
  type    = string
  default = "10"
}

variable "be_session_affinity" {
  type    = string
  default = "NONE"
}

# RMIG Autoscaler
variable "rmig_as_name" {
  type    = string
  default = "rmig-as"
}

variable "min_replicas" {
  type    = string
  default = 6
}

variable "max_replicas" {
  type    = string
  default = 16
}

# Global Forwarding Rule
variable "gfr_name" {
  type    = string
  default = "website-forwarding-rule"
}

variable "gfr_portrange" {
  type    = string
  default = "80"
}

variable "thp_name" {
  type    = string
  default = "http-proxy"
}

variable "urlmap_name" {
  type    = string
  default = "sobel-load-balancer"
}
