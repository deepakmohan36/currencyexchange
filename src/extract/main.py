import requests
import functions_framework
import currency_mapping
import conversion_data
import json
from datetime import datetime
import load_to_gcs

@functions_framework.http
def main(request):

    try:  

        currency_keys_json = currency_mapping.currency_key_mapping()

        currency_keys_list = list(currency_keys_json.keys())

        daily_conversion_rates = conversion_data.daily_conversion_data(currency_keys_list)

        content = json.dumps(daily_conversion_rates)

        bucket_name = 'project_currency_exchange'

        current_date = datetime.now().strftime("%Y-%m-%d")

        file_name = f'daily_conversion_rates_{current_date}.json'

        load_to_gcs.upload_to_gcs(bucket_name,file_name, content)



        return {
            "result": currency_keys_list
        }, 200
    
    
    except Exception as e:
        return {
            "error": str(e)
        }, 500
