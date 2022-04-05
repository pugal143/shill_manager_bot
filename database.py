import pymongo

from datetime import datetime
import random

client = pymongo.MongoClient()
mydb = client["botdbs"]


def question_ask(update, username):
    sender = update.message.reply_text
    fix = "none"
    question_per = mydb["qn_permission"]
    question = mydb["questions"]
    for i in question_per.find({}):
        check = i["username"]
        if check == username:
            fix = "allow"
    qn_request = mydb["qn_reason"]
    check = qn_request.find_one({"_id": 0})
    if check["request"] == "true":
        if fix == "allow":
            try:
                list_ids = []
                for i in question.find({}):
                    list_ids.append(i["_id"])
                rand = random.choice(list_ids)
                qn_get_unformat = question.find_one({"_id": rand})
                qn_format = qn_get_unformat["question"]
                qn_repeat = qn_get_unformat["repeat"]
                qn_time = datetime.now()
                qn_repeat -= 1
                question.update_one({"_id": rand}, {"$set": {"repeat": qn_repeat, "time": qn_time}})
                if qn_repeat == 0:
                    question.delete_one({"_id": rand})
                sender(qn_format)
            except:
                sender("No questions available at the moment")
        else:
            sender("You don't have permission to get questions")
    else:
        sender("Question provider currently off\nReason:\n{0}".format(check["reason"]))


def event_logic(update):
    events = mydb["events"]
    sender = update.message.reply_text
    length = 0
    for i in events.find({}):
        length += 1
    if length == 0:
        sender("No active events founded")
    else:
        sender("Current active events:")
        for i in events.find({}):
            update.message.reply_text(i["event_text"])


def dict_add(update, text):
    mydb = client["botdbs"]
    total_key = []
    myquestion = mydb["questions"]
    get_all = myquestion.find({})
    for i in get_all:
        get_keys = i["_id"]
        total_key.append(get_keys)
    for i in range(1, 500):
        if i not in total_key:
            from datetime import datetime
            now = datetime.now()
            myquestion.insert_one({"_id": i, "time": now, "question": text, "repeat": 7})
            update.message.reply_text("added at index " + str(i))
            break
    else:
        update.message.reply_text("Out of range 500")

def dict_add_multiple(update, text_list):
    mydb = client["botdbs"]
    myquestion = mydb["questions"]
    now = datetime.now()
    indexing = []
    dup_list = 0
    find_dup = myquestion.find({})
    #
    for i in find_dup:
        get = i["question"]
        if get in text_list:
            text_list.remove(get)
            dup_list += 1
    update.message.reply_text("Total duplicates found:" + str(dup_list))
    #
    for i in text_list:
        total_key = []
        get_all = myquestion.find({})
        for j in get_all:
            get_keys = j["_id"]
            total_key.append(get_keys)
        for k in range(1, 400):
            if k not in total_key:
                myquestion.insert_one({"_id": k,"time":now, "question": i, "repeat": 7})
                indexing.append(k)
                break
        else:
            update.message.reply_text("Out of range 400")
    if len(indexing) == 0:
        update.message.reply_text("list of index used 'None'")
    else:
        update.message.reply_text("list of index used" + str(indexing))
        update.message.reply_text("New multiple questions added")
