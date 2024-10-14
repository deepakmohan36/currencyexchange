import requests

def daily_conversion_data(currency_keys):

    data = []
    try:

        for key in currency_keys:

            URL = f'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{key}.json'
            response = requests.get(URL)
            result = response.json()
            print(f'loading the result for {key}')
            data.append(result)

        return data
            
    except Exception as e:
        return str(e)