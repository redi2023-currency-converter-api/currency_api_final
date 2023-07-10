import requests
import config

class CurrencyConverter:
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

        # Source and target currency input format - if the currency in the API data list from SUPPORTED_CURRENCIES(hard coded in line 6), it is acccepted and if not exception raised for source and target curiencies.
        source_currency = None
        while source_currency is None:
            user_provided_source_currency = input("Enter the source currency (e.g., USD, EUR, GBP, JPY): ")
            if user_provided_source_currency in config.SUPPORTED_CURRENCIES:
                source_currency = user_provided_source_currency
            else:
                print('Provided source currency is not valid or not supported. Please provide a supported currency from: ' + str(config.SUPPORTED_CURRENCIES))

        target_currency = None
        while target_currency is None:
            user_provided_target_currency = input("Enter the target currency (e.g., USD, EUR, GBP, JPY): ")
            if user_provided_target_currency in config.SUPPORTED_CURRENCIES:
                target_currency = user_provided_target_currency
            else:
                print('Provided target currency is not valid or not supported. Please provide a supported currency from: ' + str(config.SUPPORTED_CURRENCIES))

        return amount, source_currency, target_currency

    # calling the REST API to get the exchange rates. 
    # All errors and exceptions are deligated to the caller
    def get_exchange_rate(self, source_currency, target_currency):

        params = {
            'apikey': config.API_KEY,
            'base_currency': source_currency,
        }
        response = requests.get(config.BASE_URL, params=params)

        # throwing resulting errors to the caller
        response.raise_for_status()
        data = response.json()
        
        assert 'data' in data, 'Malformed json response from the REST API. The element \'data\' not found'
        rates = data['data']

        assert target_currency in rates, 'Target currency is not supported by the API'
             
        return rates[target_currency]
    
    # Convert the currencies with help of the exchange rates feteched from the API
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
    
    except requests.exceptions.ConnectionError as e:
        print('Network error. Unable to call the REST API: ', e)

    except requests.exceptions.HTTPError as e:
        print('The REST API returned an error: ', e)

    except requests.exceptions.RequestException as e:
        print('Error while connecting to the REST API:', e)
    
    except AssertionError as e:
        print(e)

    except Exception as e:
        print('Unable to convert the currency. Program ran into an error:', e)


if __name__ == '__main__':
    main()