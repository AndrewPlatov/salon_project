import asyncio       # библиотека для работы с асинхронными (параллельными) функциями
from aiogram import Bot, Dispatcher, types  # библиотека для бота: класс бота и класс диспетчера (управляющий класс)
from aiogram.filters import Command
from secret import TOKEN  # Секретный файл, полученный вами в переписке с бот-прародителем
from datetime import datetime
import re

# Django settings
import os
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'salon.settings')
import django
django.setup()

dp = Dispatcher()         # Создание управляющего объекта.
bot = Bot(token=TOKEN)    # Создается объект бота с нашим паролем. Один бот - один экземпляр на токен.
# Команду в бот необходимо вводить так: /start
@dp.message(Command("start"))
async def command_start_handler(message):
    print('Ура! Мне написал', message.chat.id)
    await message.answer(
        "Привет! Я твой помощник в мире русского языка! https://t.me/Russian_Gurubot")
asyncio.run(           # Запуск асинхронной функции
    dp.start_polling(  # диспетчер начинает обмен сообщениями, 
        bot))          # используя бот
# "работа" его - ничего не делать, только ожидать сообщения


@dp.message_handler(commands=['writeme'])
async def handle_writeme(message: types.Message):
    text = message.text
    match = re.search(r'/writeme\s+(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})', text)
    if not match:
        await message.reply("Используйте формат: /writeme ГГГГ-ММ-ДД ЧЧ:ММ")
        return
    
    date_str, time_str = match.groups()
    target_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    now = datetime.now()
    delay = (target_time - now).total_seconds()
    
    if delay <= 0:
        await message.reply("Это время уже прошло.")
        return
    
    await message.reply(f"Я напомню вам в {target_time.strftime('%Y-%m-%d %H:%M')}")
    
    await asyncio.sleep(delay)
    await message.answer(f"Ты просил тебя разбудить в {target_time.strftime('%Y-%m-%d %H:%M')}.")

async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())