# © @TheAltron

import asyncio

from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, ChatAdminRequired, UserNotParticipant, ChatWriteForbidden

MUST_JOIN = "TheAltron"

JOIN_MESSAGE = f"""**Please Join My Updates Channel to use this Bot!**

Due to Telegram Users Traffic, Only Channel Subscribers can use the Bot!
"""

STATS_PHOTO = "https://te.legra.ph/file/04e8f8e6bbf74c54f3f9d.jpg"


# MUST JOIN TO A CHAT
async def must_join(client: Client, message: Message, MUST_JOIN: str = MUST_JOIN):
    """
    Parameters:
        client (:obj:`~pyrogram.Client`)
        
        message (:obj:`~pyrogram.types.Message`)

        MUST_JOIN (``str``, *optional*)
    """

    try:
        await client.get_chat_member(MUST_JOIN, message.from_user.id)
    except UserNotParticipant:
        if MUST_JOIN.isalpha():
            link = "https://t.me/" + MUST_JOIN
        else:
            chat_info = await client.get_chat(MUST_JOIN)
            link = chat_info.invite_link
        try:
            await message.reply(
                JOIN_MESSAGE,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✘ ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ", url=link)]
                ]),
            )
            await message.stop_propagation()
        except ChatWriteForbidden:
            pass
    except ChatAdminRequired:
        print(f"I'm not admin in the MUST_JOIN chat : {MUST_JOIN} !")


# STATS OF THE BOT
async def stats(client: Client, message: Message, stats_text, stats_photo=STATS_PHOTO):
    """
    Parameters:
        client (:obj:`~pyrogram.Client`)
        
        message (:obj:`~pyrogram.types.Message`)

        stats_text (``str``):
            The text which will be sended.

        stats_photo (``str``, *optional*):
            Link of that photo, which will be sended.
    """

    await client.send_photo(chat_id=message.chat.id, 
        photo=stats_photo,
        caption=stats_text
    )


# GLOBAL CAST
async def gcast(client: Client, message: Message, user_ids: list):
    """
    Parameters:
        client (:obj:`~pyrogram.Client`)
        
        message (:obj:`~pyrogram.types.Message`)

        user_ids (``list``):
            List of the Chat-Ids, in which the Broadcast Message will be sended.
    """

    if message.reply_to_message:
        m = message.reply_to_message_id
        p = message.chat.id
    else:
        query = message.text.split(" ", 1)
        if len(query) == 1:
            await message.reply_text(f"𝗨𝘀𝗮𝗴𝗲:\n » /gcast [MESSAGE] ᴏʀ [Reply to a Message]")
            return
        gcast_msg = query[1]

    alt = 0
    for uid in user_ids:
        try:
            if message.reply_to_message:
                await client.forward_messages(uid, p, m)
            else:
                await client.send_message(uid, text=gcast_msg)
            alt += 1
            await asyncio.sleep(0.3)
        except FloodWait as e:
            flood_time = int(e.x)
            await asyncio.sleep(flood_time)
        except Exception:
            pass
    try:
        await message.reply_text(f"**» ʙʀᴏᴀᴅᴄᴀꜱᴛᴇᴅ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ {alt} ᴄʜᴀᴛꜱ.**")
    except:
        pass
