from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from django.db.models import Q

from Quiz.models import Quiz as qz
from TGBot.bot.handlers.users.main_dialog import do_start
from TGBot.bot.keyboards.user import main_keyboard
from TGBot.bot.states.user import Quiz
from TGBot.bot.utils.models_complete import complete_quiz
from TGBot.models import TGUser

router = Router()
import re
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

router = Router()
builder = InlineKeyboardBuilder()
builder.row(types.InlineKeyboardButton(text="Пропустити", callback_data="skip"))


# будет 3 блока, первый загрузка списка викторин, второй выбор викторины и ее автоматический запуск,
# 3-й прохождение, ответ вопрос инлайн хенрдел
@router.message(F.text == '🏆 Вікторини')
async def list_quizes(message: types.Message):
    user =TGUser.objects.get_or_none(pk=message.from_user.id)
    quizes_btns = InlineKeyboardBuilder()
    quizes = qz.objects.filter(
        Q(result__user__isnull=True) | ~Q(result__user=user),
        is_show=True
    ).order_by('-created')
    if quizes.count() > 0:
        for quize in quizes:
            quizes_btns.row(types.InlineKeyboardButton(text=f"{quize.title}", callback_data=f"quiz:{quize.id}"))

        await message.bot.send_message(message.from_user.id, "Список доступних вікторин",
                                       reply_markup=quizes_btns.as_markup())
    else:
        await message.bot.send_message(message.from_user.id, "Доступних вікторин ще нема!")


@router.callback_query(StateFilter(None), F.data.contains("quiz"))
async def quiz_run(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    quiz_bank = await state.get_data()
    quiz_id = callback.data.split(":")[1]
    print(quiz_id)
    current_quiz: qz = qz.objects.filter(pk=quiz_id, is_show=True).first()
    print(current_quiz)
    print("s")
    # question structure - {question}
    quiz_structure = {"quiz_id": quiz_id, "questions": [], "score": 0, "current_question": None,"current_step":None}
    if current_quiz:
        list_questions = current_quiz.get_questions()
        for question in list_questions:
            print(question.id)
            print(question.question_text)
            answers = question.get_answers()
            if quiz_structure["current_question"] is None:
                quiz_structure["current_question"] = question.id
            if quiz_structure["current_step"] is None:
                quiz_structure["current_step"] = question.score_value
            # for temp save question before added to list
            temp_question_structure = {
                "id": question.id,
                "question_text": question.question_text,
                "answers": []
            }
            for answer in answers:
                print(answer.answer_text)
                print(answer.is_correct)
                temp_question_structure["answers"].append({"text": answer.answer_text, "is_correct": answer.is_correct})
            quiz_structure["questions"].append(temp_question_structure)
            await state.update_data(quiz_structure=quiz_structure)
        await state.set_state(Quiz.AnswerProcess)
        mess, keyboard = await build_question(quiz_structure)
        mess = f"Що ж почнемо!\nЯкщо потрібно зупинити вікторину просто надішли команду /start\n"+mess
        await callback.bot.send_message(callback.from_user.id,text = mess, reply_markup=keyboard,parse_mode=ParseMode.HTML )
        await callback.bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)

        # сохранить эти данные в стейте, потом отправить сообщеине что опрос начат.
        # сделать хендлер для сохранения ответов на вопросы или просто сумирования балов и когда вопросов нет, то
        # отправлять в бд в результаты и кидать юзеру стикер
    else:
        await callback.answer(show_alert=True, text="Схоже, що ця вікторина вже закінчилась або не є активною.")
    await callback.answer()
    # загрузка квиза и проверка тчо он не скрыт. если скрыт то отмена.
    # загрузка вопросов и ответов , создание переменной для хранения структуры ответов и вопросов а так же счета


async def build_question(quiz_structure: dict):
    # create message with question and buttons
    message_text = ""
    question_text = quiz_structure["questions"][0]["question_text"]
    message_text += f"<b>{question_text}</b>"
    quiz_answers = InlineKeyboardBuilder()
    kb_main = []
    for answer in quiz_structure["questions"][0]["answers"]:
        kb_main.append([types.KeyboardButton(text=answer['text'])])
    main_keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb_main,
            resize_keyboard=True)
    return message_text,main_keyboard


@router.message(Quiz.AnswerProcess)
async def quiz_process(message: types.Message, state: FSMContext):
    if message.text == "/start":
        await message.bot.send_message(message.from_user.id,text=f"Що ж, дуже шкода, що ти вирішив призупинити та покинути вікторину :(")
        await state.clear()
        await do_start(message, state)
    quiz_bank = await state.get_data()
    quiz_structure = quiz_bank["quiz_structure"]
    current_question = quiz_structure["current_question"]
    user_answer = message.text
    #await message.bot.delete_message(chat_id=callback.from_user.id,message_id=callback.message.message_id)
    q_index_del = None
    current_quesiton_dict = None
    for indx,quiz_question in enumerate(quiz_structure["questions"]):
        if quiz_question["id"] == current_question:
            q_index_del = indx
            current_quesiton_dict = quiz_question
            break
    for answer in current_quesiton_dict["answers"]:
        if answer["is_correct"] and message.text==answer["text"]:
            quiz_structure["score"] = quiz_structure["score"] + quiz_structure["current_step"]
            break
    del quiz_structure["questions"][q_index_del]

    if quiz_structure["questions"]:
        quiz_structure["current_question"] = quiz_structure["questions"][0]["id"]
        await state.update_data(quiz_structure=quiz_structure)
        mess, keyboard = await build_question(quiz_structure)
        await message.bot.send_message(message.from_user.id,text=mess, reply_markup=keyboard,parse_mode=ParseMode.HTML )
    else:

        print("send stiker it's all - save data")
        await complete_quiz(user_id=message.from_user.id,quiz_id=quiz_structure["quiz_id"],score=quiz_structure["score"])
        score = quiz_structure["score"]
        await message.bot.send_message(message.from_user.id,text=f"Дякую, за участь у вікторині, ти великий молодець!\nТвій результат - {score} 🏆")
        await message.bot.send_sticker(message.from_user.id,
                                       sticker="CAACAgIAAxkBAAELpgpl7GXGxNwduEY9g7VpFNN-B-X-pwACqhgAAg9lCEoGzNzn0P2-0zQE",reply_markup=main_keyboard)
        await state.clear()
