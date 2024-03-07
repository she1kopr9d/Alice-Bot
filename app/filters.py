from aiogram.filters import Filter
from aiogram.types import Message

from app.database.requests import IsAdmin as isAdmin
from app.database.requests import IsActiveChat as isActiveChat

class IsActiveChat(Filter):
    async def __call__(self, message: Message):
        return await isActiveChat(message.chat.id)

class IsAdmin(Filter):
    async def __call__(self, message: Message):
        return await isAdmin(message.chat.id)