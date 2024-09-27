import asyncio
import logging
import sys
import requests 

from decouple import config
from aiogram import Bot, Dispatcher, html, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = config('TELEGRAM_SECRET_KEY')

form_router = Router()
dp = Dispatcher()

class Form(StatesGroup):
    name = State()

@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer(
        "Добрый день. Как вас зовут?",
    )

@form_router.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    usd = await get_exchange_rate()
    await message.answer(f'Рад знакомству, {message.text}! Курс доллара сегодня {int(usd)}р')

async def get_exchange_rate():
    res = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    res_json = res.json()
    return res_json['Valute']['USD']['Value']

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(form_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())