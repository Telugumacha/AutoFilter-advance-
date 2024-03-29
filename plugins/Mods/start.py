# Copyright 2023 Qewertyy, MIT License

from pyrogram import Client, filters, types as t
from bott import StartTime

startText = """
Just an AI/Utility bot by `@VeldXd`.
Commands:
`/draw`: create images
`/upscale`: upscale your images
`/gpt`: chatgpt
`/bard`: bard ai by google
`/mistral`: mistral ai
`/llama`: llama by meta ai
`/palm`: palm by google
`/reverse`: reverse image search
`/gemini`: gemini by google
"""

@Client.on_message(filters.command(["ai","aihelp","repo","source"]))
async def aihelp(_: Client, m: t.Message):
    await m.reply_text(
        startText,
        reply_markup=t.InlineKeyboardMarkup(
            [
                [
                    t.InlineKeyboardButton(text="ᴍʏ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ",url="https://t.me/codeflix_bots")
                ]
            ]
        )
    )
