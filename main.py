from datetime import datetime
from os import getenv
import csv

from dotenv import load_dotenv
from telebot import TeleBot, types

load_dotenv()
TOKEN = getenv("TOKEN")

WEEKDAYS = ["ПОНЕДЕЛЬНИК", "ВТОРНИК", "СРЕДА", "ЧЕТВЕРГ", "ПЯТНИЦА", "СУББОТА", "ВОСКРЕСЕНЬЕ"]

bot = TeleBot(TOKEN)

user_group: dict[int, str] = dict()


@bot.message_handler(commands=["start"])
def start(message: types.Message):
    bot.send_message(message.chat.id, "Привет! Напиши свою группу в чат, чтобы увидеть расписание.")


@bot.message_handler(regexp="\\d+\\-\\d+")
def set_group(message: types.Message):
    user_group[message.from_user.id] = message.text
    select_schedule(message)


def select_schedule(message: types.Message) -> None:
    keyboard = types.InlineKeyboardMarkup([[
        types.InlineKeyboardButton("День", callback_data="day"),
        types.InlineKeyboardButton("Неделя", callback_data="week"),
        types.InlineKeyboardButton("Сессия", callback_data="session")
    ], [
        types.InlineKeyboardButton("Назад", callback_data="start")
    ]])

    bot.send_message(message.chat.id, "Выбери, какое тебе нужно расписание.", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda callback: True)
def button(callback: types.CallbackQuery):

    if callback.data == "day":
        schedule = load_day_schedule(user_group[callback.from_user.id])
    elif callback.data == "week":
        schedule = load_week_schedule(user_group[callback.from_user.id])
    elif callback.data == "session":
        schedule = load_session_schedule(user_group[callback.from_user.id])
    elif callback.data == "back":
        select_schedule(callback.message)
        return
    elif callback.data == "start":
        start(callback.message)
        return

    keyboard = types.InlineKeyboardMarkup([[types.InlineKeyboardButton("Назад", callback_data="back")]])
    bot.edit_message_text(schedule, callback.message.chat.id,
                          callback.message.id, reply_markup=keyboard, parse_mode="Markdown")


def load_day_schedule(group: str) -> str:
    schedule = []
    with open("schedule.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Group'] == group and row['Day'] == str(datetime.now().weekday()+1):
                formatted_entry = f"`{row['Time']}`: {row['Subject']}, _{row['Room']}_"
                schedule.append(formatted_entry)
    return f"*{WEEKDAYS[datetime.now().weekday()]}:*\n{'\n'.join(schedule)}" if schedule else "Расписание не найдено :("


def load_week_schedule(group: str) -> str:
    schedule: dict[str, list[str]] = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
    with open("schedule.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Group'] == group:
                formatted_entry = f"`{row['Time']}`: {row['Subject']}, _{row['Room']}_"
                schedule[int(row['Day'])].append(formatted_entry)
    result = ""
    for day, day_schedule in schedule.items():
        result += f"*{WEEKDAYS[day-1]}:*\n"
        result += "\n".join(day_schedule)+"\n"
    return result if schedule else 'Расписание не найдено.'


def load_session_schedule(group: str) -> str:
    return 'Расписание не найдено.'


def main() -> None:
    bot.polling(non_stop=True)


if __name__ == "__main__":
    main()
