import re

from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from TGBot.bot.keyboards.user import main_keyboard
from TGBot.bot.states.user import Registration
from TGBot.bot.utils.models_complete import complete_user_registration
from TGBot.bot.utils.validators import check_correct_name, is_valid_phone, is_valid_email

router = Router()
builder = InlineKeyboardBuilder()
builder.row(types.InlineKeyboardButton(text="Пропустити", callback_data="skip"))


@router.message(Registration.StartRegistration, F.text == 'Зареєструватися')
async def start_registration(message: types.Message, state: FSMContext):
    await message.bot.send_message(message.from_user.id, "👤 Введіть своє ім'я")
    await state.set_state(Registration.Name)


@router.message(Registration.Name, F.text)
async def name_registration(message: types.Message, state: FSMContext):
    name = message.text
    is_correct = await check_correct_name(name)
    if message.text == "Зареєструватися":
        is_correct = False
    if not is_correct:
        await message.bot.send_message(message.from_user.id,
                                       "Ім'я не повинно містити в собі будь-які сторонні символи.\nВведіть коректні дані")
    else:
        await state.update_data(name=name)
        await message.bot.send_message(message.from_user.id, "📞 Введіть свій номер телефону")
        await state.set_state(Registration.Phone)


@router.message(Registration.Phone, F.text)
async def phone_registration(message: types.Message, state: FSMContext):
    phone = message.text
    is_correct = await is_valid_phone(phone)
    print(phone)
    if not is_correct:
        await message.bot.send_message(message.from_user.id,
                                       "Перевірте правильність номеру телефону.\nВведіть коректні дані")
    else:
        print(f"{phone}---+")
        await state.update_data(phone=phone)
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(
            text="Пропустити", callback_data="skip")
        )
        await message.bot.send_message(message.from_user.id, "📱✉️ Введіть свій e-mail")
        await state.set_state(Registration.Mail)


@router.message(Registration.Mail, F.text)
async def mail_registration(message: types.Message, state: FSMContext):
    mail = message.text
    is_correct = await is_valid_email(mail)
    if not is_correct:
        await message.bot.send_message(message.from_user.id,
                                       "Перевірте правильність формату пошти.\nВведіть коректні дані")
    else:
        await state.update_data(mail=mail)
        await message.bot.send_message(message.from_user.id, "📱 Введіть свій instagram",
                                       reply_markup=builder.as_markup())
        await state.set_state(Registration.Instagram)


@router.message(Registration.Instagram, F.text)
async def instagram_registration(message: types.Message, state: FSMContext):
    instagram = message.text
    await state.update_data(instagram=instagram)
    user = await state.get_data()
    await complete_user_registration(user_id=message.from_user.id, username=message.from_user.username,
                                     name=user["name"], phone=user["phone"], mail=user["mail"],
                                     instagram=user["instagram"])
    await message.bot.send_message(message.from_user.id, "✅ Реєстрацію завершено", reply_markup=main_keyboard)
    await state.clear()


@router.callback_query(Registration.Instagram, F.data == "skip")
async def instagram_mail_registration(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(instagram=None)
    user = await state.get_data()
    await complete_user_registration(user_id=callback.from_user.id, username=callback.from_user.username,
                                     name=user["name"], phone=user["phone"], mail=user["mail"],
                                     instagram=user["instagram"])
    await callback.bot.send_message(callback.from_user.id, "✅ Реєстрацію завершено", reply_markup=main_keyboard)
    await callback.answer()
    await state.clear()
