from aiogram.fsm.state import State, StatesGroup

class CreateFormState(StatesGroup):
    name = State()
    age = State()
    gender = State()
    target = State()
    description = State()