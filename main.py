from datetime import datetime
from os import getenv
import csv

from dotenv import load_dotenv
from telebot import TeleBot, types

from modules.schedule import Schedule

load_dotenv()
TOKEN = getenv("TOKEN")


bot = TeleBot(TOKEN)
schedule = Schedule("schedule.csv")

user_group: dict[int, str] = dict()


@bot.message_handler(commands=["start"])
def start(message: types.Message):
    bot.send_message(message.chat.id, getenv("GREETING"))
    bot.send_message(message.chat.id, getenv("SEND_GROUP"))


@bot.message_handler(regexp="\\d+\\-\\d+")
def set_group(message: types.Message):
    user_group[message.from_user.id] = message.text
    sent_message = bot.send_message(message.chat.id, getenv("SELECT_SCHEDULE"))
    select_schedule(sent_message)


def select_schedule(message: types.Message) -> None:
    keyboard = types.InlineKeyboardMarkup([[
        types.InlineKeyboardButton(getenv("DAY"), callback_data="day"),
        types.InlineKeyboardButton(getenv("WEEK"), callback_data="week"),
        types.InlineKeyboardButton(getenv("SESSION"), callback_data="session")
    ], [
        types.InlineKeyboardButton(getenv("CHANGE_GROUP"), callback_data="change_group")
    ]])

    bot.edit_message_text(getenv("SELECT_SCHEDULE"),
                          message.chat.id, message.id, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda callback: True)
def button(callback: types.CallbackQuery):

    if callback.data == "day":
        show_schedule = schedule.get_day(user_group[callback.from_user.id])
    elif callback.data == "week":
        show_schedule = schedule.get_week(user_group[callback.from_user.id])
    elif callback.data == "session":
        show_schedule = schedule.get_session(user_group[callback.from_user.id])
    elif callback.data == "back":
        select_schedule(callback.message)
        return
    elif callback.data == "change_group":
        bot.edit_message_text(getenv("SEND_GROUP"),
                              callback.message.chat.id, callback.message.id)
        return

    keyboard = types.InlineKeyboardMarkup([[types.InlineKeyboardButton(getenv("BACK"), callback_data="back")]])
    bot.edit_message_text(show_schedule, callback.message.chat.id,
                          callback.message.id, reply_markup=keyboard, parse_mode="Markdown")


def main() -> None:
    bot.polling(non_stop=True)


if __name__ == "__main__":
    main()
