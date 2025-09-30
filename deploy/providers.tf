terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.6"
    }
    bitwarden = {
      source  = "maxlaverse/bitwarden"
      version = "~> 0.15.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
    external = {
      source  = "hashicorp/external"
      version = "~> 2.3"
    }
  }
}

provider "docker" {
  host = "unix:///tmp/docker.sock"
}

provider "bitwarden" {
  access_token = var.bitwarden_access_token

  experimental {
    embedded_client = true
  }
}

provider "null" {}

provider "external" {}
