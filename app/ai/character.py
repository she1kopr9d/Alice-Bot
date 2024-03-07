from app.ai.gpt import Chat, count_request
from app.database.requests import create_character_2

from random import randint

from russiannames.parser import NamesParser

from app.ai.promt_gen import *


def gen_seed():
    return randint(0, 1)



promt_short = 'Перескажи этот текст: '
#promt_name = 'Как тебя зовут? Напиши только имя без точки ((ОДНИМ СЛОВОМ))'
#promt_name = 'Придумай имя'
#promt_age = 'Сколько тебе лет? Напиши только число без точки'
        
black_list = ["Извините", "не могу помочь", "в создании персонажей"]

def check_black_list(message: str):
    if message == None:
        return False
    for word in black_list:
        if word in message:
            return True
    return False

async def ai_request(info: str, recursion: int = 0):
    recursion += 1
    if recursion >= 3:
        return None
    ai = Chat()
    try:
        data = await ai.send(info)
    except:
        return await ai_request(info, recursion)
    if check_black_list(data):
        return await ai_request(info, recursion)
    return data

async def create_character(info: str = "", recursion: int = 0):
    recursion += 1
    if recursion >= 3:
        return None, None, None, None, None
    
    seed = gen_seed()

    name = await gen_name(seed)
    age = gen_age()
    sex = gen_gender(seed)

    dis = await ai_request(info + " " + gen_discription(seed))
    if dis == None:
        return None, None, None, None, None
    short = await ai_request(promt_short + dis)
    if short == None:
        return None, None, None, None, None
    
    await create_character_2(name, age, sex, dis, short)
    return name, age, sex, dis, short