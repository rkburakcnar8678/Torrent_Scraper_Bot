import aiohttp
import json
from pyrogram import Client, filters, emoji
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import api_hash, api_id, bot_token, ARQ_API_BASE_URL 


app = Client("torrent_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


print("\nBot Started\n")


@app.on_message(filters.command(['start']))
async def start(_, message):
    await message.reply_text("Hello I'm Torrent Scraper Bot\nSend Command 'help' To Show Help Screen, Join @TheHamkerChat For Support.")



@app.on_message(filters.command(['help']))
async def help(_, message):
    await message.reply_text("/torrent query, To Search For Torrents")

m = None
i = 0
a = None
query = None


@app.on_message(filters.command(["torrent"]))
async def torrent(_, message):
    global m
    global i
    global a
    global query
    try:
        await message.delete()
    except:
        pass
    if len(message.command) < 2:
        await message.reply_text("Usage: /torrent query")
        return
    query = message.text.split(None, 1)[1].replace(" ", "%20")
    m = await message.reply_text("Searching")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{ARQ_API_BASE_URL}torrent?query={query}") \
                    as resp:
                a = json.loads(await resp.text())
    except:
        await m.edit("Found Nothing.")
        return
    result = (
        f"**Page - {i+1}**\n\n"
        f"Name: {a[i]['name']}\n"
        f"Upload: {a[i]['uploaded']}\n"
        f"Size: {a[i]['size']}\n"
        f"Leechers: {a[i]['leechs']} "
        f"seeders: {a[i]['seeds']}\n"
        f"Magnet: `{a[i]['magnet']}`\n\n\n"
    )
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Next {emoji.RIGHT_ARROW}",
                                         callback_data="next"),
                    InlineKeyboardButton(f"Delete {emoji.CROSS_MARK}",
                                         callback_data="delete")
                ]
            ]
        ),
        parse_mode="markdown",
    )


@app.on_callback_query(filters.regex("next"))
async def callback_query_next(_, message):
    global i
    global m
    global a
    global query
    i += 1
    result = (
        f"**Page - {i+1}**\n\n"
        f"Name: {a[i]['name']}\n"
        f"Upload: {a[i]['uploaded']}\n"
        f"Size: {a[i]['size']}\n"
        f"Leechers: {a[i]['leechs']} "
        f"seeders: {a[i]['seeds']}\n"
        f"Magnet: `{a[i]['magnet']}`\n\n\n"
    )
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"{emoji.LEFT_ARROW} Previous",
                                         callback_data="previous"),
                    InlineKeyboardButton(f"Next {emoji.RIGHT_ARROW}",
                                         callback_data="next"),
                    InlineKeyboardButton(f"Delete {emoji.CROSS_MARK}",
                                         callback_data="delete")

                ]
            ]
        ),
        parse_mode="markdown",
    )


@app.on_callback_query(filters.regex("previous"))
async def callback_query_previous(_, message):
    global i
    global m
    global a
    global query
    i -= 1
    result = (
        f"**Page - {i+1}**\n\n"
        f"Name: {a[i]['name']}\n"
        f"Upload: {a[i]['uploaded']}\n"
        f"Size: {a[i]['size']}\n"
        f"Leechers: {a[i]['leechs']} "
        f"seeders: {a[i]['seeds']}\n"
        f"Magnet: `{a[i]['magnet']}`\n\n\n"
    )
    await m.edit(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"{emoji.LEFT_ARROW} Previous",
                                         callback_data="previous"),
                    InlineKeyboardButton(f"Next {emoji.RIGHT_ARROW}",
                                         callback_data="next"),
                    InlineKeyboardButton(f"Delete {emoji.CROSS_MARK}",
                                         callback_data="delete")
                ]
            ]
        ),
        parse_mode="markdown",
    )


@app.on_callback_query(filters.regex("delete"))
async def callback_query_delete(_, message):
    global m
    global i
    global a
    global query
    await m.delete()
    m = None
    i = 0
    a = None
    query = None


app.run()
