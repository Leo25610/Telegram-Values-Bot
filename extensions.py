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

        # Проверяем, есть ли обе валюты в базе
        missing_currencies = []
        if base not in data["rates"]:
            missing_currencies.append(base)
        if quote not in data["rates"]:
            missing_currencies.append(quote)

        # Если какая-то валюта отсутствует, отправляем конкретную ошибку
        if missing_currencies:
            return f"⚠️ Ошибка: Валюта:  {', '.join(missing_currencies)}  не найдена!"

        # Выполняем конвертацию
        base_to_usd = data["rates"][base]
        quote_to_usd = data["rates"][quote]
        exchange_rate = quote_to_usd / base_to_usd
        converted_amount = amount * exchange_rate

        return f"{amount} {base} = {converted_amount:.2f} {quote}"