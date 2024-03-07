from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from app.callbackdata import Davinchik_CBD
from app.tags import *
from aiogram.types import KeyboardButton

def r_none():
    return ReplyKeyboardBuilder().as_markup()

def davinchik(id: int):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="❤️", callback_data=Davinchik_CBD(id=id, action=LIKE).pack()))
    builder.add(InlineKeyboardButton(text="👎", callback_data=Davinchik_CBD(id=id, action=SKIP).pack()))
    builder.add(InlineKeyboardButton(text="💤", callback_data=Davinchik_CBD(id=id, action=SLEEP).pack()))
    return builder.as_markup()

def gender():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Мужчина"))
    builder.add(KeyboardButton(text="Женщина"))
    return builder.as_markup(resize_keyboard=True)

def target():
    builer = ReplyKeyboardBuilder()
    builer.add(KeyboardButton(text="Девушки"))
    builer.add(KeyboardButton(text="Парни"))
    builer.add(KeyboardButton(text="Любые"))
    return builer.as_markup(resize_keyboard=True)