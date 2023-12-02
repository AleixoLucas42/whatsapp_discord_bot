import os
import discord
from discord.ext import commands
import requests
import json

wpp_url = "http://whatsapp:3000/client/sendMessage/DISC_WPP_SESSION"
chat_id = os.environ["CHAT_ID"]
token = os.environ["DISC_TOKEN"]

def send_wpp_notification(content):
    payload = json.dumps({
        "chatId": chat_id,
        "contentType": "string",
        "content": content
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", wpp_url, headers=headers, data=payload)

    if response.status_code == 200:
        print("Enviado notificação no whatsapp")
    else:
        print(f"Erro {response.status_code} ao enviar a notificação\n")
        print(response.text)

intents = discord.Intents.all()
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:
        if after.channel is not None:
            channel_name = after.channel.name
            guild_name = after.channel.guild.name
            print(f"Usuário {member.name} se conectou ao canal de voz {channel_name}")
            send_wpp_notification(f"Usuário {member.name} se conectou ao canal de voz {channel_name}")

bot.run(token)
