import requests

class CurrencyConverter:

    def __init__(self):
        self.api_key = 'jrCy84YCw2ofEwigtJGUxPv9DudG1TBQk0MfBXHH'
        self.base_url = 'https://api.freecurrencyapi.com/v1/latest'
        #self.currncies_api_url = 'https://api.freecurrencyapi.com/v1/currencies'- if necessary to fetch the supported currency list as rturn output 

    # user_input error handling - if input string or negative value  
    # only error handling included but no exceptions are thrown  
    def get_user_input(self):
        amount = 0
        while amount <= 0: 
            try:
                amount = float(input("Enter the amount you wish to convert: "))

                if amount <= 0:
                    print('Please provide a number greater than 0')

            except ValueError:
                print('Provided value is not a number. Please provide a valid number as the amount')
        
        ##Better to fetch from the freecurrencyAPI Currency Endpoint directly but below I just tried the easier version of creating a list of supported currency from the documentation (currency list section)
        supported_currencies = ["EUR", "USD", "JPY", "BGN", "CZK", "DKK", "GBP", "HUF", "PLN", "RON", "SEK", "CHF", "ISK", "NOK", "HRK", "RUB", "TRY", 
                              "AUD", "BRL", "CAD", "CNY", "HKD", "IDR", "ILS", "INR", "KRW", "MXN", "MYR", "NZD", "PHP", "SGD", "THB", "ZAR"]

        # Source and target currency input format - if the currency in the API data list from supported currencies(hard coded above), it is acccepted and if not exception raised for source and target curiencies. 
        source_currency = None
        while source_currency is None:
            user_provided_source_currency = input("Enter the source currency (e.g., USD, EUR, GBP, JPY): ")

            if user_provided_source_currency in supported_currencies:
                source_currency = user_provided_source_currency
            else:
                print('Provided source currency is not valid or not supported. Please provide a supported currency from : ' + str(supported_currencies))
           
        target_currency = None
        while target_currency is None:
            user_provided_target_currency = input("Enter the target currency (e.g., USD, EUR, GBP, JPY): ")

            if user_provided_target_currency in supported_currencies:
                target_currency = user_provided_target_currency
            else:
                print('Provided target currency is not valid or not supported. Please provide a supported currency from : ' + str(supported_currencies))

        return amount, source_currency, target_currency


    def get_exchange_rate(self, source_currency, target_currency):
        params = {
            'apikey': self.api_key,
            'base_currency': source_currency,
        }

        response = requests.get(self.base_url, params=params)

        # handling HTTP response headers. See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
        # HTTP handling in API necessary documented in API documentation. See https://freecurrencyapi.com/docs/#authentication-methods
        # no error handling but during the  get_exchange_rate , only in an error exceptions are thrown 

        if 401 == response.status_code:
            raise Exception('API authentication failed. Invalid API key provided. Unable to access the API')

        if 429 == response.status_code:
            raise Exception('API quota rate limit reached. API refused connection. Please wait')

        if 200 != response.status_code:
            raise Exception('Error while connecting to the API. Giving up')

        data = response.json()

        if 'data' not in data:
            raise Exception('Error while fetching data from the API. No data received')
            
        rates = data['data']

        if target_currency not in rates:
            raise Exception('Provided \'target_currency\' {target_currency} is not found in the API response')
            
        return rates[target_currency]
   

    # Create a currency converter function
    def convert(self, user_input):
        # Create a variable that store the currency exchange change rate from the API
        exchange_rate = self.get_exchange_rate(user_input[1], user_input[2])
        # Convert by multiplying the amount to the target currency exchange rate
        return user_input[0] * exchange_rate


def main():
    # Create an object of class CurrencyConverter
    converter = CurrencyConverter()
    # Call the get_user_input function and the values returned will store in the user_input variable (tuple)
    user_input = converter.get_user_input()

    try:
        # Call the convert function and the value returned will stored in output variable  
        output = converter.convert(user_input)
        
        # Print the output and limit the precision to 2 decimal places
        print(f"{user_input[0]} {user_input[1]} is equivalent to {round(output, 2)} {user_input[2]}.")

    except Exception as e:
        print('Unable to conver the currency. Program ran into error', e)


if __name__ == '__main__':
    main()     
