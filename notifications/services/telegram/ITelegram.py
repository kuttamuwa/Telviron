"""
Telegram Notification Service

"""
from telegram.ext import Updater

from notifications.models.models import TelegramNotification
import telegram


class TelegramDataService:
    bot = None

    def __init__(self, bot=None):
        self.bot = bot
        if self.bot is None:
            self.bot = self.get_system_bot(False)

        self.updater = self.set_updater()

    def set_updater(self):
        updater = Updater(token=self.bot.token, use_context=True)

        return updater

    @classmethod
    def get_user_bot(cls, username, add_default=False):
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
