import requests
import functions_framework
import currency_mapping
import conversion_data
import load_to_gcs

@functions_framework.http
def main(request):

    try:  

        currency_keys_json = currency_mapping.currency_key_mapping()

        #extract the list of currency keys
        currency_keys_list = list(currency_keys_json.keys())

        #extract converstion rates by passing the list
        daily_conversion_rates = conversion_data.daily_conversion_data(currency_keys_list)

        #load the result to GCS
        load_to_gcs.load_to_gcs(daily_conversion_rates)


        return {
            "result": "success"
        }, 200
    
    
    except Exception as e:
        return {
            "error": str(e)
        }, 500
