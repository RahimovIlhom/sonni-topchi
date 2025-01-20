from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from data.config import ADMINS


class BotAdminFilter(BaseFilter):
    async def __call__(self, update: [Message, CallbackQuery], *args, **kwargs) -> bool:

        return str(update.from_user.id) in ADMINS
