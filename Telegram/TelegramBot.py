import logging
from telegram import __version__ as TG_VER
from telegram import Update
from telegram.ext import *
from telegram.ext import Updater
import ClientData


class TelegramBot:
    __instance = None

    def __init__(self):
        if TelegramBot.__instance is not None:
            raise Exception('This Class Singleton!')
        else:
            self.updater = Updater(ClientData.telegramBotApiKey, use_context=True)
            self.dispatcher = self.updater.dispatcher
            TelegramBot.__instance = self

    @staticmethod
    def getInstance():
        if TelegramBot.__instance is None:
            TelegramBot()
        return TelegramBot.__instance

    def sendMessageToUser(self, text, chat_id=ClientData.myUserId) -> None:
        try:
            self.updater.bot.send_message(chat_id=chat_id, text=text)
        except Exception as e:
            print("Something gone wrong! ", e)
