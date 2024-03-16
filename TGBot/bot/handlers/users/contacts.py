from aiogram import Router, types
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from TGBot.models import TGUser, TemplateBlock
from TGBot.bot.states.user import Registration
from aiogram import F

# from tgbot.models import User
# from tgbot.bot.utils.extra_datas import make_title

router = Router()


@router.message(F.text == "📞 Контакти")
async def do_start(message: types.Message):
    start_template: TemplateBlock = await TemplateBlock.objects.filter(template_type="CONTACTS").afirst()
    if start_template is None:
        await message.bot.send_message(message.from_user.id, "Шаблон відсутній")
        return None
    if start_template.image:
        await message.bot.send_photo(message.from_user.id, caption=start_template.description,
                                 photo=FSInputFile(start_template.image.path) )
    else:
        await message.bot.send_message(message.from_user.id, text=start_template.description)