import pymongo
from pymongo import MongoClient
import telegram
from telegram.ext import *
import scratch as s
from telegram import KeyboardButton, ReplyKeyboardMarkup

bot = telegram.Bot(token="5123712096:AAFoWsAeO_sJyrsl0upMa-LUCeHE-k8AWYE")

# API_KEY = "5299420575:AAHDNH7-5Q6LhCqgQ_ZBwz8XSY2oFBz6dyM"


MONGODB_URL = "mongodb+srv://pugalkmc:pugalkmc@cluster0.vx30p.mongodb.net/botdbs?retryWrites=true&w=majority"

# MONGODB_URI = os.environ["mongodb+srv://pugalkmc:pugalkmc@cluster0.vx30p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"]

client = MongoClient(MONGODB_URL)
mydb = client.get_default_database()


def start(update, context):
    chat_id = update.message.chat_id
    username = update.message.chat.username
    checking_exist = mydb["people"]

    update.message.reply_text("Please click this /help to continue chat")
    reply_keyboard = [['Question', 'Form Link', 'Active events']]
    update.message.reply_text("Use below buttons for quick access",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                               one_time_keyboard=True))

    for i in checking_exist.find({}):
        if username == i["username"]:
            break
    else:
        checking_exist.insert_one({"_id": chat_id, "username": username})
        bot.sendMessage(chat_id=1291659507, text="New user found @" + str(username))


def help(update, context):
    update.message.reply_text("""Available Commands :-
    /about_project_work - Full details about our work
    /tele_group - HOL Telegram group URL
    /daily_form_link - Daily Task form updated URL
    /active_events - Daily Task form updated URL""")


about_work = "none for now"


def About_Project(update, context):
    update.message.reply_text(about_work)


def tele_group(update, context):
    update.message.reply_text("Telegram group URL:\nhttps://t.me/HeroesoftheLandGroup")


def form(update, context):
    getform_link = mydb["formlink"]
    get = getform_link.find_one({"_id": 0}, {"_id": 0, "link": 1})
    update.message.reply_text(get["link"])


def daily_work(update, context):
    from database import event_logic
    event_logic(update)


def admin_commands():
    admin_cmd = """Available admin commands
    1) append <your text> --to add as question\n
    2) set_form <form link> --to set or update new form\n
    3) set_about <your text> --to add information about this project work\n
    4) set_new_event <your event message> --to set new events\n
    5) del_event <enter text> --delete already used event text to delete"""
    return admin_cmd


commands_list = ["hol_user_list", "hol_user_remove", "remove_admin", "add_admin", "multiple_add_question",
                 "commands_list", "del_event", "set_new_event", "set_new_form", "add_qn", "hol_user_add",
                 "request_question", "permission_list", "announcement_user", "give_all_questions"]

admin_list = ["PugalKMC", "SaranKMC"]


def msg_handle(update, context):
    sender = update.message.reply_text

    username = update.message.chat.username
    # chat_id = update.message.chat_id
    # first_name = update.message.chat.first_name
    # last_name = update.message.chat.last_name
    text = str(update.message.text)
    text_low = text.lower()
    taken = ""
    for i in commands_list:
        if i in text:
            taken = "yes"
            break
    if "question" == text_low:
        from database import question_ask
        question_ask(update, username)

    elif "form link" in text_low:
        form(update, context)
    elif "active events" in text_low:
        from database import event_logic
        event_logic(update)

    elif taken == "yes":
        admin_col = mydb["admins"]
        for i in admin_col.find({}):
            if username == i["username"]:
                from admin_fun import admin_mod
                admin_mod(update, text, bot, telegram)
                break
        else:
            sender("You don't have permission to access this")

    else:
        response = s.sample(text_low)
        sender(response)


def error(update, context):
    pass


def main():
    updater = Updater("5123712096:AAFoWsAeO_sJyrsl0upMa-LUCeHE-k8AWYE", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("tele_group", tele_group))
    dp.add_handler(CommandHandler("about_project_work", About_Project))
    dp.add_handler(CommandHandler("daily_form_link", form))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("active_events", daily_work))
    dp.add_handler(MessageHandler(Filters.text, msg_handle))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


main()
