import asyncio
import os
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv

import Commands
from Structures import StartMenu, MainMenu, BadMessage, ClaimToPlayerMenu, InputFormMenu, Box1Menu, \
    Box3Menu, Box2Menu, Box4Menu, Box5Menu, Box6Menu


async def main():
    from SQLite.FrequentActions import ExitsTable
    if ExitsTable("users") == 0:
        from SQLite.CreateTables import CreateTableUsers
        await CreateTableUsers()
        print("[>] Таблица [users] отсутствует, пересоздаём...")
    if ExitsTable("requests") == 0:
        from SQLite.CreateTables import CreateTableRequests
        await CreateTableRequests()
        print("[>] Таблица [requests] отсутствует, пересоздаём...")
    print("[+] Все таблицы на месте!")

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
    DP.include_router(ClaimToPlayerMenu.router)
    DP.include_router(InputFormMenu.router)
    DP.include_router(Box1Menu.router)
    DP.include_router(Box2Menu.router)
    DP.include_router(Box3Menu.router)
    DP.include_router(Box4Menu.router)
    DP.include_router(Box5Menu.router)
    DP.include_router(Box6Menu.router)
    DP.include_router(BadMessage.router)

    logging.basicConfig(stream=sys.stdout)
    await DP.start_polling(BOT)


if __name__ == "__main__":
    asyncio.run(main())
