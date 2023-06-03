import os
import pymongo

class Config(object):
    # get a token from https://chatbase.com
    CHAT_BASE_TOKEN = os.environ.get("CHAT_BASE_TOKEN", "lskdfjsdj")
    # get a token from @BotFather
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "6049064152:AAFUbjpWbOCnkWonbRG7gUZJZd9jZmMp1Pg")
    # The Telegram API things
    APP_ID = int(os.environ.get("APP_ID", 1725988))
    API_HASH = os.environ.get("API_HASH", "35b829bed9b38bb0a5e8079e777277cf")
    # Get these values from my.telegram.org
    # Array to store users who are authorized to use the bot
    # Banned Unwanted Members..
    PORT = os.environ.get("PORT", "8080")
    myclient = pymongo.MongoClient("mongodb+srv://CaptionRemover:CaptionRemover@cluster0.h5m1p3w.mongodb.net/?retryWrites=true&w=majority")
    mydb = myclient["mutelist"]
    MUTEDB = mydb["words"]
    NOCAPDB = mydb["nocapdb"]
    LINKDB = mydb["linkdb"]
    WORK_CHAT = -1001988780014
    MUTE = ["Ashwin"]
    NOCAP = "True"
    LINKMODE = "True"
