from aiogram import Router, types
from aiogram import F
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder
from django.db.models import Min

from AbityrientProject import settings
from TGBot.models import Slider

router = Router()


@router.message(F.text == "🏫🎓 Про наш факультет")
async def open_slider(message: types.Message):
    builder = InlineKeyboardBuilder()
    # builder.row(types.InlineKeyboardButton(text="◀️️", callback_data=f"left:{}"))
    builder.row(types.InlineKeyboardButton(text="▶️", callback_data=f"slide_right:{2}"))
    if await Slider.objects.acount()>0:
        first_slide = await Slider.objects.order_by('priority').afirst()
        img_path = f"{first_slide.image.path}"
        await message.bot.send_photo(message.from_user.id, photo=FSInputFile(img_path),caption="❕ Бажаєш дізнатися більше? Подивись коротеньку презентацію про наш факультет", reply_markup=builder.as_markup())
    else:
        await message.bot.send_message(message.from_user.id,"Слайди відсутні")


@router.callback_query(F.data.contains("slide_right"))
async def slide_right(callback: types.CallbackQuery):
    step = int(callback.data.split(":")[1])
    print(step+1)
    builder = InlineKeyboardBuilder()
    first_slide = await Slider.objects.filter(priority=step).afirst()
    is_slide_exist = await Slider.objects.filter(priority=step+1).aexists()
    print(is_slide_exist)
    btns_list = [types.InlineKeyboardButton(text="◀️️", callback_data=f"slide_left:{step - 1}")]
    if is_slide_exist:
         btns_list.insert(1,types.InlineKeyboardButton(text="▶️", callback_data=f"slide_right:{step+1}"))
    builder.row(*btns_list)
    img_path = f"{first_slide.image.path}"
    print(img_path)
    await callback.bot.edit_message_media(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                          media=InputMediaPhoto(caption=f"📑 Слайд {step}",media=FSInputFile(img_path)),reply_markup=builder.as_markup())
    #await callback.bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                                 #reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data.contains("slide_left"))
async def slide_left(callback: types.CallbackQuery):
    step = int(callback.data.split(":")[1])
    builder = InlineKeyboardBuilder()
    print(step)
    first_slide =await Slider.objects.filter(priority=step).afirst()
    is_slide_exist =await Slider.objects.filter(priority=step - 1).aexists()
    lst_btns = [types.InlineKeyboardButton(text="▶️", callback_data=f"slide_right:{step+1}")]
    cpt_text =None
    if is_slide_exist:
        left_button = types.InlineKeyboardButton(text="◀️️", callback_data=f"slide_left:{step - 1}")
        lst_btns.insert(0,left_button)
        cpt_text =f"📑 Слайд {step}"
    else:
        cpt_text = "❕ Бажаєш дізнатися більше? Подивись коротеньку презентацію про наш факультет"
    builder.row(*lst_btns)
    img_path = f"{first_slide.image.path}"
    await callback.bot.edit_message_media(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                          media=InputMediaPhoto(media=FSInputFile(img_path),caption=cpt_text), reply_markup=builder.as_markup())

    #await callback.bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id, reply_markup=builder.as_markup())
    await callback.answer()
