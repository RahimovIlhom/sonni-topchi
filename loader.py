from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from data import config
from utils import Database, AsyncJSONManager

bot = Bot(token=config.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

db = Database()
json_manager = AsyncJSONManager()


async def on_startup_bot():
    await db.connect()
    await json_manager.read_messages()
    await json_manager.preload_texts()


async def stop_bot():
    await db.disconnect()
    await json_manager.close()
