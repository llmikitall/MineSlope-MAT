import asyncio
import os
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv

import BadMessage
import Commands
from Structures import StartMenu, MainMenu, SendMessageMenu

if load_dotenv():
    print("[+] Файл .env успешно инициирован!")
else:
    print("[-] Файл .env не найден!")

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)

DP = Dispatcher()
DP.include_router(Commands.router)
DP.include_router(StartMenu.router)
DP.include_router(MainMenu.router)
DP.include_router(SendMessageMenu.router)
DP.include_router(BadMessage.router)


async def main():
    logging.basicConfig(stream=sys.stdout)
    await DP.start_polling(BOT)


if __name__ == "__main__":
    asyncio.run(main())
