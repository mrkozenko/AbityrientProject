import asyncio

from aiogram import Router, types
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from TGBot.bot.keyboards.user import main_keyboard
from TGBot.models import TGUser, TemplateBlock, Admins
from TGBot.bot.states.user import Registration, SenderForm
from aiogram import F

# from tgbot.models import User
# from tgbot.bot.utils.extra_datas import make_title

router = Router()


@router.message(StateFilter(None), CommandStart())
async def do_start(message: types.Message, state: FSMContext):
    start_template: TemplateBlock = await TemplateBlock.objects.filter(template_type="START").afirst()
    user = TGUser.objects.get_or_none(pk=message.from_user.id)
    if start_template is None:
        await message.bot.send_message(message.from_user.id, "Шаблон відсутній")
        return None
    keyboard = main_keyboard
    if user is None:
        kb = [[types.KeyboardButton(text="Зареєструватися")], ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await state.set_state(Registration.StartRegistration)
    print("% static 'TGBot/1w.png' %")
    if start_template.image:
        await message.bot.send_photo(message.from_user.id, caption=start_template.description,
                                     photo=FSInputFile(start_template.image.path), reply_markup=keyboard)
    else:
        await message.bot.send_message(message.from_user.id, text=start_template.description, reply_markup=keyboard)


@router.message(StateFilter(None), F.text == "⬅️ Назад")
async def back(message: types.Message, state: FSMContext):
    await do_start(message, state)


@router.message(StateFilter(None), F.text == "/admin")
async def admin_base(message: types.Message, state: FSMContext):
    kb_set = [[types.KeyboardButton(text="⬅️ Назад")]]
    kb_admin_menu = types.ReplyKeyboardMarkup(
        keyboard=kb_set,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    user = TGUser.objects.get_or_none(pk=message.from_user.id)
    if user is not None:
        is_admin = Admins.objects.filter(user=user).exists()
        print(is_admin)
        if is_admin:
            await state.set_state(SenderForm.InputMessageLink)
            await message.answer(text="Перешліть пост з текстом для розсилки", reply_markup=kb_admin_menu)
    else:
        print("no user")


@router.message(SenderForm.InputMessageLink)
async def admin_link_read(message: types.Message, state: FSMContext):
    user = TGUser.objects.get_or_none(pk=message.from_user.id)
    if user is not None:
        kb_set = [[types.KeyboardButton(text="⬅️ Назад")], [types.KeyboardButton(text="Підтвердити ✅")]]
        kb_admin_menu = types.ReplyKeyboardMarkup(
            keyboard=kb_set,
            resize_keyboard=True,
            one_time_keyboard=True
        )
        if message.text == "⬅️ Назад":
            await state.clear()
            await message.answer(
                "Розсилка відмінена!\nЩоб повернутись в адмін меню введіть команду /admin, ваш акаунт повинен бути в розділі адміністраторів")
            await do_start(message, state)
        else:
            await state.update_data(mess_forwarding=message)
            await message.forward(message.from_user.id)
            await message.answer(text="Перед початком розсилки,остаточно підтвердіть її запуск або відмініть.",
                                 reply_markup=kb_admin_menu)
            await state.set_state(SenderForm.SubmitLink)
    else:
        await state.clear()


@router.message(SenderForm.SubmitLink)
async def admin_run_or_back(message: types.Message, state: FSMContext):
    user = TGUser.objects.get_or_none(pk=message.from_user.id)
    if user is not None:
        if message.text == "⬅️ Назад":
            await state.clear()
            await message.answer(
                "Розсилка відмінена!\nЩоб повернутись в адмін меню введіть команду /admin, ваш акаунт повинен бути в розділі адміністраторів")
            await do_start(message, state)
        elif message.text == "Підтвердити ✅":
            print("Запуск розсилки")
            users = TGUser.objects.all().values_list('tg_id', flat=True)
            await message.answer(f"Розсилка запущена, загальна планова кількість учасників, що отримають повідомлення - {len(users)}\nПісля завершення розсилки Ви отримаєте сповіщення.")
            message_bank = await state.get_data()
            message_for_forward:types.Message = message_bank["mess_forwarding"]
            asyncio.create_task(sending_spam(message_for_forward, users))
            await state.clear()
            print("send start")
            await do_start(message, state)
    else:
        await state.clear()


async def sending_spam(message: types.Message,users):
    counter_done = 0
    not_send = 0
    for user_id in users:
        try:
            await message.forward(user_id)
            counter_done+=1
        except Exception as e:
            not_send+=1
            print(e)
        await asyncio.sleep(15)
    await message.bot.send_message(message.from_user.id,f"Розсилка завершена.\nВсього абітурієнтів - {len(users)}\nУспішно надіслано - {counter_done}.\nНе вдалось надіслати - {not_send}.")