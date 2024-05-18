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

# Crea una red 
resource "google_compute_network" "workers_net" {
  name                            = "workers_net"
  routing_mode                    = "REGIONAL"
  auto_create_subnetworks         = false
  mtu                             = 1460
  delete_default_routes_on_create = false

  depends_on = [google_project_service.compute]
}

resource "google_compute_subnetwork" "workers_subnet" {
  name                     = "workers-subnet"
  ip_cidr_range            = "10.0.0.0/18"
  region                   = var.region
  network                  = google_compute_network.workers_net.id
  private_ip_google_access = true

}

resource "google_compute_router" "workers_router" {
  name    = "workers_router"
  region  = var.region
  network = google_compute_network.workers_net.id
}

# Crea un recurso NAT que traducirá las direcciones IP de origen de la subred privada de kubernetes. 
resource "google_compute_router_nat" "router_nat" {
  name   = "router_nat"
  router = google_compute_router.workers_net.name
  region = var.region

  source_subnetwork_ip_ranges_to_nat = "LIST_OF_SUBNETWORKS"
  nat_ip_allocate_option             = "MANUAL_ONLY"

  subnetwork {
    name                    = google_compute_subnetwork.workers_subnet.id
    source_ip_ranges_to_nat = ["ALL_IP_RANGES"]
  }

  nat_ips = [google_compute_address.router_nat.self_link]
}

# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_address
# Crea una IP pública para ser utilizada en el NAT
resource "google_compute_address" "nat_address" {
  name         = "nat_address"
  address_type = "EXTERNAL"
  network_tier = "PREMIUM"

  depends_on = [google_project_service.compute]
}