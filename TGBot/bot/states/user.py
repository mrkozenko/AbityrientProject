from aiogram.filters.state import State, StatesGroup


class Registration(StatesGroup):
    # User input data for DB like name,mail,phone...
    StartRegistration = State()
    Name = State()
    Phone = State()
    Mail = State()
    Instagram = State()


class Quiz(StatesGroup):
    # user start give answers on quiz
    Start = State()  # here we load questions and in loop send to user
    AnswerProcess = State()


class SpecialtySearch(StatesGroup):
    # user start give answers on quiz
    Search = State()


class ProfileUpdate(StatesGroup):
    # change information field of current user profile
    UpdateField = State()


class SenderForm(StatesGroup):
    # for sending messages to students
    InputMessageLink = State()
    SubmitLink = State()
