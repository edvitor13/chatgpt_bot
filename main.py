import os

from discord import Intents
from chatgpt_bot.bot import Bot


client = Bot(intents=Intents.all())
client.run(os.environ['CHATGPT_BOT_TOKEN'])
