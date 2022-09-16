# -*- coding: utf-8 -*-
import config
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import logging
logging.basicConfig(level=logging.INFO)
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import CallbackQuery

bot = Bot(token=config.telegram_token)

dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def handler(message: types.Message):
    if message.chat.type == 'private':
        arg = message.get_args()
        send_question = InlineKeyboardMarkup()
        if config.lang == 'ru':
            send_question.row(InlineKeyboardButton('Отправить анонимное сообщение', callback_data=f'confirm_quest:{arg}'))
        elif config.lang == 'en':
            send_question.row(InlineKeyboardButton('Send anonymous message', callback_data=f'confirm_quest:{arg}'))  
        me = await bot.get_me()

        if config.lang == 'ru':
            if arg:
                await bot.send_message(message.from_user.id, f'<b>Добро пожаловать!</b>\n\nВы перешли по ссылке друга и теперь вы можете отправить ему анонимное сообщение.\n\nВаша ссылка, чтобы вам могли задать анонимный вопрос: \n\n<code>https://t.me/{me.username}?start={message.from_user.id}</code>', parse_mode=types.ParseMode.HTML, reply_markup=send_question)
            else:
                await bot.send_message(message.from_user.id, f'<b>Добро пожаловать!</b>\n\nВаша ссылка, чтобы вам могли задать анонимный вопрос: \n\n<code>https://t.me/{me.username}?start={message.from_user.id}</code>', parse_mode=types.ParseMode.HTML)
        elif config.lang == 'en':
            if arg:
                await bot.send_message(message.from_user.id, f'<b>Welcome!</b>\n\nYou have followed a friend\'s link and now you can send him an anonymous message.\n\nYour link so you can be asked an anonymous question: \n\n<code>https://t.me/{me.username}?start={message.from_user.id}</code>', parse_mode=types.ParseMode.HTML, reply_markup=send_question)
            else:
                await bot.send_message(message.from_user.id, f'<b>Welcome!</b>\n\nYour link so you can be asked an anonymous question: \n\n<code>https://t.me/{me.username}?start={message.from_user.id}</code>', parse_mode=types.ParseMode.HTML)

class MessageQuestion(StatesGroup):
    msgq = State() 

@dp.callback_query_handler(text_startswith="confirm_quest")
async def confirm_quest(message: types.Message, state: FSMContext):
    global userid
    userid = str(message.data.split(":")[1])
    if config.lang == 'ru':
        if userid == str(message.from_user.id):
            await bot.send_message(message.from_user.id, f'<b>Вы не можете отправить анонимное сообщение самому себе!</b>', parse_mode=types.ParseMode.HTML)
        else:
            await MessageQuestion.msgq.set()
            await bot.send_message(message.from_user.id, f'<b>Напишите любое анонимное сообщение для друга!</b>', parse_mode=types.ParseMode.HTML)
    elif config.lang == 'en':
        if userid == str(message.from_user.id):
            await bot.send_message(message.from_user.id, f'<b>You cannot send an anonymous message to yourself!</b>', parse_mode=types.ParseMode.HTML)
        else:
            await MessageQuestion.msgq.set()
            await bot.send_message(message.from_user.id, f'<b>Write any anonymous message to a friend!</b>', parse_mode=types.ParseMode.HTML)

@dp.message_handler(state=MessageQuestion.msgq)
async def userinfobans(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['msgq'] = message.text
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        
        if config.lang == 'ru':
            await bot.send_message(userid, f'Вам было отправлено новое анонимное сообщение:\n\n{message.text}')
            await bot.send_message(message.from_user.id, '<b>Ваше анонимное сообщение было успешно отправлено!</b>', parse_mode=types.ParseMode.HTML)
        elif config.lang == 'en':
            await bot.send_message(userid, f'A new anonymous message has been sent to you:\n\n{message.text}')
            await bot.send_message(message.from_user.id, '<b>Your anonymous message was sent successfully!</b>', parse_mode=types.ParseMode.HTML)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates= True)