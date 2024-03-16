from typing import Optional

from Quiz.models import Result, Quiz
from TGBot.models import TGUser


async def complete_user_registration(user_id: int, username: Optional[str] = None, name: str = "", phone: str = "",
                                     mail: Optional[str] = None, instagram: Optional[str] = None):
    # create of TGuser instance and save to DB
    user = TGUser(tg_id=user_id, tg_username=username, name=name, phone=phone, mail_address=mail,
                  instagram_username=instagram)
    await user.asave()


async def complete_quiz(user_id: int, quiz_id: int, score: int):
    # create of Result instance and save to DB
    try:
        user = await TGUser.objects.filter(tg_id=user_id).afirst()
        quiz = await Quiz.objects.filter(pk=quiz_id).afirst()

        result = Result(quiz=quiz, user=user, score=score)
        await result.asave()
    except Exception as e:
        print(f"complete_quiz - {e}")
