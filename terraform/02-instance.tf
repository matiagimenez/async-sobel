
data "google_client_openid_userinfo" "me" {}

# Definimos el template de las VM que se irán creando como workers
resource "google_compute_instance_template" "sobel-worker-template" {
  name_prefix          = var.prefix
  description          = var.desc
  project              = var.project
  region               = var.region
  tags                 = ["${var.tags}"]
  instance_description = var.desc_inst
  machine_type         = var.machine_type
  can_ip_forward       = false

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
  }

  // Como imagen base usamos la creada con Packer (sobel.json)
  disk {
    source_image = var.source_image 
    auto_delete  = true
    boot         = true
  }

  network_interface {
    network = var.network
    
    # Esto es para darle una IP publica a los workers. Pero como son accedidos a través del balanceador, no haría falta.
    # Give a Public IP to instance(s)
    # access_config {
      // Ephemeral IP
    # }
  }

  service_account {
    scopes = ["userinfo-email", "compute-ro", "storage-ro"]
  }

  lifecycle {
    create_before_destroy = true
  }

  # Acá se define que archivo se va al iniciar cada una de las instancias (init.sh)
  metadata_startup_script = file(var.metadata_startup_script)

  # Configuración metadata para ssh key
  # metadata = {
  #   ssh-keys = "${split("@", data.google_client_openid_userinfo.me.email)[0]}:${tls_private_key.keys.public_key_openssh}"
  # }
}
