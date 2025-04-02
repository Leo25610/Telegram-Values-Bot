API_KEY = "dca05264f3f34e1c8ee6667714080f6d"
base = "USD"
quote = "RUB"
amount = 1000


def convert_currency(base, quote, amount):
    import requests

    url = f"https://openexchangerates.org/api/latest.json?app_id={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "rates" in data and base in data["rates"] and quote in data["rates"]:
        base_to_usd = data["rates"][base]
        quote_to_usd = data["rates"][quote]

        exchange_rate = quote_to_usd / base_to_usd
        converted_amount = amount * exchange_rate

        print(f"{amount} {base} = {converted_amount:.2f} {quote}")
        return converted_amount
    else:
        print("Ошибка: Одна из валют не найдена в базе данных.")
        return None


convert_currency(base, quote, amount)