import requests
import asyncio
from config import TOKENS, refresh_tokens as refresh_tokens_db
import json
from app.database.requests import set_tag_token, create_chat, get_active_chat, IsActiveChat, update_messages, archive_chat
from app.database.models import Chat as ChatModel

URL = "https://api.openai.com/v1/chat/completions"

SYSTEM = "system"
USER = "user"
ASSISTANT = "assistant"

count_request = 0

async def refresh_tokens():
    global count_request
    tokens = await TOKENS()
    await set_tag_token(tokens[(count_request-1)%len(tokens)], "e")
    await refresh_tokens_db()

async def get_header():
    global count_request
    tokens = await TOKENS()
    token = tokens[count_request%len(tokens)]
    count_request+=1
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

def get_body(messages: list) -> dict:
    return {
        "model": "gpt-3.5-turbo-1106",
        "messages": messages
    }

def update(messages: list, role: str, content: str) -> list:
    messages.append({"role": role, "content": content})
    return messages

def undo(message: list) -> list:
    return message.pop(-1)


async def async_request(messages: list, recursion: int = 0) -> str or None:
    recursion += 1
    if recursion >= 5:
        raise Exception("recursion limit")
    header = await get_header()
    body = get_body(messages)
    response = await asyncio.to_thread(requests.post, URL, json=body, headers=header)
    try:
        return json.loads(response.text)["choices"][0]["message"]["content"]
    except:
        return None

class Chat():
    def __init__(self, messages: list = []) -> None:
        self.messages = messages

    def system_send(self, message: str) -> None:
        self.messages = update(self.messages, SYSTEM, message)

    async def safe_request(self, messages: list) -> str or None:
        try:
            return await async_request(messages)
        except:
            raise Exception("recursion limit")

    async def send(self, message: str) -> str:
        self.messages = update(self.messages, USER, message)
        answer = await self.safe_request(self.messages) 
        if answer == None:
            self.messages = undo(self.messages)
        else:
            self.messages = update(self.messages, ASSISTANT, answer)
        #print("------\n", message, "\n\n\n", answer, "\n------")
        return answer
    
class DB_Chat():
    def __init__(self, tg_id: int, messages: list = []) -> None:
        self.messages = messages
        self.tg_id = tg_id

    async def system_send(self, message: str) -> None:
        self.messages = update(self.messages, SYSTEM, message)
        await update_messages(self.tg_id, SYSTEM, message)

    async def safe_request(self, messages: list) -> str:
        try:
            return await async_request(messages)
        except Exception as e:
            print(e)
            return await self.safe_request(messages)

    async def send(self, message: str) -> str:
        self.messages = update(self.messages, USER, message)
        await update_messages(self.tg_id, USER, message)
        answer = await self.safe_request(self.messages)
        self.messages = update(self.messages, ASSISTANT, answer)
        await update_messages(self.tg_id, ASSISTANT, message)
        print("------\n", message, "\n\n\n", answer, "\n------")
        return answer

class LinkedChat():
    chats = dict()

    async def Add(tg_id: int, messages: list = []) -> None:
        if (await IsActiveChat(tg_id)) == False:
            await create_chat(tg_id)
        chat = await get_active_chat(tg_id)
        LinkedChat.chats.update({tg_id: DB_Chat(tg_id, json.loads(chat.messages))})

    def Get(tg_id: int) -> DB_Chat:
        return LinkedChat.chats[tg_id]
    
    async def Remove(tg: int) -> None:
        await archive_chat(tg)
        try:
            LinkedChat.chats.pop(tg)
        except:
            pass
