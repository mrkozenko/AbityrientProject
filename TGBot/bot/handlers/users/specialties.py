from aiogram import Router, types
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, InputMediaPhoto, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from django.db.models import Min

from AbityrientProject import settings
from TGBot.bot.handlers.users.main_dialog import do_start
from TGBot.bot.states.user import SpecialtySearch
from TGBot.models import Specialty, TemplateBlock

router = Router()


@router.message(F.text == "❓ Ким ти можеш стати?")
async def show_specialty_menu(message: types.Message, state: FSMContext):
    #добавить логику для загрузки списка специальносте и если есть добавить проверку на картинки

    kb_main = [
        [
            types.KeyboardButton(text=f"⬅️ Назад"),
        ]
    ]

    if await Specialty.objects.acount() > 0:
        specialty_template: TemplateBlock = await TemplateBlock.objects.filter(template_type="SPECIALTY").afirst()
        if specialty_template is None:
            await message.bot.send_message(message.from_user.id, "Шаблон відсутній")
            return None
        specialties =  Specialty.objects.order_by('priority').only("title").all()
        for specialty in specialties:
            kb_main.append(
            [
                types.KeyboardButton(text=f"{specialty.title}"),
            ])
        main_keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb_main,
            resize_keyboard=True)
        await state.set_state(SpecialtySearch.Search)
        if specialty_template.image:
            await message.bot.send_photo(message.from_user.id, caption=specialty_template.description,photo=FSInputFile(specialty_template.image.path),reply_markup=main_keyboard)
        else:
            await message.bot.send_message(message.from_user.id, text=specialty_template.description,reply_markup=main_keyboard)

    else:
        await message.bot.send_message(message.from_user.id, "Слайди відсутні")

@router.message(SpecialtySearch.Search, F.text)
async def show_specialty_menu(message: types.Message, state: FSMContext):
    #добавить логику для загрузки списка специальносте и если есть добавить проверку на картинки
    #await state.clear()
    text = message.text
    print("mu tyt")
    is_specialty_exist = Specialty.objects.filter(title=text).exists()
    if is_specialty_exist:
        print(is_specialty_exist)
        specialty = await Specialty.objects.filter(title=text).afirst()
        await message.bot.send_photo(message.from_user.id, caption=specialty.title,photo=FSInputFile(specialty.image.path))
    else:
            print("we leave?")
            await state.clear()
            await do_start(message,state)