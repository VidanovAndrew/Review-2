from datetime import datetime
import Parser
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, ValidationError
import html
import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, StringCommandHandler
import database
from collections import Counter



# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    helped = "i can \n new_docs <N> \n new_topics <N> \n" \
             " doc <doc_title> \n words <topic_name> \n describe_doc <doc_title \n "
    update.message.reply_text(helped)


def echo(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def rbc_main_parse(update: Update, _: CallbackContext) -> None:
    # update.message.reply_text('I\'m already working on it')
    new = database.get_main_news(_.args[0])
    for i in new:
        update.message.reply_text(i[1])
        update.message.reply_text(i[3])
    # update.message.reply_text('Parsed')

    
def update_main_news(update: Update, _: CallbackContext) -> None:
    for i in database.update_main_news():
        print(i[1])
        print(i[4])
        print(i[5])


def update_topic_news(update: Update, _: CallbackContext) -> None:
    database.update_topic_news(_.args[0])
    print(_.args)


def get_topic_news(update: Update, _: CallbackContext) -> None:
    new = database.get_topic_news(_.args[0])
    for i in new:
        update.message.reply_text(i[1])
        update.message.reply_text(i[3])


def words(update: Update, _: CallbackContext) -> None:
    new = database.get_topic_news(_.args[0])
    answer = ''
    for i in new:
        answer += i[4]
        answer += ' '
    update.message.reply_text(answer)


def describe_topic(update: Update, _: CallbackContext) -> None:
    topic = database.describe_topic(_.args[0])
    length = len(topic)
    summary = 0
    for article in topic:
        summary += len(article[2])
    update.message.reply_text("amount of notes: " + str(length))
    update.message.reply_text("average length of note: " + str(summary / length))


def get_article(update: Update, _: CallbackContext) -> None:
    says = " ".join(_.args)
    print(says)
    answer = database.get_article(says)
    if answer is None:
        update.message.reply_text("i didn't find")
    else:
        update.message.reply_text(answer[2])


def get_statistic(update: Update, _: CallbackContext) -> None:
    says = " ".join(_.args)
    print(says)
    answer = database.get_article(says)
    if answer is None:
        update.message.reply_text("i didn't find")
    else:
        commons = Counter(html.escape(answer[2]).split()).most_common(5)
        for word in commons:
            ans = str(word[0]) + ' : ' + str(word[1])
            update.message.reply_text(ans)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1713836874:AAFvVy8bk-j9MxBw8ml5V0HmqVHjHcJVuK4")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("update", update_main_news))
    dispatcher.add_handler(CommandHandler("up", update_topic_news))
    dispatcher.add_handler(CommandHandler("topic", get_topic_news))
    dispatcher.add_handler(CommandHandler("new_docs", rbc_main_parse))
    dispatcher.add_handler(CommandHandler("doc", get_article))
    dispatcher.add_handler(CommandHandler("describe_doc", get_statistic))
    dispatcher.add_handler(CommandHandler("words", words))
    dispatcher.add_handler(CommandHandler("describe_topic", describe_topic))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()


# print(database.update_topic_news("City"))
