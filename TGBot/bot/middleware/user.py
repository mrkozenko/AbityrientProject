import asyncio
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject

from TGBot.bot.handlers.users.main_dialog import do_start
from TGBot.bot.states.user import Registration
from TGBot.models import TGUser


class UserAuthMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user = data["event_from_user"]
        user_db = TGUser.objects.get_or_none(pk=user.id)
        if user_db is None:
            if data.get("state", None) is not None:
                ctnx:FSMContext = data["state"]
                ss = await ctnx.get_state()
                if ss is not None:
                    if "Registration" in ss.split(":")[0]:
                        return await handler(event, data)
                    else:
                        return await do_start(event, data["state"])
                else:
                    return await do_start(event,data["state"])
            else:
                return await do_start(event, data["state"])
        return await handler(event, data)
