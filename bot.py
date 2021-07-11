# Bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
from itertools import cycle

load_dotenv()
TOKEN = os.getenv('TOKEN')

client = commands.Bot(command_prefix='#')
client.remove_command('help')

@client.event
async def on_ready():
	print(f"{client.user} has connected to Discord's API")
	change_status.start()

@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send(f'Invalid command used perhaps take a look at: ''!help''?')

status = cycle(['Play.64Stacks.com', 'Minecraft: Java Edition'])

@tasks.loop(seconds=0, minutes=1, hours=0, count=None, reconnect=True, loop=None)
async def change_status():
	await client.change_presence(activity=discord.Game(next(status)))

client.cog_list = [
    "cogs.server_management",
    "cogs.user_management",
    "cogs.useful",
    "cogs.fun"
]

for cog in client.cog_list:
	client.load_extension(cog)
print(f"\nAll {len(client.cog_list)} cogs loaded!\n")

client.run(TOKEN)