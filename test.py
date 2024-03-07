# import asyncio
# from app.ai.generate import Chat, Async_Chat
# while True:
#     print("-"*40)
#     print(Chat("4").send('Сгенеруй на русском языке. Придумай персонажа по шаблону: "Зовут тебя Алиса, тебе 18 лет. Ты любишь рисовать и писать сюжеты, что-то по типу манги. Учишься на первом курсе в университете. Твоя внешность - рост 165, волосы тёмные, стройная фигура, зелёные глаза. Твой характер застенчивый, но тебе интересно со мной общаться." ПРИДУМАЙ СВОЁ, НЕ ИПОЛЬЗУЙ МОЙ ШАБЛОН!!'))
from app.ai.gpt import Chat
import asyncio



async def ask():
    ai = Chat()
    print(await ai.send("Как дела?"))

async def main():
    request = [asyncio.create_task(ask()) for _ in range(10)]
    for req in request:
        await req

if __name__ == "__main__":
    asyncio.run(main())