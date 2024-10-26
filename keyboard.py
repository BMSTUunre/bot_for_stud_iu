from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

import text
from text import Buttons


main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=Buttons.check_points), KeyboardButton(text=Buttons.history)]
    ])

in_state_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=Buttons.cancel)]
    ])


def make_kb(is_admin=False,):
    keyboard = [
        [KeyboardButton(text=Buttons.check_points), KeyboardButton(text=Buttons.history)]
    ]
    if is_admin:
        keyboard[0] += [KeyboardButton(text=Buttons.add_points)]

    return ReplyKeyboardMarkup(keyboard=keyboard)
