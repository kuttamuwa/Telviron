"""
Telegram Notification Service

"""
import json

import telegram
from django_celery_beat.models import IntervalSchedule, PeriodicTask, SECONDS
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from notifications.models.models import TelegramActive, MessageStore
from notifications.services.image.manipulator import ImageManipulator
from notifications.services.telegram.singleton import Singleton
from usrapp.models.models import CustomUser


class TelegramDataService(metaclass=Singleton):
    bot = None

    def __init__(self, bot=None):
        print("Initializing Telegram Bot")

        self.bot = self.get_system_bot(add_default=False) if bot is None else bot

        self.updater = self.set_updater()
        self.dispatcher = self.updater.dispatcher

        # initial settings
        self.init_settings()

        # start bot
        self.updater.start_polling()

    def init_settings(self):
        # button
        self.dispatcher.add_handler(CallbackQueryHandler(self.button))

        # help
        help_handler = CommandHandler('help', self.help_command)
        self.dispatcher.add_handler(help_handler)

        # start
        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

        # set message
        message_handler = CommandHandler('message', self.set_message)
        self.dispatcher.add_handler(message_handler)

        # unknown
        # unknown_handler = CommandHandler('', self.unknown)
        # self.dispatcher.add_handler(MessageHandler([Filters.command], self.unknown))

    @staticmethod
    def start(update, context):
        # save active channel information to use again
        user = update.effective_chat.username
        TelegramActive.objects.update_or_create(username=user, chat_id=update.effective_chat.id)

        keyboard = [
            [
                InlineKeyboardButton("Option 1", callback_data='1'),
                InlineKeyboardButton("Option 2", callback_data='2'),
            ],
            [InlineKeyboardButton("Option 3", callback_data='3')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(
            "Hi! Welcome to Doviz RSS Feeder. If you /start me, we'll start to serve you immediately !  \n ",
            reply_markup=reply_markup)

    @staticmethod
    def help_command(update, context):
        update.message.reply_text('Use /start to test this bot.')

    @staticmethod
    def rss_store_handler(update, context):
        user = update.effective_chat.username
        # todo: if user is not admin
        rss_name, rss_link = context.args

        # create rss

        msg = f"We are watching the RS Service : {rss_link}"
        update.message.reply_text(msg)

    @staticmethod
    def unknown(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text='')

    def set_updater(self):
        updater = Updater(token=self.bot.token, use_context=True)

        return updater

    @classmethod
    def get_user_bot(cls, username, add_default=False):
        from notifications.models.models import TelegramNotification

        tele_user = TelegramNotification.objects.get(user__username=username)
        bot = telegram.Bot(token=tele_user.token)

        if add_default:
            cls.save_as_default(bot)
        return bot

    @classmethod
    def get_system_bot(cls, add_default=True):
        return cls.get_user_bot('admin', add_default)

    @classmethod
    def save_as_default(cls, bot: telegram.Bot):
        cls.bot = bot

    def send_msg(self, chat_id, msg):
        self.bot.send_message(chat_id, msg)

    @staticmethod
    def button(update, context) -> None:
        """Parses the CallbackQuery and updates the message text."""
        query = update.callback_query

        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        query.answer()

        query.edit_message_text(text=f"Selected option: {query.data}")

    @classmethod
    def send_message_all(cls, msg):
        for usr in TelegramActive.objects.all():
            bot = cls.get_user_bot(username=usr.username, add_default=False)
            bot.send_message(msg)

    @staticmethod
    def set_message(update, context):
        user = update.effective_chat.username
        if user == 'admin':  # admin name
            msg, tarih = context.args
            MessageStore.objects.update_or_create(
                message=msg, tarih=tarih
            )
            update.message.reply_text("Message set !")
        else:
            update.message.reply_text("You don't have admin permission, you worm !")


tele_service = TelegramDataService()
