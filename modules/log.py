import logging
from functools import wraps

from telebot import types

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def log_user_activity(func):
    @wraps(func)
    def wrapper(message: types.Message | types.CallbackQuery, *args, **kwargs):
        user_tag = message.from_user.username if message.from_user.username else message.from_user.id
        try:
            logging.info(f"User: {user_tag}, Function: {func.__name__}, Message: {message.text}")
        except AttributeError:
            logging.info(f"User: {user_tag}, Function: {func.__name__}, Callback: {message.data}")
        return func(message, *args, **kwargs)
    return wrapper
