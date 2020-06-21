import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, MessageHandler, CallbackQueryHandler
from telegram.ext import Filters
from django_telegrambot.apps import DjangoTelegramBot
from emorun.constants import *
from emorun.commands import cmds
from emorun.commands import callback as cb
logger = logging.getLogger(__file__)


def error(update, context):
    print('error detected and catched by error handler')
    error = context.error
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    print('starting')
    logger.info("Loading handlers for emorun")
    dp = DjangoTelegramBot.getDispatcher('emorunbot')
    for cmd in cmds:
        name = cmd.command if hasattr(cmd, 'command') else cmd.__name__
        dp.add_handler(CommandHandler(name, cmd))
        print('added: '+name)
    # dp.add_error_handler(error)
    dp.add_handler(CallbackQueryHandler(cb))
