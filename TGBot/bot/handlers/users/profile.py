from aiogram import Router, types
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, InputMediaPhoto, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from django.db.models import Min

from TGBot.bot.handlers.users.main_dialog import do_start
from TGBot.bot.states.user import ProfileUpdate
from TGBot.bot.utils.validators import check_correct_name, is_valid_phone, is_valid_email
from TGBot.models import TGUser

router = Router()

builder = InlineKeyboardBuilder()
builder.row(types.InlineKeyboardButton(text="Змінити ім'я", callback_data="change_name"))
builder.row(types.InlineKeyboardButton(text="Змінити телефон", callback_data="change_phone"))
builder.row(types.InlineKeyboardButton(text="Змінити пошту", callback_data="change_mail"))
builder.row(types.InlineKeyboardButton(text="Змінити instagram", callback_data="change_instagram"))

no_keyboard = InlineKeyboardBuilder()
no_keyboard.row(types.InlineKeyboardButton(text="Відмінити", callback_data="NO"))


@router.message(F.text == "👤 Профіль")
async def show_specialty_menu(message: types.Message, state: FSMContext):
    # добавить логику для загрузки списка специальносте и если есть добавить проверку на картинки
    user: TGUser = await TGUser.objects.filter(pk=message.from_user.id).afirst()
    if user:
        msg_template = f"""
Контактні дані
👤 Ім'я: {user.name}
📞 Телефон: {user.phone}
✉️ E-mail: {user.mail_address} 
📱 Instagram: {'не вказано' if user.instagram_username is None else user.instagram_username}"""
        await message.bot.send_message(message.from_user.id, msg_template, reply_markup=builder.as_markup())


@router.callback_query(ProfileUpdate.UpdateField, F.data == "NO")
async def cancel_action(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await do_start(callback, state)


@router.callback_query(F.data.contains("change"))
async def name_change(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ProfileUpdate.UpdateField)
    if callback.data == "change_name":
        await state.update_data(field_type="change_name")
        await callback.bot.send_message(callback.from_user.id, "Введіть нове ім'я:",
                                        reply_markup=no_keyboard.as_markup())
    elif callback.data == "change_phone":
        await state.update_data(field_type="change_phone")
        await callback.bot.send_message(callback.from_user.id, "Введіть нове номер телефону:",
                                        reply_markup=no_keyboard.as_markup())
    elif callback.data == "change_mail":
        await state.update_data(field_type="change_mail")
        await callback.bot.send_message(callback.from_user.id, "Введіть нову поштову адресу:",
                                        reply_markup=no_keyboard.as_markup())
    elif callback.data == "change_instagram":
        await state.update_data(field_type="change_instagram")
        await callback.bot.send_message(callback.from_user.id, "Введіть новий нікнейм:",
                                        reply_markup=no_keyboard.as_markup())
    await callback.answer()


@router.message(ProfileUpdate.UpdateField)
async def fields_change(message: types.Message, state: FSMContext):
    field_info = await state.get_data()
    if field_info.get("field_type", None) is None:
        await state.clear()
        return None
    field_type = field_info["field_type"]
    msg_text = message.text
    is_correct = None
    record: TGUser = TGUser.objects.filter(tg_id=message.from_user.id).first()
    if field_type == "change_name":
        is_correct = await check_correct_name(msg_text)
        if not is_correct:
            await message.bot.send_message(message.from_user.id,
                                           "Ім'я не повинно містити в собі будь-які сторонні символи.\nВведіть коректні дані")
        else:
            record.name = msg_text
            record.save()
            await state.clear()
            await message.bot.send_message(message.from_user.id, "Ваша інформація успішно оновлена та збережена ✅")
            await do_start(message, state)
    elif field_type == "change_phone":
        is_correct = await is_valid_phone(msg_text)
        if not is_correct:
            await message.bot.send_message(message.from_user.id,
                                           "Перевірте правильність номеру телефону.\nВведіть коректні дані")
        else:
            record.phone = msg_text
            record.save()
            await state.clear()
            await message.bot.send_message(message.from_user.id, "Ваша інформація успішно оновлена та збережена ✅")
            await do_start(message, state)
    elif field_type == "change_mail":
        is_correct = await is_valid_email(msg_text)
        if not is_correct:
            await message.bot.send_message(message.from_user.id,
                                           "Перевірте правильність формату пошти.\nВведіть коректні дані")
        else:
            record.mail_address = msg_text
            record.save()
            await state.clear()
            await message.bot.send_message(message.from_user.id, "Ваша інформація успішно оновлена та збережена ✅")
            await do_start(message, state)
    elif field_type == "change_instagram":
        record.instagram_username = msg_text
        record.save()
        await state.clear()
        await message.bot.send_message(message.from_user.id, "Ваша інформація успішно оновлена та збережена ✅")
        await do_start(message, state)
