#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import config

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = config.TOKEN
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


def start(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Play ▶️", callback_data='1'),
            InlineKeyboardButton("Stop ⏹", callback_data='2'),
        ],
        [InlineKeyboardButton("Restart 🔃", callback_data='3')],
        [InlineKeyboardButton("Pause ⏯", callback_data='4')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выбери действие:', reply_markup=reply_markup)


def button(update, context) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Выбрано: {query.data}")
    if query.data == "1":
        os.system("mpc play")
    if query.data == "2":
        os.system("mpc stop")
    if query.data == "3":
        os.system("mpc clear")
        os.system("mpc add $(youtube-dl --prefer-insecure -g -f91 jfKfPfyJRdk) && mpc play")
    if query.data == "4":
        os.system("mpc pause")


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Не распознано.")


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))

updater.start_polling()
updater.idle()
