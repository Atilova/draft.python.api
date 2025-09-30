variable "bitwarden_access_token" {
  type      = string
  sensitive = true
}

variable "service_name" {
  type = string
}

variable "image" {
  type = string
}

variable "image_registry" {
  type    = string
  default = "atilova/draft.python.api"
}
