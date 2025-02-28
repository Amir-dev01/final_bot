from aiogram import types

async def info_handler(message: types.Message):
    text = "Этот бот создан для управления товарами и заказами."
    await message.answer(text)

def register_handlers(dp):
    dp.register_message_handler(info_handler, commands=["info"])