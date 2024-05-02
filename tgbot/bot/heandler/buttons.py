from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup

class UserState(StatesGroup):
    name = State()
    age = State()
    phone_number = State()
    request = State()

def menu_buttons():
    btn = KeyboardButton(text ='phone_button', request_contact=True)
    return ReplyKeyboardMarkup(keyboard=[[btn]], resize_keyboard=True, one_time_keyboard=True)