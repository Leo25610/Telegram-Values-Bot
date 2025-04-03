import telebot
import requests
from extensions import Converter,ConvertionException



bot = telebot.TeleBot(config.TOKEN)
api = config.API_KEY


#Обрабатывает команду: "/values"(список доступных валют)
@bot.message_handler(commands=['values'])
def send_list_of_values(message):
    url = f"https://openexchangerates.org/api/currencies.json?app_id={api}"
    response=requests.get(url)
    data= response.json()
    currincies=[f'{key} : {value}' for key,value in data.items()]
    chunk_size=50
    for i in range(0,len(currincies),chunk_size):
        chunk='\n'.join(currincies[i:i+chunk_size])
        bot.send_message(message.chat.id, f"Список доступных валют: \n {chunk}")


# Обрабатываем сообщения содержащие команды: '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Здравствуйте, {message.chat.username}")
    bot.send_message(message.chat.id, f'Введите пожалуйста данные для рассчета курса в формате: <валюту для обмена> <валюту на которую хотите обменять> <количество валюты>.(например: USD EUR 1)')
    bot.send_message(message.chat.id,f'Для получения списка валют введите:  /values')


#Обрабатываем сообщения связанные с функционалом бота
@bot.message_handler(func=lambda message: True)  # Теперь бот реагирует на любые сообщения
def handle_conversion(message):
    values = message.text.split()

    if len(values) < 3:
        bot.send_message(message.chat.id,"⚠ Ошибка: Вы ввели слишком мало параметров." )
        return

    if len(values) > 3:
        bot.send_message(message.chat.id,"⚠ Ошибка: Вы ввели слишком много параметров")
        return

    try:
        base, quote, amount = values

        if base.lower() == quote.lower():
            raise ConvertionException(f"Нельзя конвертировать {base} в {base} же!")

        amount = float(amount)  # Проверяем, является ли сумма числом

        result = Converter.convert_currency(base.upper(), quote.upper(), amount)
        bot.send_message(message.chat.id, result)

    except ConvertionException as e:
        bot.send_message(message.chat.id, f"⚠ Ошибка: {e}")
    except ValueError:
        bot.send_message(message.chat.id, "⚠ Ошибка: Введите сумму **цифрами** (например, `100`).", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, "❌ Произошла непредвиденная ошибка. Попробуйте снова.")
        print(f"[ERROR] {e}")  # Выводим ошибку в терминал для отладки



bot.polling(none_stop=True)

