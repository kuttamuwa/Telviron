"""
Telegram Notification Service

"""
from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from notifications.models.models import TelegramActive, MessageStore
from notifications.scheduled.bgscheduler import scheduler
from notifications.services.telegram.singleton import Singleton


class IDumanTelegramService(metaclass=Singleton):
    bot_admin_username = 'etoletta'  # admin / creator / tester / developer etc. username
    date_example = "22052022-16:00"
    date_format = "%d%m%Y-%H:%M"
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
        message_handler = CommandHandler('set', self.set_message)
        self.dispatcher.add_handler(message_handler)

    def start(self, update, context):
        # save active channel information to use again
        user = update.effective_chat.username
        TelegramActive.objects.update_or_create(username=user, chat_id=update.effective_chat.id)

        keyboard = [
            [
                InlineKeyboardButton("Get Previous All Time Messages", callback_data='get_message'),
            ],
            [
                InlineKeyboardButton("Set Message", callback_data='set_message')
            ],
            [
                InlineKeyboardButton("EVERYONE", callback_data='everyone'),
            ],
        ]
        # if user != self.bot_admin_username:
        #     keyboard.pop()

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(
            "Hi! Welcome to Duman RSS Feeder. If you /start me, we'll start to serve you immediately !  \n ",
            reply_markup=reply_markup)

    @staticmethod
    def help_command(update, context):
        update.message.reply_text('Use /start to test this bot.')

    def set_updater(self):
        updater = Updater(token=self.bot.token, use_context=True)

        return updater

    @classmethod
    def get_user_bot(cls, username, add_default=False):
        from notifications.models.models import TelegramNotification

        tele_user = TelegramNotification.objects.get(user__username=username)
        bot = Bot(token=tele_user.token)

        if add_default:
            cls.save_as_default(bot)
        return bot

    @classmethod
    def get_system_bot(cls, add_default=True):
        return cls.get_user_bot('admin', add_default)

    @classmethod
    def save_as_default(cls, bot: Bot):
        cls.bot = bot

    # @staticmethod
    def button(self, update, context) -> None:
        """Parses the CallbackQuery and updates the message text."""
        query = update.callback_query

        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        if query.data == 'subscribe':
            res = self.subscribe(update, context)
            if res[1]:
                msg = "You are already subscribed ! But we updated in any case.. "
            else:
                msg = "Subscribing is successfull ! If you want to unsubscribe \n"
            msg += r"see: \help"

        elif query.data == 'set_message':
            try:
                msg = "Please type like this: \n" \
                      "/set We have an merging announcement with one of GAFAM, 22052022-16:00"
            except PermissionError:
                msg = "You don't have permission to create message ! \n"
                msg += r"Please see: \help"

        elif query.data == 'get_message':
            msg = self.get_message(update, context)

        elif query.data == 'everyone':
            self.send_message_all(update, context)

        else:
            msg = "There is no option ! \n"
            msg += r"Please see: \help"

        query.answer()

        query.edit_message_text(text=msg)

    @classmethod
    def send_message_all(cls, update, context):
        print("SENDING MESSAGES TO EVERYONE")
        messages = MessageStore.objects.all()
        if not messages:
            update.message.reply_text("There is no saved messages : (")
        else:
            for msg in MessageStore.objects.all():
                cls.send_message_one(msg)

        update.message.reply_text("We sent all messages to the everyone !")

    @classmethod
    def send_message_one(cls, msg):
        for subs in TelegramActive.objects.all():
            chat_id = subs.chat_id
            cls.bot.send_message(chat_id=chat_id, text=msg.message)

    # @staticmethod
    def set_message(self, update, context):
        user = update.effective_chat.username
        if user == self.bot_admin_username:  # admin name
            tarih = context.args[-1]
            msg = " ".join(context.args[:-1])[:-1]
            response = (f"Mesaj : {msg} \n"
                        f"Tarih: {tarih}")

            tarih = datetime.strptime(tarih, self.date_format)
            job = scheduler.add_job(
                self.send_message_one,
                'date',
                kwargs={'msg': msg},
                run_date=tarih
            )
            MessageStore.objects.update_or_create(
                message=msg,
                tarih=tarih,
                job_id=job.id
            )
            update.message.reply_text('Created your scheduled message task ! \n'
                                      f'{response}')
        else:
            raise PermissionError("You don't have admin permission, you worm !")

    def get_message(self, update, context):
        user = update.effective_chat.username
        print(f"Messages read by : {user}")
        if len(MessageStore.objects.all()) > 0:
            return "\n \n".join([f"Mesaj : {i.message} \n"
                                 f"Tarih : {i.tarih}" for i in MessageStore.objects.all()])
        else:
            return f"""There is no data in feed :( Why don't you create one ? ex: /set THIS IS FIRST DATA IN FEED, {self.date_example} """

    @staticmethod
    def subscribe(update, context):
        user = update.effective_chat.username
        chat_id = update.effective_chat.id

        return TelegramActive.objects.update_or_create(
            username=user,
            chat_id=chat_id
        )
