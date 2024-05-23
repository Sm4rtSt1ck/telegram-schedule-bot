from datetime import datetime
from os import getenv
import csv
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

load_dotenv()
TOKEN = getenv("TOKEN")

WEEKDAYS = ["Понедельник", "Вторник", "Среду", "Четверг", "Пятницу", "Субботу", "Воскресенье"]


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Выбери группу, чтобы увидеть расписание.')
    await send_group_selection(update)


def load_groups(filename: str) -> list:
    groups = set()
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            groups.add(row['Group'])
    return sorted(groups)


def load_schedule(filename: str, group: str) -> str:
    schedule = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Group'] == group and row['Day'] == str(datetime.now().weekday()+1):
                formatted_entry = f"`{row['Time']}`: {row['Subject']}, _{row['Room']}_"
                schedule.append(formatted_entry)
    return '\n'.join(schedule) if schedule else 'Расписание не найдено.'


async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    group = query.data

    if group == 'back':
        await send_group_selection(query)
    else:
        schedule = load_schedule('schedule.csv', group)
        keyboard = [[InlineKeyboardButton("Назад", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Расписание для группы *{group}* на *{WEEKDAYS[datetime.now().weekday()]}*:\n\n{schedule}",
                                      reply_markup=reply_markup, parse_mode='Markdown')


async def send_group_selection(update_or_query):
    groups = load_groups('schedule.csv')
    keyboard = [[InlineKeyboardButton(group, callback_data=group)] for group in groups]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if isinstance(update_or_query, Update):
        await update_or_query.message.reply_text(text='Выберите группу:', reply_markup=reply_markup)
    else:
        await update_or_query.edit_message_text(text='Выберите группу:', reply_markup=reply_markup)


def main() -> None:
    # Создаем приложение и передаем ему токен
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))

    # Запуск бота
    application.run_polling()


if __name__ == '__main__':
    main()
