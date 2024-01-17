from pyrogram import dispatcher
from info import NETWORK_USERNAME
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode

from telegram.ext import (
    CallbackContext,
    CommandHandler,
)

PHOTO = "https://graph.org/file/f6e3a9853109ff418c398.jpg"

network_name = NETWORK_USERNAME.lower()

if network_name == "Team_Netflix":
    def uchiha(update: Update, context: CallbackContext):

        TEXT = f"""
ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ [ᴛᴇᴀᴍ ɴᴇᴛғʟɪx ](https://t.me/team_netflix),
ᴛᴇᴀᴍ ɴᴇᴛғʟɪx ɪs ᴀ ɢʀᴏᴜᴘ ᴏғ ᴘᴇᴏᴘʟᴇ ᴡʜᴏ ᴀʀᴇ ᴛʀʏɪɴɢ ᴛᴏ ᴘʀᴏᴠɪᴅᴇ ᴀʟʟ ᴛʜᴇ ᴇʟᴇᴄᴛʀᴏɴɪᴄ ᴍᴇᴅɪᴀ ʙᴀsᴇᴅ ᴇɴᴛᴇʀᴛᴀɪɴᴍᴇɴᴛ sᴛᴜғғ ғʀᴇᴇ ᴏғ ᴄᴏsᴛ ᴛᴏ ᴀʟʟ ᴛʜᴏsᴇ ᴡʜᴏ ᴄᴀɴɴᴏᴛ ᴀғғᴏʀᴅ ɪᴛ, Pʟᴇᴀsᴇ ᴅᴏ sᴜᴘᴘᴏʀᴛ ᴜs ᴀɴᴅ ᴀʟsᴏ sᴜᴘᴘᴏʀᴛ ᴏᴜʀ ᴀᴅᴅ-ʙᴀsᴇᴅ ᴄᴏɴᴛᴇɴᴛ ᴀs ɪᴛ ʜᴇʟᴘs ᴜs ᴋᴇᴇᴘ ᴛʜᴇ ᴄᴏɴᴛᴇɴᴛ ғʀᴇᴇ ᴏғ ᴄᴏsᴛ.
 ᴛᴇᴀᴍ ɴᴇᴛғʟɪx ᴡᴀs ᴄʀᴇᴀᴛᴇᴅ ᴏɴ 20 December 2022..
"""

        update.effective_message.reply_photo(
            PHOTO, caption= TEXT,
            parse_mode=ParseMode.MARKDOWN,

                reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(text="sʜᴀʀᴇ & sᴜᴘᴘᴏʀᴛ", url="https://t.me/share/url?url=https%3A//t.me/Team_Netflix")],
                    [
                    InlineKeyboardButton(text="sᴇʀɪᴇs ᴀɴᴅ ᴍᴏᴠɪᴇs", url="https://t.me/Netflixe_Original/14"),
                    InlineKeyboardButton(text="ᴏᴜʀ ɢʀᴏᴜᴘs", url="https://t.me/Movie7xChat/4")
                    ],
                ]
            ),
        )


    uchiha_handler = CommandHandler(("about", "network", "net"), uchiha, run_async = True)
    dispatcher.add_handler(uchiha_handler)

    __help__ = """
    ──「ᴀʙᴏᴜᴛ • ᴛᴇᴀᴍ ɴᴇᴛғʟɪx 」──                         
    
    ❂ /about or /network: Get information about our community! Using it in groups may create promotion so we don't support using it in groups."""
    
    __mod_name__ = "ᴀʙᴏᴜᴛ"