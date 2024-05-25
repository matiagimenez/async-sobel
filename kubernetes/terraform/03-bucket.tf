resource "google_storage_bucket" "bucket" {
  name          = var.bucket_name 
  location      = var.region 
  storage_class = "STANDARD"
  force_destroy = true
  
  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 1
    }
  }
}

resource "google_storage_default_object_access_control" "public_rule" {
  bucket = var.bucket_name
  role   = "READER"
  entity = "allUsers"
  
  # Depende de que el bucket este creado para aplicar la regla
  depends_on = [google_storage_bucket.bucket]
}
