import asyncio       # библиотека для работы с асинхронными (параллельными) функциями
from aiogram import Bot, Dispatcher  # библиотека для бота: класс бота и класс диспетчера (управляющий класс)
from aiogram.filters import Command

# Django settings
import os
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'salon.settings')
import django
django.setup()

from bookings.models import Booking

from asgiref.sync import sync_to_async
@sync_to_async
def get_data():
    return
list(Booking.objects.all())

from salon.secret import TOKEN
dp = Dispatcher()         # Создание управляющего объекта.
bot = Bot(token=TOKEN)    # Создается объект бота с нашим паролем. Один бот - один экземпляр на токен.
# Команду в бот необходимо вводить так: /start
@dp.message(Command("start"))
async def command_start_handler(message):
    print('Ура! Мне написал', message.chat.id)
    data = await get_data()
    print(data)
    await message.answer(
        "Ты написал:" + message.text)
asyncio.run(           # Запуск асинхронной функции
    dp.start_polling(  # диспетчер начинает обмен сообщениями, 
        bot))          # используя бот
# "работа" его - ничего не делать, только ожидать сообщения

from bookings.models import Booking

@sync_to_async
def get_tasks():
    return list(Booking.objects.all())

@dp.message(Command("whatsnew"))
async def handle_whatsnew(message):
    tasks = await get_tasks()
    if not tasks:
        await message.answer("Нет новых задач.")
        return

    data_lines = []
    for task in tasks:
        line = f"Задача: {task.title}, Дедлайн: {task.deadline.strftime('%Y-%m-%d')}"
        data_lines.append(line)

    data_text = "\n".join(data_lines)
    await message.answer(data_text)

if __name__ == '__main__':
    asyncio.run(dp.start_polling())