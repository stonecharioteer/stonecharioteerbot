# -*- coding: utf-8 -*-
import time
import os
import logging
import datetime
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
    elif "stats" in query or "statistics" in query or "weather" in query or "report" in query:
        send(bot, update, "You want the weather report boss? No problemo.")
        if "one week" in query or "1 week" in query:
            send(bot, update, "Pulling data for a week.")
            df_one_day = tempmon.filter_last_one_week()
        elif "one month" in query or "1 month" in query:
            send(bot, update, "Pulling data for a month.")
            df_one_day = tempmon.filter_last_one_month()
        elif "six months" in query or "6 months" in query:
            send(bot, update, "Pulling data for six months.")
            df_one_day = tempmon.filter_last_six_months()
        else:
            send(bot, update, "Pulling data for a day.")
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
    elif "headache" in query or "migraine" in query:
        send(
                bot, 
                update, 
                "Hmm, you want to know if you're going to get a headache or migraine today? Give me a moment, boss. Let me check my completely valid WebMD degree in neurology.")
        df = tempmon.filter_last_one_day()
        min_pressure = df["pressure"].min()
        max_pressure = df["pressure"].max()
        message = "The pressure varied from {:.3f} millibar to {:.3f} millibar in the last 24 hours.".format(min_pressure, max_pressure)
        send(bot, update, message)
        message = "Let me analyse the last one week."
        send(bot, update, message)
        df2 = tempmon.filter_last_one_week()
        end_time = df2["timestamp"].max() - datetime.timedelta(minutes=24*60)
        df2 = df2.loc[df2.timestamp <= end_time]
        min_p = df2["pressure"].min()
        max_p = df2["pressure"].max()
        message = "The pressure varied from {:.3f} millibar to {:3f} millibar in the last week, not including the last 24 hours.".format(min_p, max_p)
        send(bot, update, message)
        range_p_1d = max_pressure - min_pressure
        range_p_1w = max_pressure - min_pressure
        if range_p_1d > range_p_1w:
            message = "The pressure has varied a little too wildly today. The range is {:3f} millibar. You might get a headache.".format(range_p_1d)
        else:
            message = "The pressure variation today has been a little less compared to earlier in the week. You might not get a headache."
        send(bot, update, message) 
        message = "Uh, you know I don't have my MD yet, right boss?"
        send(bot, update. message)

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
    out = subprocess.check_output(["/usr/games/cowsay", text.replace("cowsay ", "").replace("Cowsay ", ""])
    logging.debug(out.decode("ascii"))
    return send(bot, update, out.decode("ascii"))

def fortune(bot, update):
    import subprocess
    out = subprocess.check_output(["/usr/games/fortune"])
    logging.debug(out.decode("ascii"))
    return send(bot, update, out.decode("ascii"))

def cowsay_fortune(bot, update):
    import subprocess
    out = subprocess.check_output(["/usr/games/fortune"])
    out = subprocess.check_output(["/usr/games/cowsay", out.decode("ascii")])
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
