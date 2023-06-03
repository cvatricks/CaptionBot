import os
import pymongo

class Config(object):
    # get a token from https://chatbase.com
    CHAT_BASE_TOKEN = os.environ.get("CHAT_BASE_TOKEN", "lskdfjsdj")
    # get a token from @BotFather
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "6049064152:AAFUbjpWbOCnkWonbRG7gUZJZd9jZmMp1Pg")
    # The Telegram API things
    APP_ID = int(os.environ.get("APP_ID", 123))
    API_HASH = os.environ.get("API_HASH", "123abcde")
    # Get these values from my.telegram.org
    # Banned Unwanted Members..
    MONGODB_URL = os.environ.get("MONGODB_URL", "db://url")
    myclient = pymongo.MongoClient(str(MONGODB_URL))
    mydb = myclient["mutelist"]
    MUTEDB = mydb["words"]
    NOCAPDB = mydb["nocapdb"]
    LINKDB = mydb["linkdb"]
    WORK_CHAT = os.environ.get("WORK_CHAT", "-1233445")
