import requests

class CurrencyConverter:
    API_URL = "https://api.freecurrencyapi.com/v1/latest?apikey=J3Am3GDPlvlGhuFIpIcU1z57rINJi0QWNT3UgONz"

    def __init__(self):
        self.rates = {}

    def fetch_exchange_rates(self):
        response = requests.get(self.API_URL)
        if response.status_code == 200:
            data = response.json()
            self.rates = data.get("data", {})
            print(self.rates)
        else:
            raise Exception("Failed to fetch exchange rates from the API.")

    def convert_currency(self, amount, source_currency, target_currency):
        source_rate = self.rates.get(source_currency)
        target_rate = self.rates.get(target_currency)

        if not source_rate:
            raise Exception(f"Unsupported source currency: {source_currency}")
        if not target_rate:
            raise Exception(f"Unsupported target currency: {target_currency}")

        converted_amount = amount * (target_rate / source_rate)
        return converted_amount

def get_user_input(prompt):
    value = input(prompt)
    return value.strip()

def get_numeric_input(prompt):
    while True:
        value = get_user_input(prompt)
        try:
            numeric_value = float(value)
            return numeric_value
        except ValueError:
            print("Invalid amount entered. Please enter a numerical value.")

def main():
    converter = CurrencyConverter()
    try:
        converter.fetch_exchange_rates()
    except Exception as e:
        print(f"Error: {str(e)}")
        return

    amount = get_numeric_input("Enter the amount you wish to convert: ")
    source_currency = get_user_input("Enter the source currency (e.g., USD, EUR, GBP, JPY): ").upper()
    target_currency = get_user_input("Enter the target currency (e.g., USD, EUR, GBP, JPY): ").upper()

    try:
        converted_amount = converter.convert_currency(amount, source_currency, target_currency)
        print(f"{amount} {source_currency} is equivalent to {converted_amount:.2f} {target_currency}.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
