"""
Duman ARGE RSS Feeder

"""
import os.path
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine, Column, Integer, String, Sequence, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from telegram import Bot
from telegram.ext import Updater, CommandHandler

from config import settings

global bot

date_example = "22052022-16:00"
date_format = "%d%m%Y-%H:%M"

db = create_engine(f"sqlite:///{os.path.join(os.path.abspath('.'), 'app.db')}", echo=True)
session = Session(bind=db)

Base = declarative_base()

scheduler = BackgroundScheduler(daemon=True)


# bot init
def init_bot():
    # create
    bot = Bot(token=settings.token)
    updater = Updater(token=bot.token, use_context=True)
    dispatcher = updater.dispatcher

    # handlers
    help_handler = CommandHandler('help', help_cmd)
    dispatcher.add_handler(help_handler)

    get_handler = CommandHandler('get', get_messages)
    dispatcher.add_handler(get_handler)

    # get_handler_q = CommandHandler('get', get_messages)
    # dispatcher.add_handler(get_handler)

    start_handler = CommandHandler('start', start_cmd)
    dispatcher.add_handler(start_handler)

    set_handler = CommandHandler('create', create_message)
    dispatcher.add_handler(set_handler)

    # polling
    updater.start_polling()

    return bot, updater


class TelegramActive(Base):
    __tablename__ = 'telegram_active'

    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    chat_id = Column(String, unique=True)
    username = Column(String, unique=True)


# environment functions
def create_user(chat_id, username):
    q = session.query(TelegramActive).filter(TelegramActive.chat_id == chat_id)
    if q.count() == 1:
        q.update(values={
            'chat_id': chat_id,
            'username': username})
    else:
        user = TelegramActive(chat_id=chat_id, username=username)
        session.add(user)

    session.commit()


def create_environment():
    # creation
    Base.metadata.create_all(db)
    print("Table created !")

    # add default user
    create_user(chat_id=settings.default_chat_id, username=settings.default_username)
    print("Default chat id inserted !")


# bot functions
def help_cmd(update, context):
    response = f"""
    # Select
    /get/<number>: Get nth message
    /get: Get all messages. 
    \n

    # Create
    /create: (only admin) create OR UPDATE messaging task. ex: /create THIS IS FIRST DATA IN FEED, {date_example} 
    /create/<number> (only admin) UPDATE one messaging task. ex: /create THIS IS UPDATE DATA IN FEED
    \n

    # Delete
    /drop: Messages can be dropped with
    /drop/<number>: Deletes nth message
    
    \n
    # Send
    /send: Started to send each message to everyone
    """

    update.message.reply_text(response)


# SELECT
def get_messages(update, context):
    messages = scheduler.get_jobs()
    if messages:
        messages = "\n ".join([f"Message : {i.kwargs['text']} - Run time : {i.next_run_time}" for i in messages])
        update.message.reply_text(messages)
    else:
        update.message.reply_text('There is no saved message :( ')


def send_msg_all(text):
    print("SENDING TO EVERYONE ! ")
    for instance in session.query(TelegramActive):
        bot.send_message(chat_id=instance.chat_id, text=text)


def start_cmd(update, context):
    user = update.effective_chat.username
    chat_id = update.effective_chat.id

    update.message.reply_text(
        "Hi! Welcome to Duman RSS Feeder. Started ! \n"
        "See: /help")
    create_user(
        username=user,
        chat_id=chat_id
    )


def create_message(update, context):
    tarih = context.args[-1]
    msg = " ".join(context.args[:-1])[:-1]
    tarih = datetime.strptime(tarih, date_format)

    response = (f"Mesaj : {msg} \n"
                f"Tarih: {tarih}")

    job = scheduler.add_job(
        send_msg_all,
        'date',
        kwargs={'text': msg},
        run_date=tarih
    )

    # commit
    session.commit()

    update.message.reply_text(response)


if __name__ == '__main__':
    bot, updater = init_bot()

    create_environment()
    scheduler.start()
    updater.idle()
