from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputStream, AudioPiped
from youtube_dl import YoutubeDL
import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

app = Client("music_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
vc = PyTgCalls(app)

ydl_opts = {
    'format': 'bestaudio',
    'quiet': True,
    'extract_flat': 'in_playlist',
}

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("🎵 Welcome to the Telegram Music Bot!")

@app.on_message(filters.command("play"))
async def play(_, msg):
    query = " ".join(msg.command[1:])
    if not query:
        return await msg.reply("❗ Please provide a song name or link.")

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        url = info['url']
        await vc.join_group_call(
            msg.chat.id,
            InputStream(
                AudioPiped(url),
            )
        )
        await msg.reply(f"▶️ Playing: {info['title']}")

@app.on_message(filters.command("pause"))
async def pause(_, msg):
    await vc.pause_stream(msg.chat.id)
    await msg.reply("⏸ Paused.")

@app.on_message(filters.command("resume"))
async def resume(_, msg):
    await vc.resume_stream(msg.chat.id)
    await msg.reply("▶️ Resumed.")

@app.on_message(filters.command("stop"))
async def stop(_, msg):
    await vc.leave_group_call(msg.chat.id)
    await msg.reply("🛑 Stopped music and left VC.")

app.start()
vc.start()
print("Bot is running...")
app.idle()
