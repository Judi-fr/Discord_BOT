from discord import Intents
from discord_easy_commands import EasyBot, discord
import requests
import json
import os


def get_meme():
  response = requests.get('https://meme-api.com/gimme/MemesESP')
  json_data = json.loads(response.text)
  return json_data['url']


intents = discord.Intents.default()
intents.message_content = True

bot = EasyBot(intents=intents)

bot.setCommand("!github", "https://github.com/")
bot.setCommand("!meme", get_meme())

bot.run(os.environ["TOKEN"])