from bot_config import dp
from handlers import (
    start,
    info,
    products,
    order,
    fsm
)


start.register_handlers(dp)
info.register_handlers(dp)
products.register_handlers(dp)
order.register_handlers(dp)
fsm.register_handlers(dp)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
