module "service" {
  source = "git@github.com:Atilova/swarm.service.terraform.git?ref=v1"

  service_name = var.service_name
  deployment_config = {
    replicas       = 2
    image          = var.image
    image_registry = var.image_registry
  }
  container_config = {
    read_only_fs = false
    resources = {
      reservations = {
        cpus   = "100m"
        memory = "128Mi"
      }
      limits = {
        cpus   = "200m"
        memory = "256Mi"
      }
    }
  }
  ingress = {
    external = {
      http = {
        container_port = 8000
        exposed_urls = {
          "/api/v1/" = "/api/v1/"
          "/metrics" = "/metrics"
        }
      }
    }
    internal = {
      http = {
        container_port = 8000
        exposed_urls = {
          "/" = "/"
        }
      }
    }
  }
  healthcheck = {
    enabled = true
  }
  pre_deployment_jobs = [
    {
      command = "entrypoint python -V && env | grep cf__test__config"
    },
  ]
  cronjobs = [
    {
      name     = "RunEveryMinute"
      schedule = "* * * * *"
      command  = "entrypoint echo \"$(date) - $(python -V && env | grep cf__test__config) ok\"; sleep 10"
    },
    {
      name     = "RunEveryTwoMinutes"
      schedule = "*/2 * * * *"
      command  = "entrypoint echo \"$(date) - Every 2 minutes\""
    },
    {
      name     = "RunEveryFiveMinutes"
      schedule = "*/5 * * * *"
      command  = "entrypoint echo \"$(date) - Every 5 minutes\""
    }
  ]
  env = {
    "cf__test__config"         = "true"
    "cf__gunicorn__bind"       = "0.0.0.0:8000"
    "cf__database__pool__size" = "25"
  }
  config_mounts = [
    {
      name = "example.txt"
      value = <<-EOT
        Hello Hello!
      EOT
    }
  ]
}
