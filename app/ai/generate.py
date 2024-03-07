import g4f
from g4f import CreateResult

request_type = {
    "4" : g4f.models.gpt_4,
    "3" : "gpt-3.5-turbo"
}

class Async_Chat():
    messages = []
    def __init__(self, type: str = "3") -> None:
        self.type = request_type[type]

    async def send(self, message: str) -> str:
        self.update("user", message)
        data = await self.get_response()
        self.update("assistant", data)
        return data
    
    async def unsafe_send(self, message: str) -> str:
        self.update("user", message)
        data = await self.unsafe_get_response()
        self.update("assistant", data)
        return data

    def update(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    async def get_response(self) -> str:
        try:
            response = await g4f.ChatCompletion.create_async(
                model=self.type,
                messages = self.messages
            )
            return response
        except Exception as e:
            print("ошибка", e)
            return await self.get_response()
        
    async def unsafe_get_response(self) -> str:
        response = await g4f.ChatCompletion.create_async(
            model=self.type,
            messages = self.messages
        )
        return response

class Chat():
    messages = []
    def __init__(self, type: str = "3") -> None:
        self.type = request_type[type]

    def send(self, message: str) -> str:
        self.update("user", message)
        return self.get_response()
    
    def update(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def get_response(self) -> str:
        try:
            response = g4f.ChatCompletion.create(
                model=self.type,
                messages = self.messages
            )
            return response
        except Exception as e:
            print(e)
            return self.get_response()