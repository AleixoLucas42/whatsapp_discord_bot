import os
import discord
from discord.ext import commands
import requests
import json
import time

wpp_url = "http://whatsapp:3000/client/sendMessage/DISC_WPP_SESSION"
chat_id = os.environ["CHAT_ID"]
token = os.environ["DISC_TOKEN"]
bot_status_working = False
last_notification_time = {}

def send_wpp_notification(content):
    payload = json.dumps({
        "chatId": chat_id,
        "contentType": "string",
        "content": content
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", wpp_url, headers=headers, data=payload, verify=False)

    if response.status_code == 200:
        print("[+] whatsapp message sent")
    else:
        print(f"[!] error {response.status_code} sending message\n")
        print(response.text)

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
            guild_name = after.channel.guild.name
            print(f"[+] {member.name} connected to voice channel {channel_name}")

            if member.id not in last_notification_time or time.time() - last_notification_time[member.id] > 30:
                send_wpp_notification(f"{member.name} on: {channel_name}")
                last_notification_time[member.id] = time.time()

if __name__ == '__main__':
    while (bot_status_working is not True):
        time.sleep(10)
        print("[*] trying to wake up bot")
        if (send_wpp_notification("✅ bot is awake")):
            bot_status_working = True
    print("[*] bot waked up")
    bot.run(token)