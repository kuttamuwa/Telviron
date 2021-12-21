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

date_example = "22052022-16:00"
date_format = "%d%m%Y-%H:%M"

db = create_engine(f"sqlite:///{os.path.join(os.path.abspath('.'), 'app.db')}", echo=True)
session = Session(bind=db)

Base = declarative_base()


class TelegramActive(Base):
    __tablename__ = 'telegram_active'

    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    chat_id = Column(String, unique=True)
    username = Column(String, unique=True)


class MessageStore(Base):
    __tablename__ = 'message_store'

    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    msg = Column(String)
    created_date = Column(DateTime, server_default=func.now())
    run_date = Column(DateTime)


# environment functions
def create_user(chat_id, username):
    q = session.query(TelegramActive).filter(TelegramActive.chat_id == chat_id)
    if q.count() == 1:
        q.update(values={
            'chat_id': chat_id,
            'username': 'yarrraaak'})
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
def send_msg_all(text):
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


def help_cmd(update, context):
    response = f"""
    # Select
    /get/<number>: Get nth message
    
    \n\n
    
    # Create
    /create: (only admin) create OR UPDATE messaging task. ex: /create THIS IS FIRST DATA IN FEED, {date_example} 
    /create/<number> (only admin) UPDATE one messaging task. ex: /create THIS IS UPDATE DATA IN FEED
    \n\n
    
    # Read
    /get: Get all messages. 
    
    \n\n
    
    # Delete
    /drop: Messages can be dropped with
    /drop/<number>: Deletes nth message
    
    """

    update.message.reply_text(response)


def create_message(update, context):
    tarih = context.args[-1]
    msg = " ".join(context.args[:-1])[:-1]
    tarih = datetime.strptime(tarih, date_format)

    # msg
    MessageStore(
        msg=msg, run_date=tarih
    )

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


def get_messages(update, context):
    messages = " \n\n".join([f"Mesaj : {instance.msg} - Tarih : {instance.run_date}" for
                             instance in session.query(MessageStore)])

    update.message.reply_text(messages)


# bot init
def init_bot():
    # create
    bot = Bot(token=settings.token)
    updater = Updater(token=bot.token, use_context=True)
    dispatcher = updater.dispatcher

    # handlers
    start_handler = CommandHandler('start', start_cmd)
    dispatcher.add_handler(start_handler)

    set_handler = CommandHandler('set', create_message)
    dispatcher.add_handler(set_handler)

    # polling
    updater.start_polling()
    updater.idle()

    return bot


def create_scheduler():
    scheduler = BackgroundScheduler()
    return scheduler


# style: button
# dispatcher.add_handler(CallbackQueryHandler(button)


if __name__ == '__main__':
    create_environment()

    bot = init_bot()
    scheduler = create_scheduler()
    print("Running..")
