from aiogram.filters.callback_data import CallbackData


class Davinchik_CBD(CallbackData, prefix="dav"):
    id: int
    action: str