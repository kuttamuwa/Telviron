"""
Telegram Notification Service

"""
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, Filters

from notifications.models.models import TelegramNotification
import telegram

from provider.models.models import Doviz, SarrafiyeMilyem
from usrapp.models.models import CustomUser


class TelegramDataService:
    bot = None

    def __init__(self, bot=None):
        self.bot = bot
        if self.bot is None:
            self.bot = self.get_system_bot(False)

        self.updater = self.set_updater()
        self.dispatcher = self.updater.dispatcher

        # initial settings
        self.init_settings()

        # start bot
        self.updater.start_polling()

    def init_settings(self):
        # start
        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

        # watch
        watch_handler = CommandHandler('watch', self.watch)
        self.dispatcher.add_handler(watch_handler)

        # unknown
        # unknown_handler = CommandHandler('', self.unknown)
        # self.dispatcher.add_handler(MessageHandler([Filters.command], self.unknown))

        # milyem makas
        milyem_handler = CommandHandler('add_milyem', self.add_milyem)
        self.dispatcher.add_handler(milyem_handler)

    @staticmethod
    def watch(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Watcher !')

    @staticmethod
    def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Hi! My name is NPC Dumb Bot. '
                                                                        '@Kuttamuwa created me !')

    @staticmethod
    def unknown(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Ne diyosun amcık')

    @staticmethod
    def add_milyem(update, context):
        user = update.effective_chat.username
        kur, alis, satis = context.args

        sarrafiye_milyem = SarrafiyeMilyem.objects.get_or_create(
            kur=kur,
            alis=alis,
            satis=satis,
            source=user
        )

        update.message.reply_text(f'Milyem makası güncellendi ! : {sarrafiye_milyem[0]}')

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
