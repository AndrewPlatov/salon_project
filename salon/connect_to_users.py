import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

# Django setup
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salon.settings')
import django
django.setup()

from bookings.models import Booking, MessageRecord

from asgiref.sync import sync_to_async

@sync_to_async
def save_message(user_id, text):
    msg_record = MessageRecord(user_id=user_id, message_text=text)
    msg_record.save()
    return msg_record

@sync_to_async
def get_all_bookings():
    return list(Booking.objects.all())

from salon.secret import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def command_start_handler(message: Message):
    print('Ура! Мне написал', message.chat.id)
    data = await get_all_bookings()
    print(data)
    await message.answer("Привет! Отправьте мне сообщение, и я сохраню его в базу данных.")

# Обработка всех сообщений (не команд)
@dp.message()
async def handle_message(message: Message):
    await save_message(user_id=message.from_user.id, text=message.text)
    await message.answer("Ваше сообщение сохранено!")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)