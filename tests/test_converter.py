import pytest
from main import CurrencyConverter

def test_convert_happy_path():
    expected_result = 198.111234108
    cc = CurrencyConverter()
    result = cc.convert(user_input = [2, 'EUR', 'RUB'])
    assert result == expected_result

def test_convert_error_input():
    expected_result = -4.3421575672
    cc = CurrencyConverter()
    result = cc.convert(user_input = [-4, 'EUR', 'USD'])
    assert result == expected_result

def test_get_exchange_rate_happy_path():
    expected_result = 99.055617054
    cc = CurrencyConverter()
    result = cc.get_exchange_rate('EUR', 'RUB')
    assert result == expected_result

def test_get_exchange_rate_error_input():
    cc = CurrencyConverter()
    with pytest.raises(Exception):
        cc.get_exchange_rate(324, 'EUR')

def test_get_exchange_rate_empty_input():
    cc = CurrencyConverter()
    with pytest.raises(Exception):
        cc.get_exchange_rate()