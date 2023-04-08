from aiogram import Dispatcher
from aiogram.dispatcher.handler import CancelHandler 
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from loader import db
import keyboards.keyboard as kb

class UserBanned(BaseMiddleware):
    async def on_process_message(self, message: Message, data: dict):

        if not message.from_user.username:
            await message.answer("<b>Я не могу тебя пустить дальше, у тебя нет @username</b>")
            raise CancelHandler

        try:
            user = db.get("SELECT ban FROM users WHERE userid = ?", (message.from_user.id, ))[0]
        except:
            user = 0

        if user == 1:
            await message.answer(
                '<b>🔥 Вы заблокированы</b>'
            )
            raise CancelHandler


    async def on_process_callback_query(self, call: CallbackQuery, data: dict):
        pass

        if not call.from_user.username:
            await call.answer("<b>Я не могу тебя пустить дальше, у тебя нет @username</b>", show_alert=True)
            raise CancelHandler

        try:
            user = db.get("SELECT ban FROM users WHERE userid = ?", (call.from_user.id, ))[0]
        except:
            user = 0

        if user == 1:
            await call.answer(
                '<b>🔥 Вы заблокированы</b>'
            )
            raise CancelHandler