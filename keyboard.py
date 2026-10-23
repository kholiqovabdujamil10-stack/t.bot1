from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="History"),KeyboardButton(text="Help"),KeyboardButton(text="Profile")]],
        resize_keyboard=True
    )