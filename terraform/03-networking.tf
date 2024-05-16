resource "google_compute_firewall" "allow_http" {
  name          = "allow-http"
  network       = "default"
  target_tags   = ["allow-http"]
  source_ranges = ["0.0.0.0/0"]

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }
}
