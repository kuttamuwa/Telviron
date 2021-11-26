"""
Telegram Notification Service

"""
import json

import telegram
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from telegram.ext import Updater, CommandHandler

from notifications.models.models import TelegramActive
from notifications.services.image.manipulator import ImageManipulator
from notifications.services.telegram.singleton import Singleton


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
        # keyboard test


        # start
        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

        # watch
        watch_handler = CommandHandler('watch', self.watch)
        self.dispatcher.add_handler(watch_handler)

        # watch list
        watch_list_handler = CommandHandler('watchlist', self.watch_list)
        self.dispatcher.add_handler(watch_list_handler)

        # unknown
        # unknown_handler = CommandHandler('', self.unknown)
        # self.dispatcher.add_handler(MessageHandler([Filters.command], self.unknown))

    stringList = {"Name": "John", "Language": "Python", "API": "pyTelegramBotAPI"}
    crossIcon = u"\u274C"

    def send_msg(self, chat_id, msg):
        self.bot.send_message(chat_id, msg)

    @staticmethod
    def watch_list(update, context):
        user = update.effective_chat.username
        tasks = PeriodicTask.objects.filter(name__startswith=user).values('name')

        msg = list(tasks)
        msg = "There is no active task for you :(" if not msg else msg
        update.message.reply_text(msg)

    @staticmethod
    def watch(update, context):
        user = update.effective_chat.username
        try:
            symbol = context.args[0]

            generated_funny = ImageManipulator.generate_funny_crypto(f"{symbol} WATCHING ")

            schedule, created = IntervalSchedule.objects.get_or_create(
                every=5,
                period=IntervalSchedule.SECONDS
            )
            PeriodicTask.objects.update_or_create(
                interval=schedule,
                name=f'{user}_watcher_{symbol}_5s',
                task='price.services.analyzer.ovhl_htf',
                kwargs=json.dumps({
                    'symbol': symbol
                })
            )

            update.message.reply_photo(
                open(generated_funny, 'rb')
            )
        except IndexError:
            update.message.reply_text('Are you sure you add your symbol ? ex. BTC/USDT, ETH/USDT etc.')

    @staticmethod
    def start(update, context):
        user = update.effective_chat.username
        TelegramActive.objects.update_or_create(username=user, chat_id=update.effective_chat.id)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Hi! My name is NPC Dumb Bot. '
                                                                        '@Kuttamuwa created me !')

    @staticmethod
    def unknown(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Ne diyosun amcık')

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
