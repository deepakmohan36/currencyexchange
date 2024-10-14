import json
from datetime import datetime
from google.cloud import storage 

def load_to_gcs(daily_conversion_rates):
    
    content = json.dumps(daily_conversion_rates)
    current_date = datetime.now().strftime("%Y-%m-%d")

    bucket_name = 'project-currency-exchange'
    file_name = f'daily_logs/daily_conversion_rates_{current_date}.json'

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Upload the content to GCS
    blob.upload_from_string(content)
    print(f"File {file_name} uploaded to {bucket_name}.")
