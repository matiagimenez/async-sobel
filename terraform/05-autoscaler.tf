# Definimos un autoscaler regional para un grupo de instancias administrado (RMIG). 
# El autoscaler ajustará automáticamente el tamaño del grupo de instancias basado en la utilización de la CPU, 
# para garantizar un rendimiento óptimo de la aplicación.
resource "google_compute_region_autoscaler" "cras" {

  name   = "autoscaler"
  region = var.region
  target = google_compute_region_instance_group_manager.rmig.self_link

  autoscaling_policy {
    max_replicas    = var.max_replicas
    min_replicas    = var.min_replicas
    cooldown_period = 30

    cpu_utilization {
      target = 0.75
    }
  }
}

