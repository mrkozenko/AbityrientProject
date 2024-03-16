from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
kb_main = [
    [
        types.KeyboardButton(text="👤 Профіль"),
        types.KeyboardButton(text="❓ Ким ти можеш стати?")
    ],
    [types.KeyboardButton(text="🏆 Вікторини",)],
    [types.KeyboardButton(text="📞 Контакти"),
    types.KeyboardButton(text="🏫🎓 Про наш факультет")],
]
main_keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb_main,
    resize_keyboard=True)

