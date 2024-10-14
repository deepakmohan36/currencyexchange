import requests

def currency_key_mapping():

    URL = 'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json'

    try:
        
        response = requests.get(URL)

        result = response.json()

        return result
    
    except Exception as e:
        return str(e)
