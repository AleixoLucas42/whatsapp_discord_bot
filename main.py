import os
import discord
from discord.ext import commands
import aiohttp
import json
import time
import asyncio

wpp_url = "http://whatsapp:3000/client/sendMessage/DISC_WPP_SESSION"
chat_id = os.environ["CHAT_ID"]
token = os.environ["DISC_TOKEN"]
last_notification_time = {}

async def send_wpp_notification(content):
    payload = json.dumps({
        "chatId": chat_id,
        "contentType": "string",
        "content": content
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(wpp_url, headers=headers, data=payload, ssl=False, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    print("[+] whatsapp message sent")
                else:
                    print(f"[!] error {response.status} sending message")
                    print(await response.text())
    except asyncio.TimeoutError:
        print("[!] Timeout sending whatsapp message")
    except Exception as e:
        print(f"[!] Exception sending whatsapp message: {e}")

intents = discord.Intents.all()
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'[*] bot connected as {bot.user.name}')

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:
        if after.channel is not None:
            channel_name = after.channel.name
            print(f"[+] {member.name} connected to voice channel {channel_name}")

            now = time.time()
            if member.id not in last_notification_time or now - last_notification_time[member.id] > 30:
                await send_wpp_notification(f"{member.name} on: {channel_name}")
                last_notification_time[member.id] = now

if __name__ == '__main__':
    bot.run(token)

