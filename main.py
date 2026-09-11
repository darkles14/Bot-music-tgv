import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Укажите ваш новый токен и HTTPS-ссылку на сайт с интерфесом
BOT_TOKEN = "ВАШ_НОВЫЙ_ТОКЕН_ОТ_BOTFATHER"
WEBAPP_URL = "https://ваш-логин.github.io/telegram-music-bot/" 
OWNER_ID = 6948885848

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# База данных в памяти для теста
admins = {OWNER_ID: "owner"}

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🎧 Открыть Музыкальный Плеер", 
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])
    await message.answer("Нажми кнопку ниже, чтобы запустить плеер:", reply_markup=kb)

@dp.message(Command("grant_admin"))
async def grant_admin(message: types.Message):
    if message.from_user.id != OWNER_ID:
        await message.answer("❌ Нет прав.")
        return
    
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Использование: /grant_admin USER_ID")
        return
        
    target_id = int(args[1])
    admins[target_id] = "admin"
    
    try:
        await bot.send_message(target_id, "👑 Вам выданы права администратора!")
        await message.answer(f"✅ Пользователь {target_id} назначит админом.")
    except Exception:
        await message.answer("✅ Права выданы.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
