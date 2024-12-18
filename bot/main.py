import discord
from discord.ext import commands
import logging
from config import TOKEN
import os
from utils.init_setup import init_directories

# Intent configuration
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

# Bot initialization
bot = commands.Bot(command_prefix='!', intents=intents)

# Loading extensions
async def load_extensions():
    for folder in ['cogs', 'commands', 'events']:
        for filename in os.listdir(f'./{folder}'):
            if filename.endswith('.py') and not filename.startswith('__'):
                print(f"Loading extension: {folder}.{filename[:-3]}")
                await bot.load_extension(f'{folder}.{filename[:-3]}')
                print(f"Extension loaded: {folder}.{filename[:-3]}")

async def main():
    async with bot:
        init_directories()
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main()) 