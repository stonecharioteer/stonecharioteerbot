# -*- coding: utf-8 -*-

import os
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                level=logging.DEBUG)

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
import bs4
import xkcd
import matplotlib
matplotlib.use("Agg")

from matplotlib import pyplot as plt
plt.style.use("ggplot")
from .plugins import tempmon

def start(bot, update):
    bot.send_message(chat_id=update.message.id, text="Hello, world!")

def categorize(bot, update):
    """
    Takes a user's query and categorizes it.
    TODO: Use `nltk` or `sklearn` here.
    """
    query = update.message.text.lower()
    if "cowsay" in query:
        if "fortune" in query:
            cowsay_fortune(bot, update)
        else:
            cowsay(bot, update, update.message.text)
        return True
    elif "fortune" in query:
        fortune(bot, update)
        return True
    elif "stats" in query or "statistics" in query:
        df_one_day = tempmon.filter_last_one_day()
        df_one_day.set_index(keys="timestamp",inplace=True)
        fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(9, 20))
        df_one_day["temperature_h"].plot(ax=axes[0])
        axes[0].set_title("Temperature (Humidity Based) [°C]")
        df_one_day["temperature_p"].plot(ax=axes[1])
        axes[1].set_title("Temperature (Pressure Based) [°C]")
        df_one_day["humidity"].plot(ax=axes[2])
        axes[2].set_title("Humidity [%]")
        df_one_day["pressure"].plot(ax=axes[3])
        axes[3].set_title("Pressure [millibar]")
        plt.tight_layout()
        fig.savefig("stats.png",dpi=220)
        bot.send_photo(
                        chat_id=update.message.chat_id, 
                        photo=open("stats.png","rb"))
        return True
        
    elif "temperature" in query:
        df_one_day = tempmon.filter_last_one_day()
        message = "Mean Temperature in the past 24h was \n{:.4f}°C (Pressure based)\n{:.4f} °C (Humidity based)".format(df_one_day["temperature_p"].mean(), df_one_day["temperature_h"].mean())
        send(bot, update, message)
        return True
    elif "humidity" in query:
        df_one_day = tempmon.filter_last_one_day()
        message = "Mean humidity in the past 24h was {:.4f}%".format(df_one_day["humidity"].mean())
        send(bot, update, message)
        return True
    elif "pressure" in query:
        df_one_day = tempmon.filter_last_one_day()
        message = "Mean pressure in the past 24h was {:.4f} millibar".format(df_one_day["pressure"].mean())
        send(bot, update, message)
        return True
    elif "xkcd" in query:
        comic = xkcd.getRandomComic()
        response = "[{}]({})\n{}".format(comic.title, comic.imageLink, comic.altText)
        bot.send_message(
            chat_id=update.message.chat_id, 
            text=response,
            parse_mode=telegram.ParseMode.MARKDOWN)
        return True
    return None

def cowsay(bot, update, text):
    import subprocess
    out = subprocess.check_output(["cowsay", text.replace("cowsay ", "")])
    logging.debug(out.decode("ascii"))
    return send(bot, update, out.decode("ascii"))

def fortune(bot, update):
    import subprocess
    out = subprocess.check_output(["fortune"])
    logging.debug(out.decode("ascii"))
    return send(bot, update, out.decode("ascii"))

def cowsay_fortune(bot, update):
    import subprocess
    out = subprocess.check_output(["fortune"])
    out = subprocess.check_output(["cowsay", out.decode("ascii")])
    return send(bot, update, out.decode("ascii"))

def send(bot, update, message, parse_mode=None):
    if parse_mode is None:
        bot.send_message(chat_id=update.message.chat_id, text=message)
    else:
        bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode=parse_mode)

def response(bot, update):
    response_attempt = categorize(bot, update)
    if response_attempt is None:
        bot.send_message(chat_id=update.message.chat_id, text="I'm not sure what you need.")

def serve(env):
    import logging
    from dotenv import load_dotenv
    load_dotenv(env)
    updater = Updater(token=os.environ["TOKEN"])
    dispatcher = updater.dispatcher
    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)
    response_handler = MessageHandler(Filters.text, response)
    dispatcher.add_handler(response_handler)

    try:
        logging.info("Beginning polling now!")
        updater.start_polling()
    except KeyboardInterrupt:
        updater.stop()
