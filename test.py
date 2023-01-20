import discord,asyncio,os
from discord.ext import commands, tasks

channel_id = 1065374297515884637
botDescription="Bot"
intents = discord.Intents.all()
token = "MTA2NTM3MjI2NTc2MTQ4MDcwNA.GAvOjb.dlKaj_tvRnqYOsyHynBMApnIt3ZUYVOxnmeeVc"
bot = commands.Bot(command_prefix="?", help_command=None, description=botDescription, intents=intents)

@bot.event
async  def on_ready():
    change_status.start()
    print('bot in active')

@tasks.loop(seconds=5)
async def change_status():
    channel = bot.get_channel(channel_id)
    #await bot.change_presence(activity=discord.Game('online'))
    print('test')
    #await channel.send('here')
bot.run(token)