#sql
SQLALCHEMY_URL = "sqlite+aiosqlite:///db.sqlite3"

#telegram
TG_TOKEN = "6788206631:AAEg27nocDegN6LVgwJ3mMUtWTGxx-6T5Yg"

#ai
CGPT_TOKEN = "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"
#ID_YTOKEN = "aje3vk9qautkaef6i8in"
ID_YTOKEN = "b1gk4mlufojp67j8k8gf"
YTOKEN = "AQVNw_0TpXu0U55pIlfV3seW9QIBn-URBNToCeVp"

# character ai
CHAR_TOKEN = "6acd79f14934700fae20a41b829e127db08f0c30"

from app.database.requests import get_tokens
tokens = []

async def refresh_tokens():
    global tokens
    tokens = await get_tokens()
    return tokens

async def TOKENS():
    global tokens
    if len(tokens) == 0:
        tokens = await get_tokens()
    return tokens