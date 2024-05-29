from os import getenv

from dotenv import load_dotenv
from telebot import TeleBot, types

from modules.schedule import Schedule


# Load environment variables from a .env file
load_dotenv()

bot = TeleBot(getenv("TOKEN"))
schedule = Schedule()

# Users' id and their groups
users_groups: dict[int, str] = dict()
# just aboba and nothing else.
aboba = True


@bot.message_handler(commands=["start"])
def start(message: types.Message):
    """Handler for the `/start` command"""

    bot.send_message(message.chat.id, getenv("GREETING"))
    bot.send_message(message.chat.id, getenv("SEND_GROUP"))

    bot.register_next_step_handler(message, set_group)


def set_group(message: types.Message):
    """Set the user's group"""

    users_groups[message.from_user.id] = message.text

    # Check if the schedule for the group exists
    if schedule.check_group(message.text):
        sent_message = bot.send_message(message.chat.id, getenv("SELECT_SCHEDULE"))
        select_schedule(sent_message)
    else:
        sent_message = bot.send_message(message.chat.id, getenv("GROUP_NOT_FOUND"))
        add_schedule(sent_message)


def add_schedule(message: types.Message) -> None:
    """Ask the user if they want to add the schedule"""

    keyboard = types.InlineKeyboardMarkup([[
        types.InlineKeyboardButton(getenv("YES"), callback_data="add_schedule"),
        types.InlineKeyboardButton(getenv("CHANGE_GROUP"), callback_data="change_group")
    ]])
    bot.edit_message_text(getenv("GROUP_NOT_FOUND"),
                          message.chat.id, message.id,
                          reply_markup=keyboard)


def process_schedule(message: types.Message) -> None:
    """Process and add the schedule"""

    # just aboba.
    if not aboba: return

    # Add the schedule and check if it was added successfully
    added = schedule.set_schedule(message, users_groups[message.from_user.id])

    if added:
        # Prompt the user to select the type of schedule
        sent_message = bot.send_message(message.chat.id, getenv("SCHEDULE_ADDED"))
        select_schedule(sent_message)
    else:
        # Ask the user for the correct format
        bot.send_message(message.chat.id, getenv("SCHEDULE_NOT_ADDED"))
        sent_message = bot.send_message(message.chat.id, getenv("ENTER_SCHEDULE"))
        button(types.CallbackQuery(sent_message.id, sent_message.from_user, "add_schedule", sent_message.chat, sent_message.json, sent_message))


def select_schedule(message: types.Message) -> None:
    """Prompt the user to select the type of schedule"""

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
    """Callback query handler for button clicks"""

    # just aboba.
    global aboba

    if callback.data == "day":
        show_schedule = schedule.get_day(users_groups[callback.from_user.id])
    elif callback.data == "week":
        show_schedule = schedule.get_week(users_groups[callback.from_user.id])
    elif callback.data == "session":
        show_schedule = schedule.get_session(users_groups[callback.from_user.id])
    elif callback.data == "back":
        select_schedule(callback.message)
        return
    
    # Button to change group
    elif callback.data == "change_group":
        bot.edit_message_text(getenv("SEND_GROUP"),
                              callback.message.chat.id,
                              callback.message.id)
        # just aboba.
        aboba = False

        bot.register_next_step_handler(callback.message, set_group)
        return

    # Button to add a schedule
    elif callback.data == "add_schedule":
        keyboard = types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton(getenv("BACK"), callback_data="change_group")]])

        bot.edit_message_text(getenv("ENTER_SCHEDULE"),
                              callback.message.chat.id, callback.message.id,
                              reply_markup=keyboard, parse_mode="Markdown")
        # just aboba.
        aboba = True

        bot.register_next_step_handler(callback.message, process_schedule)
        return

    keyboard = types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton(getenv("BACK"), callback_data="back")]])
    bot.edit_message_text(show_schedule,
                          callback.message.chat.id, callback.message.id,
                          reply_markup=keyboard, parse_mode="Markdown")


def main() -> None:
    """Start the bot"""
    bot.polling(non_stop=True)


if __name__ == "__main__":
    main()
