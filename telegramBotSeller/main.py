import asyncio
import config
from aiogram import Dispatcher, types
from Bot.handler import Handler
from database.base import Base, engine
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Bot.filter import Admin
Base.metadata.create_all(bind=engine)
dp = Dispatcher(config.aiogramBot, storage=MemoryStorage())
dp.filters_factory.bind(Admin)

async def main():
    BotHandler = Handler(dp)
    BotHandler.RegisterAdminEvent()
    BotHandler.RegisterWaitEvent()
    BotHandler.RegisterCommands()
    BotHandler.RegisterTextMessage()
    BotHandler.RegisterCallBack()
    print(f"---[@{(await config.aiogramBot.get_me()).username}]Бот успешно запущен---")
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
