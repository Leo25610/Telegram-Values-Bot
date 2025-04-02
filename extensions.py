import requests
from config import API_KEY
class ConvertionException(Exception):
    pass
class Converter:
    @staticmethod
    def convert_currency(base, quote, amount):  #Функция конвертации валюты
        url = f"https://openexchangerates.org/api/latest.json?app_id={API_KEY}"
        response = requests.get(url)
        data = response.json()
        if base in data["rates"] and quote in data["rates"]:
            base_to_usd = data["rates"][base]
            quote_to_usd = data["rates"][quote]

            exchange_rate = quote_to_usd / base_to_usd
            converted_amount = amount * exchange_rate
            return f"{amount} {base} = {converted_amount:.2f} {quote}"
        else:
            return "Ошибка: Одна из валют не найдена в базе данных."