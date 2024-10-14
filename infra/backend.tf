terraform {
  backend "gcs" {
    bucket  = "project-currency-exchange-tf-state"
    prefix  = "terraform/state"
    project = var.project
  }
}
