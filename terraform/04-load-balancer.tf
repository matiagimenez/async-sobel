# Configuramos el health check http que verifica el estado de los workers pegandole a su ruta de status
resource "google_compute_http_health_check" "default" {
  name               = var.hc_name
  request_path       = "/api/sobel"
  port               = var.hc_port
  check_interval_sec = 1
  timeout_sec        = 1
}

resource "google_compute_health_check" "default" {
  name               = var.hc_name
  check_interval_sec = 1
  timeout_sec        = 1

  tcp_health_check {
    port = var.hc_port
  }
}

# Creamos un servicio de backend al cual el load balancer podrá redirigir todo el tráfico.
# Este servicio de backend utiliza el grupo de instancias que se declara abajo
resource "google_compute_backend_service" "rbs" {
  name             = var.be_name
  port_name        = var.be_port_name
  protocol         = var.be_protocol
  timeout_sec      = var.be_timeout
  session_affinity = var.be_session_affinity

  backend {
    group = google_compute_region_instance_group_manager.rmig.instance_group
  }

  health_checks = ["${google_compute_http_health_check.default.self_link}"]
}

# Creamos un grupo de instancias administrado de forma regional. Es decir, existirán instancias en diferentes zonas dentro de la región especificada.
# Podría realizarse lo mismo de forma zonal y global.
resource "google_compute_region_instance_group_manager" "rmig" {
  name               = var.rmig_name
  base_instance_name = var.base_instance_name
  region             = var.region
  target_size        = var.min_replicas

  named_port {
    name = "http"
    port = 80
  }

  auto_healing_policies {
    health_check      = google_compute_http_health_check.default.self_link
    initial_delay_sec = 300
  }

  version {
    name              = "deployed-version"
    instance_template = google_compute_instance_template.sobel-worker-template.self_link
  }

}

# Configuramos el enrutamiento de las peticiones que llegan al load balancer.
resource "google_compute_global_forwarding_rule" "gfr" {
  name       = var.gfr_name
  target     = google_compute_target_http_proxy.thp.self_link
  port_range = var.gfr_portrange # Define el rango de puertos en los que la forwarding rule escuchará el tráfico entrante.
}
resource "google_compute_target_http_proxy" "thp" {
  name    = var.thp_name
  url_map = google_compute_url_map.urlmap.self_link
}
resource "google_compute_url_map" "urlmap" {
  name            = var.urlmap_name
  default_service = google_compute_backend_service.rbs.self_link
}


