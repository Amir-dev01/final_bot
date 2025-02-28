from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_config import bot, database, STUFF_USERS


class StoreFSM(StatesGroup):
    name = State()
    category = State()
    size = State()
    price = State()
    product_id = State()
    photo = State()


async def is_staff(user_id: int) -> bool:
    return user_id in STUFF_USERS


async def start_store_fsm(message: types.Message):
    if not await is_staff(message.from_user.id):
        await message.answer("У вас нет доступа к этой команде!")
        return
    await message.answer("Введите название товара:")
    await StoreFSM.name.set()


async def load_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите категорию:")
    await StoreFSM.category.set()


async def load_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("Введите размер:")
    await StoreFSM.size.set()


async def load_size(message: types.Message, state: FSMContext):
    await state.update_data(size=message.text)
    await message.answer("Введите цену:")
    await StoreFSM.price.set()


async def load_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Введите артикул:")
    await StoreFSM.product_id.set()


async def load_product_id(message: types.Message, state: FSMContext):
    await state.update_data(product_id=message.text)
    await message.answer("Отправьте фото:")
    await StoreFSM.photo.set()


async def load_photo(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("Отправьте изображение!")
        return

    photo_file_id = message.photo[-1].file_id
    data = await state.get_data()
    data["photo"] = photo_file_id

    database.add_product(data)

    text = (f"Товар добавлен!\n\n"
            f"{data['name']}\n"
            f"Категория: {data['category']}\n"
            f"Размер: {data['size']}\n"
            f"Цена: {data['price']} \n"
            f"Артикул: {data['product_id']}\n")

    await message.answer_photo(photo=photo_file_id, caption=text)
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_store_fsm, commands=["add_product"], state=None)
    dp.register_message_handler(load_name, state=StoreFSM.name)
    dp.register_message_handler(load_category, state=StoreFSM.category)
    dp.register_message_handler(load_size, state=StoreFSM.size)
    dp.register_message_handler(load_price, state=StoreFSM.price)
    dp.register_message_handler(load_product_id, state=StoreFSM.product_id)
    dp.register_message_handler(load_photo, content_types=["photo"], state=StoreFSM.photo)
