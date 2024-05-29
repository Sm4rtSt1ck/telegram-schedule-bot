import logging
from functools import wraps

from telebot import types

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%m.%d %H:%M:%S')

def log_user_activity(func):
    @wraps(func)
    def wrapper(data: types.Message | types.CallbackQuery, *args, **kwargs):
        user_tag = data.from_user.username if data.from_user.username else data.from_user.id
        try:
            logging.info(f"User: {user_tag}, Function: {func.__name__}, Message: {data.text}")
        except AttributeError:
            logging.info(f"User: {user_tag}, Function: {func.__name__}, Callback: {data.data}")
        return func(data, *args, **kwargs)
    return wrapper
