terraform {
  backend "gcs" {
    bucket = "project-currency-exchange"
    prefix = "infra/state/project-currency-exchange"
  }
}