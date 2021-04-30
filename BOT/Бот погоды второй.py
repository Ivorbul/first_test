import requests
import datetime
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
updater = Updater(token='1739728489:AAG1LyayxDrHlp36qGe8xgoe--LeTGwlO9g', use_context=True)
dispatcher = updater.dispatcher
open_weather_token = "ab31a8709cc00756d96a16532045ed6d"

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Напиши название города и я пришлю инфу по погоде!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def get_weather(update, context):
    try:
        r=requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={update.message.text}&units=metric&lang=ru&appid={open_weather_token}"
        )
        data = r.json()
        #pprint(data)

        city = data["name"]
        cur_weather =data["main"]["temp"]
        humidity =data["main"]["humidity"]
        pressure =data["main"]["pressure"]
        wind =data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_day = sunset_timestamp-sunrise_timestamp

        context.bot.send_message(chat_id=update.effective_chat.id, text=f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в городе {city}:\nТемпература: {cur_weather} С°\n"
              f"Влажность: {humidity} %\nДавление: {pressure} мм.рт.ст.\nВетер: {wind} м/с.\n"
              f"Восход солнца: {sunrise_timestamp}\n"
              f"Закат солнца: {sunset_timestamp}\n"
              f"Долгота дня: {length_day}\n"
              f"Хорошего дня!"
              )

    except Exception as ex:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Нет такого города!!!  Ты географию вообще проходил???")


weather_handler = MessageHandler(Filters.text, get_weather)
dispatcher.add_handler(weather_handler)

updater.start_polling()