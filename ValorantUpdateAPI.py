import discord
from datetime import datetime
from discord.ext import commands, tasks
from time import sleep
import requests
from pprint import pprint
import json
import pymongo
from pymongo import MongoClient
import os
import random

botDescription="Bot"
intents = discord.Intents.all()
client = commands.Bot(command_prefix="?", help_command=None, description=botDescription, intents=intents)
delay = 82800
CurrentgameVersion = 0
pingedVersion = 0

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
channel_id = int(os.getenv('channel_id'))


users = ['@El Dani','@EL Mr.Valo','@El Gi0hno','@El Braulio']

try:
    URI = os.getenv('URI')
    mongoClient = MongoClient(URI)
    db = mongoClient.ApiCalls
    collection = db.ValorantPatchVersion
    print('Conected to db sucesfully')
except:
    print('Conection failed')



def getCurrentVersion():
        data = collection.find_one(sort = [("_id", -1)])
        return data['data']['version']


def pingAPI():

    ###Gets current game version stored in the database
    print('Getting current version from database...')
    CurrentgameVersion = getCurrentVersion()
    pprint('Current Game version found in database = ' + CurrentgameVersion)
    ###


    print('pingin to check Game Version...')
    response = requests.get('https://valorant-api.com/v1/version')
    res_json = response.json()
    print(res_json)
    pingedVersion = res_json['data']['version']
    pprint('Pinged version = ' + pingedVersion)

    ####### Get data from file for testing
    # f = open('data.json')
    # data = json.load(f)
    # pingedVersion = data['data']['version']
    # pprint('Version found on api = ' + pingedVersion)
    # f.close()
    #######

    #current_time = datetime.now().strftime("%H:%M")#hour %H min %M sec %S am:pm %p 
    
    if pingedVersion != CurrentgameVersion: # enter the time you wish 
        print("Update found, bot will proceed to send msg")
        collection.insert_one(res_json)
        return True
    else:
        print('No update found, pinging again in x seconds')
        return False
            

#Program start

@client.event
async def on_ready():
    print('bot is active')
    change_status.start()


@tasks.loop(seconds=30)
async def change_status():
    isThereUpdate = pingAPI()
    if isThereUpdate:
        print("bot:user ready == {0.user}".format(client))
        channel = client.get_channel(channel_id)
        await channel.send('Hay update malditos malcriados @everyone')

    

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!va'):
        await message.channel.send('Orale pinches jotos vamos a juegar @everyone')
    
    if message.content.startswith('!gei'):
        await message.channel.send(f'Definitivamente eres el mas gei aqui {users[random.randint(0,3)]}')


client.run(TOKEN)



