import requests

class CurrencyConverter:
    def __init__(self):
        self.api_key = 'jrCy84YCw2ofEwigtJGUxPv9DudG1TBQk0MfBXHH'
        self.base_url = 'https://api.freecurrencyapi.com/v1/latest'

    def get_exchange_rate(self, from_currency, to_currency):
        params = {
            'apikey': self.api_key,
            'base_currency': from_currency,
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()

        if 'data' in data:
            rates = data['data']
            if to_currency in rates:
                return rates[to_currency]
            else:
                raise ValueError(f"Unsupported target currency: {to_currency}")
        else:
            raise ValueError("Unable to fetch exchange rates")  
    
    def get_user_input(self):
        amount = input("Enter the amount you wish to convert: ")
        try:
            amount = float(amount)
        except ValueError:
            raise ValueError("Invalid amount entered. Please enter a numerical value.")
        
        ##Better to fetch from the freecurrencyAPI Currency Endpoint directly but below I just tried the easier version of creating a list of supported currency from the documentation (currency list section)
        supported_currency = ["EUR", "USD", "JPY", "BGN", "CZK", "DKK", "GBP", "HUF", "PLN", "RON", "SEK", "CHF", "ISK", "NOK", "HRK", "RUB", "TRY", 
                              "AUD", "BRL", "CAD", "CNY", "HKD", "IDR", "ILS", "INR", "KRW", "MXN", "MYR", "NZD", "PHP", "SGD", "THB", "ZAR"]
        
        source_currency = input("Enter the source currency (e.g., USD, EUR, GBP, JPY): ")
        if source_currency not in supported_currency:
            raise ValueError("Unsupported source currency. Please enter one of the following currencies: USD, EUR, GBP, JPY…")
        #source_currency = self.validate_currency(source_currency)

        target_currency = input("Enter the target currency (e.g., USD, EUR, GBP, JPY): ")
        if target_currency not in supported_currency:
            raise ValueError("Unsupported target currency. Please enter one of the following currencies: USD, EUR, GBP, JPY…")
        ##target_currency = self.validate_currency(target_currency)?

        return amount, source_currency, target_currency
   

    # Create a currency converter function
    def convert(self, amount, source_currency, target_currency):
        # Create a variable that store the currency exchange change rate from the API
        exchange_rate = self.get_exchange_rate(source_currency, target_currency)
        # Convert by multiplying the amount to the target currency exchange rate
        return amount * exchange_rate


def main():
    # Create an object of class CurrencyConverter
    converter = CurrencyConverter()
    # try and except method 
    try:
        # Call the get_user_input function and the values returned will store in the user_input variable (tuple)
        user_input = converter.get_user_input()
        # Define 3 variables and get each element from the tuple of user_input
        amount = user_input[0]  # Can also be written in one line: amount, source_currency, target_currency = user_input 
        source_currency = user_input[1]
        target_currency = user_input[2]
        amount = float(amount)
    except ValueError as e:
        print({e})

    try:
        exchange_rate = converter.get_exchange_rate(source_currency, target_currency) #if its correct, it will execute the get exchange rate function
    except ValueError as e: 
        print({e})


    # Call the convert function and the value returned will stored in output variable        
    output = converter.convert(amount, source_currency, target_currency)
    # Print the output and limit the precision to 2 decimal places
    print(f"{amount} {source_currency} is equivalent to {round(output, 2)} {target_currency}.")
        
if __name__ == '__main__':
    main()     




