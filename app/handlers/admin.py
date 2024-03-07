import asyncio
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from app.filters import IsAdmin
from app.ai.gpt import Chat
from app.ai.character import create_character as char_create
from app.database.requests import add_token, InTable

router = Router()
router.message.filter(IsAdmin())

@router.message(Command("my_data"))
async def cmd_my_data(message: Message):
    await message.answer("Информация о вас\n"+
        f"Id - {message.from_user.id}\n" +
        f"Имя - {message.from_user.full_name}\n" +
        f"Ник - {message.from_user.username}\n" +
        f"Язык - {message.from_user.language_code}\n")
    
@router.message(Command("r3"))
async def cmd_r3(message: Message):
    args = message.text.split(" ")
    ai = Chat()
    text = await ai.send("".join(args[1:]))
    await message.answer(text)

bS = " "

async def create_character():
    ai = Chat()
    answer1 = await ai.send('Сгенеруй на русском языке. Придумай персонажа по шаблону: "Зовут тебя Алиса, тебе 18 лет. Ты любишь рисовать и писать сюжеты, что-то по типу манги. Учишься на первом курсе в университете. Твоя внешность - рост 165, волосы тёмные, стройная фигура, зелёные глаза. Твой характер застенчивый, но тебе интересно со мной общаться." ПРИДУМАЙ СВОЁ, НЕ ИПОЛЬЗУЙ МОЙ ШАБЛОН!!')
    print(answer1)
    if len(answer1) == 0:
        return await create_character()
    if answer1[0] not in bS:
        return answer1, await ai.send(f'Сгенеруй на русском языке. Опиши себя в ((10 словах))"')
    else:
        return await create_character()
        

@router.message(Command("gen_ch"))
async def cmd_gen_ch(message: Message):
    name, age, sex, dis, short = await char_create()

    await message.answer(f"Имя - {name}\n" +
                         f"Возраст - {age}\n" +
                         f"Пол - {sex}\n" +
                         f"Описание - {dis}\n" +
                         f"Краткое описание - {short}\n")
    
async def create_character_2(message: Message, info: str):
    name, age, sex, dis, short = await char_create(info)
    if name == None:
        await message.answer("Не удалось сгенерировать персонажа")
        return
    await message.answer(f"Имя - {name}\n" +
                        f"Возраст - {age}\n" +
                        f"Пол - {sex}\n" +
                        f"Описание - {dis}\n" +
                        f"Краткое описание - {short}\n")

@router.message(Command("auto_gen"))
async def cmd_auto_gen(message: Message):
    args = message.text.split(" ")
    count = 1
    threads = 1
    info = ""
    if len(args) > 1:
        threads = int(args[1])
    if len(args) > 2:
        count = int(args[2])
    if len(args) > 3:
        info = "".join(args[3:])
    for _ in range(count):
        reqs = [asyncio.create_task(create_character_2(message, info)) for _ in range(threads)]
        for req in reqs:
            await req
        
    await message.answer("Готово")

@router.message(Command("add_tokens"))
async def cmd_add_tokens(message: Message):
    lines = message.text.replace("\n", ":").split(":")
    for line in lines:
        print(line)
        if line[:3] != "sk-":
            continue
        if await InTable(line):
            await message.answer(f"Токен {line} уже есть в базе")
            continue
        await add_token(line)
        await message.answer(f"Добавлен токен {line}")

