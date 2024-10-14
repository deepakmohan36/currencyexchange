locals {
  project = var.project
}

resource "google_storage_bucket" "bucket" {
  name     = "project-currency-exchange" 
  location = var.region
  project = var.project
#   uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "object" {
  name   = "project-currency-exchange-${timestamp()}.zip"
  bucket = google_storage_bucket.bucket.name
  source = "${path.module}/project-currency-exchange.zip"
}

resource "google_cloudfunctions2_function" "function" {
  name = "currency-exchange"
  project = var.project
  location = var.region
  description = "data extraction scripts for project currency exchange"

  build_config {
    runtime = "python312"
    entry_point = "main" 
    source {
      storage_source {
        bucket = google_storage_bucket.bucket.name
        object = google_storage_bucket_object.object.name
      }
    }
  }

  service_config {
    max_instance_count  = 10
    available_memory    = "256M"
    timeout_seconds     = 60
    service_account_email = var.service_account_email
  }
  
  # Ensure that the Cloud Function depends on the updated ZIP file
  depends_on = [google_storage_bucket_object.object]

}

resource "google_cloudfunctions2_function_iam_member" "invoker" {
  cloud_function = google_cloudfunctions2_function.function.id
  location = var.region
  role           = "roles/cloudfunctions.invoker"
  member         = "serviceAccount:${var.service_account_email}"
}


resource "google_cloud_run_service_iam_member" "cloud_run_invoker" {
  service  = google_cloudfunctions2_function.function.service_config[0].service
  location = var.region
  role     = "roles/run.invoker"
  member   = "serviceAccount:${var.service_account_email}"
}


resource "google_cloud_scheduler_job" "invoke_cloud_function" {
  name        = "invoke-gcf-function"
  project     = var.project
  region      = var.region
  description = "Schedule the HTTPS trigger for cloud function currency-exchange"
  schedule    = "30 15 * * *" # every day at 6:30 AM IST
  time_zone   = "Asia/Calcutta"

  http_target {
    uri         = google_cloudfunctions2_function.function.service_config[0].uri
    http_method = "POST"
    oidc_token {
      audience              = "${google_cloudfunctions2_function.function.service_config[0].uri}/"
      service_account_email = var.service_account_email
    }
  }
}
