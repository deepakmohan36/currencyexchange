terraform {
  backend "gcs" {
    bucket = "project-currency-exchange"
    prefix = "terraform/state/jamf_mobile"
  }
}