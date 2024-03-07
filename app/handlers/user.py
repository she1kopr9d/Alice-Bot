from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram import Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardRemove

from app.database.requests import create_user, get_user, IsUser, get_random_character_2_filter, IsForm, get_form, get_character_2, delete_form
from app.database.requests import create_form as create_form_db
from app.keyboards import gender, target, r_none
from app.keyboards import davinchik as dav_kb
from app.callbackdata import Davinchik_CBD
from app.database.models import Form
from app.tags import *
from aiogram.fsm.context import FSMContext
from app.states import CreateFormState

from app.ai.gpt import LinkedChat, Chat

targets = {
    "Девушки" : Form.F,
    "Парени" : Form.M,
    "Любые" : Form.B
}

genders = {
    "Мужчина" : "М",
    "Женщина" : "Ж"
}

router = Router()

async def create_form(message: Message, state: FSMContext):
    await state.set_state(CreateFormState.name)
    await message.answer("Как вас зовут?", reply_markup=r_none())

@router.message(CreateFormState.name)
async def name_state(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CreateFormState.age)
    await message.answer("Сколько вам лет?")

@router.message(CreateFormState.age)
async def age_state(message: Message, state: FSMContext):
    if message.text.isdigit():
        if int(message.text) >= 12:
            await state.update_data(age=message.text)
            await state.set_state(CreateFormState.gender)
            await message.answer("Кто вы?", reply_markup=gender())
        else:
            await message.answer("Минимальный возраст 12 лет")
    else:
        await message.answer("Введите число")

@router.message(CreateFormState.gender)
async def gender_state(message: Message, state: FSMContext):
    for variables in genders:
        if message.text == variables:
            await state.update_data(gender=genders[message.text])
            await state.set_state(CreateFormState.target)
            await message.answer("Кто вам интересен?", reply_markup=target())
            return
    await message.answer("Это не правильныва вариант", reply_markup=gender())

@router.message(CreateFormState.target)
async def target_state(message: Message, state: FSMContext):
    for variables in targets:
        if message.text == variables:
            await state.update_data(target=targets[message.text])
            await state.set_state(CreateFormState.description)
            await message.answer("Опишите себя", reply_markup=ReplyKeyboardRemove())
            return
    await message.answer("Это не правильныва вариант", reply_markup=target())

@router.message(CreateFormState.description)
async def description_state(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    state_data = await state.get_data()
    await state.clear()
    user = await get_user(message.from_user.id)
    await delete_form(user)
    await create_form_db(user.id, state_data["name"], state_data["age"], state_data["gender"], state_data["description"], state_data["target"])
    await message.answer("Теперь мы будем искать анкеты по вашему запросу")
    await create_anket(message)

async def create_anket(message: Message):
    user = await get_user(message.chat.id)
    form = await get_form(user.id)
    character = await get_random_character_2_filter(form.target, form.age)
    await message.answer(f"{character.name} {character.age}\n{character.short_description}", reply_markup=dav_kb(character.id))

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    if (await IsUser(message.from_user.id)) == False:
        await create_user(message.from_user.id)
    if (await IsForm(message.from_user)) == False:
        await create_form(message, state)

@router.message(Command(commands=["check"]))
async def cmd_check(message: Message):
    user = await get_user(message.from_user.id)
    await message.answer(f"{user.id}")

@router.message(Command(commands=["search"]))
async def cmd_check(message: Message):
    await create_anket(message)

@router.callback_query(Davinchik_CBD.filter(F.action == SKIP))
async def skip(query: CallbackQuery, callback_data: Davinchik_CBD, bot: Bot):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await create_anket(query.message)

@router.callback_query(Davinchik_CBD.filter(F.action == SLEEP))
async def sleep(query: CallbackQuery, callback_data: Davinchik_CBD, bot: Bot):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await query.message.answer("Хорошо, отстал")