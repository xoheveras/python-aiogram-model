from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.keyboard import *
from config import ADS_NAME_BUTTON, ADS_NAME_CAPTION, URL_BOT
from states.States import *
import re

# @dp.message_handler(commands=["start"], state="*", chat_type=["private"])
# async def start(message: types.Message, state: FSMContext):
