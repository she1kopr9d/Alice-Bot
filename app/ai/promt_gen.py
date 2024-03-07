from app.ai.gpt import Chat

import random

discription_seed = ["девушку", "парня"]
gender_seed = ["Ж", "М"]
name_seed = ["девушке", "парня"]


def gen_discription(seed: int):
    return f'Без имени и возраста. Сгенеруй на русском языке. Придумай персонажа {discription_seed[seed]} по шаблону: "Ты любишь рисовать и писать сюжеты, что-то по типу манги. Учишься на первом курсе в университете. Твоя внешность - рост 165, волосы тёмные, стройная фигура, зелёные глаза. Твой характер застенчивый, но тебе интересно со мной общаться." ПРИДУМАЙ СВОЁ, НЕ ИПОЛЬЗУЙ МОЙ ШАБЛОН!!'

def gen_gender(seed: int):
    return gender_seed[seed]

async def gen_name(seed: int) -> str or None:
    return await Chat().send(f'Придумай русское {name_seed[seed]} имя, без фамилии, одно слово')

def gen_age() -> int:
    return random.randint(14, 27)

def gen_seed() -> int:
    return random.randint(0, 1)