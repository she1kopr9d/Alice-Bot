from aiogram import Bot
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.tags import *
from app.ai.gpt import LinkedChat, DB_Chat
from app.callbackdata import Davinchik_CBD
from app.database.requests import get_character_2
from app.handlers.user import create_anket

from app.filters import IsActiveChat

router = Router()

@router.callback_query(Davinchik_CBD.filter(F.action == LIKE))
async def like(query: CallbackQuery, callback_data: Davinchik_CBD, bot: Bot, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.message.answer("Отлично!")
    #await state.set_state(ChattingState.chatting)
    character = await get_character_2(callback_data.id)
    await LinkedChat.Add(query.message.chat.id)
    ai : DB_Chat = LinkedChat.Get(query.message.chat.id)
    await ai.system_send(character.description)
    await ai.system_send("Отвечай, будто ты в диалоге, сообщение до этого, это твоя роль")
    await query.message.answer(f"Диалог начат с {character.name} {character.age} лет")

@router.message(IsActiveChat())
async def chatting(message: Message, state: FSMContext):
    user_input = message.text
    if user_input == "/stop":
        await stop(message, state)
        return
    await LinkedChat.Add(message.chat.id)
    ai : DB_Chat = LinkedChat.Get(message.chat.id)
    answer = await ai.send(user_input)
    await message.answer(answer)

@router.message(Command(commands=["stop"]) and IsActiveChat())
async def stop(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Диалог закончен")
    await LinkedChat.Remove(message.chat.id)
    await message.answer("Теперь мы будем искать анкеты по вашему запросу")
    await create_anket(message)