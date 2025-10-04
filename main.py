import discord
from discord.ext import commands
from music import setup_music_commands
from soundboard import setup_soundboard_commands
from recordatorios import setup_recordatorios_commands
import requests
import json
import os
from flask import Flask
from threading import Thread
import dotenv

app = Flask('')
dotenv.load_dotenv()

@app.route('/')
def home():
    return "Hello, The bot is running!"

def run_server():
    app.run(host='0.0.0.0', port=8181)

def keep_alive():
    t = Thread(target=run_server)
    t.start()


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Bot activated! {bot.user}")

@bot.command()
async def github(ctx):
    await ctx.send("https://github.com/Judi-fr/Discord_BOT")

@bot.command()
async def meme(ctx):
    response = requests.get('https://meme-api.com/gimme/dankgentina')
    json_data = json.loads(response.text)
    await ctx.send(json_data['url'])

setup_music_commands(bot)
setup_soundboard_commands(bot)
setup_recordatorios_commands(bot)

keep_alive()
bot.run(os.environ["TOKEN"])
