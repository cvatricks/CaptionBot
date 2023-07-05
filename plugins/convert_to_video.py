
# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import re

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config


import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)


from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import enums


@pyrogram.Client.on_message((pyrogram.filters.document | pyrogram.filters.video ) & pyrogram.filters.chat(chats=Config.WORK_CHAT))
async def convert_to_video(bot, update):
    for nocapdb in Config.NOCAPDB.find():
       nocapdb = nocapdb.get("nocapdb")
    if nocapdb == "True":
        await bot.copy_message(
             chat_id = update.chat.id,
             from_chat_id = update.chat.id,
             message_id = update.id,
             caption = ""
        )
        await update.delete()
        return
    else:
        caption = update.caption
        for word in Config.MUTEDB.find():
            word = word.get("word")
            if word in caption:
               caption = caption.replace(word, "")
        newcaption = caption
        for linkdb in Config.LINKDB.find():
            linkdb = linkdb.get("linkdb")
        if linkdb == "True":
           newcaption = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', newcaption, flags=re.MULTILINE)
        msgid = update.id
        await bot.copy_message(
              chat_id = update.chat.id,
              from_chat_id = update.chat.id,
              message_id = update.id,
              caption = "**" + newcaption + "**"
        )
        await update.delete()
        return

@pyrogram.Client.on_message(pyrogram.filters.private)
async def sendname(bot, update):
    try:
      if update.text == "/link":
       try:
         for linkdb in Config.LINKDB.find():
             linkdb = linkdb.get("linkdb")
         if linkdb == "True":
            oldupdate = { "linkdb": "True" }
            updates = { "$set": { "linkdb": "False" } }
            updatedb = Config.LINKDB.update_one(oldupdate, updates)
            await update.reply_text("Link mode de-activated, It means links will not be removed from media.")
            return
         else:
            oldupdate = { "linkdb": "False" }
            updates = { "$set": { "linkdb": "True" } }
            updatedb = Config.LINKDB.update_one(oldupdate, updates)
            await update.reply_text("Link mode activated, It means all the links will be removed from media.")
            return
       except Exception as err:
           logger.info(err)
      if update.text == "/mode":
       try:
         for nocapdb in Config.NOCAPDB.find():
             nocapdb = nocapdb.get("nocapdb")
         if nocapdb == "True":
            oldupdate = { "nocapdb": "True" }
            updates = { "$set": { "nocapdb": "False" } }
            updatedb = Config.NOCAPDB.update_one(oldupdate, updates)
            await update.reply_text("Filter mode activated, It means filtered words only will be removed from media.")
            return
         else:
            oldupdate = { "nocapdb": "False" }
            updates = { "$set": { "nocapdb": "True" } }
            updatedb = Config.NOCAPDB.update_one(oldupdate, updates)
            await update.reply_text("Filter mode de-activated, It means entire caption will be removed from media.")
            return
       except UnboundLocalError:
            newupdate = { "nocapdb": "True" }
            updated = Config.NOCAPDB.insert_one(newupdate)
       except Exception as err:
            logger.info(err)
      if "/add" in update.text:
         try:
            mute = update.reply_to_message.text
            count = 0
            msgedit = await update.reply_text("Please wait")
            for a in mute.split(","):
               insert = { "word": "{}".format(a) }
               insertdb = Config.MUTEDB.insert_one(insert)
               count = count + 1
            await msgedit.edit_text("{} words added, Total Words : {}".format(count, Config.MUTEDB.count_documents({})))
            return
         except Exception as err:
            await update.reply_text(err)
            await update.reply_text("No words found to add")
      if update.text == "/deleteall":
         deletedb = Config.MUTEDB.delete_many({})
         await update.reply_text("Word list cleared successfully from the database.")
      if update.text == "/delete":
         try:
            deltf = update.reply_to_message.text
            count = 0
            msgedit = await update.reply_text("Please wait")
            for x in deltf.split(","):
               deleteone = { "word": x }
               deletedb = Config.MUTEDB.delete_one(deleteone)
               count = count + 1
            await msgedit.edit_text("{} words deleted, Total words : {}".format(count, Config.MUTEDB.count_documents({})))
            return
         except:
            await update.reply_text("No words found to delete")
      if update.text == "/list":
         words = ""
         for list in Config.MUTEDB.find():
             list = list.get("word")
             words = words + list + "\n"
         await update.reply_text("**Total Words : {}** \n\n{}".format(Config.MUTEDB.count_documents({}), words))
         return
    except Exception as er:
        pass
