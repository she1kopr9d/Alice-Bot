from app.database.models import User, Admin, Character_2, Token, async_session, Form, Chat
from sqlalchemy import select
from random import randint
import json

#chat

async def IsActiveChat(tg_id: int):
    chat = await get_active_chat(tg_id)
    return chat is not None

async def archive_chat(tg_id: int):
    async with async_session() as session:
        result = await session.scalar(select(Chat).where(Chat.status == Chat.ACTIVE).where(Chat.tg_id == tg_id))
        result.status = Chat.ARCHIVED
        await session.commit()
        await session.refresh(result)

async def update_messages(tg_id: int, role: str, content: str):
    async with async_session() as session:
        result = await session.scalar(select(Chat).where(Chat.status == Chat.ACTIVE).where(Chat.tg_id == tg_id))
        messages = json.loads(result.messages)
        messages.append({"role": role, "content": content})
        result.messages = json.dumps(messages)
        await session.commit()
        await session.refresh(result)

async def create_chat(tg_id: int):
    async with async_session() as session:
        chat = Chat(tg_id=tg_id, status=Chat.ACTIVE)
        session.add(chat)
        await session.commit()
        await session.refresh(chat)
        return chat

async def get_active_chat(tg_id: int):
    chats = await get_active_chats()
    chats = [chat for chat in chats if chat.tg_id == tg_id]
    if len(chats) == 0:
        return None
    return chats[0]

async def get_active_chats():
    async with async_session() as session:
        result = await session.scalars(select(Chat).where(Chat.status == Chat.ACTIVE))
        return result.all()

async def get_chats():
    async with async_session() as session:
        result = await session.scalars(select(Chat))
        return result.all()

#token

async def set_tag_token(token: str, tag: str):
    async with async_session() as session:
        token = await session.scalar(select(Token).where(Token.token == token))
        token.tag = tag
        await session.commit()
        await session.refresh(token)
        return token
    
async def add_token(token: str):
    async with async_session() as session:
        token = Token(token=token, status=Token.WORK)
        session.add(token)
        await session.commit()
        await session.refresh(token)
        return token
    
async def get_tokens():
    async with async_session() as session:
        result = await session.scalars(select(Token).where(Token.status == Token.WORK))
        return [token.token for token in result.all()]
    
async def InTable(token: str):
    async with async_session() as session:
        result = await session.scalar(select(Token).where(Token.token == token))
        return (result != None)
    
#form
    
async def delete_form(user: User):
    if (await IsForm(user)) == False:
        return 
    async with async_session() as session:
        result = await session.scalar(select(Form).where(Form.user == user.id))
        await session.delete(result)
        await session.commit()


async def IsForm(user: User):
    async with async_session() as session:
        result = await session.scalar(select(Form).where(Form.user == user.id))
        return result != None
    
async def create_form(user: int, name: str, age: int, sex: str, dis: str, target: str):
    async with async_session() as session:
        form = Form(user=user, name=name, age=age, sex=sex, description=dis, target=target)
        session.add(form)
        await session.commit()
        await session.refresh(form)
        return form
    
async def get_forms():
    async with async_session() as session:
        result = await session.scalars(select(Form))
        return result.all()
    
async def get_form(user: int):
    forms = await get_forms()
    for form in forms:
        if int(form.user) == int(user):
            return form
    return None

#character 2

async def get_random_character_2():
    return await get_character_2(randint(1, len(await get_characters_2())-1))

async def get_random_character_2_filter(gender: str, age: str):
    try:
        gender = {Form.F : "Ж", Form.M : "М", Form.B : "Б"}[gender]
        results = await get_characters_2()    
        results = [res for res in results if int(res.age) <= int(age)]
        if gender != "Б":
            results = [res for res in results if res.sex == gender]
        result = results[randint(0, len(results)-1)]
        return result
    except Exception as e:
        return await get_random_character_2()

async def get_character_2(id: int):
    async with async_session() as session:
        result = await session.scalar(select(Character_2).where(Character_2.id == id))
        return result
 
async def get_characters_2():
    async with async_session() as session:
        result = await session.scalars(select(Character_2))
        return result.all()

async def create_character_2(name, age, sex, dis, short):
    async with async_session() as session:
        character_2 = Character_2(name=name, age=age, sex=sex, description=dis, short_description=short)
        session.add(character_2)
        await session.commit()
        await session.refresh(character_2)
        return character_2
    
#user

async def create_user(tg_id: int):
    async with async_session() as session:
        user = User(tg_id=tg_id)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

async def get_user(tg_id: int):
    async with async_session() as session:
        result = await session.scalar(select(User).where(User.tg_id == tg_id))
        return result
    
async def IsUser(tg_id: int):
    return (await get_user(tg_id)) != None

#admin
    
async def get_admin(tg_id: int):
    async with async_session() as session:
        result = await session.scalar(select(Admin).where(Admin.tg_id == tg_id))
        return result
    
async def IsAdmin(tg_id: int):
    return (await get_admin(tg_id)) != None