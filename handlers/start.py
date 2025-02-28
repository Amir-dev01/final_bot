from aiogram import types

async def start_handler(message: types.Message):
    await message.answer(f"Здравствуйте, {message.from_user.first_name}!")

def register_handlers(dp):
    dp.register_message_handler(start_handler, commands=["start"])
