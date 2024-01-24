from aiogram import Bot, Dispatcher, types

from data import config

import telebot
from telebot import apihelper

from data.config import PROXY

apihelper.proxy = {'https': 'socks5://' + PROXY}

bot = Bot(config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot)
