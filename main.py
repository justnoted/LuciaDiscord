import os
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
client = commands.Bot(command_prefix=[], help_command=None, intents=intents)

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    await client.tree.sync()
    print(f"{client.user.name} has connected to Discord ({client.user.id}).")

async def main():
    async with client:
        await load()
        await client.start(os.getenv('DISCORD_TOKEN'))

if __name__ == '__main__':
    asyncio.run(main())