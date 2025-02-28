from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_config import database, STUFF_USERS, bot


class OrderFSM(StatesGroup):
    product_id = State()
    size = State()
    quantity = State()
    phone = State()


async def start_order(message: types.Message):
    await message.answer("Введите артикул товара:")
    await OrderFSM.product_id.set()


async def load_product_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["product_id"] = message.text
    await message.answer("Введите размер товара:")
    await OrderFSM.size.set()


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["size"] = message.text
    await message.answer("Введите количество:")
    await OrderFSM.quantity.set()


async def load_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["quantity"] = message.text
    await message.answer("Введите ваши контактные данные:")
    await OrderFSM.phone.set()


async def load_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["phone"] = message.text
        database.add_order(data)

        text = (f"Заказ оформлен!\n\n"
                f"Артикул: {data['product_id']}\n"
                f"Размер: {data['size']}\n"
                f"Количество: {data['quantity']}\n"
                f"Телефон: {data['phone']}")

        await message.answer(text)

    await state.finish()

    for staff_id in STAFF:
        await bot.send_message(staff_id, text)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_order, commands=["order"], state=None)
    dp.register_message_handler(load_product_id, state=OrderFSM.product_id)
    dp.register_message_handler(load_size, state=OrderFSM.size)
    dp.register_message_handler(load_quantity, state=OrderFSM.quantity)
    dp.register_message_handler(load_phone, state=OrderFSM.phone)