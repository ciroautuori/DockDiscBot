import discord
import logging
from typing import Optional

async def get_voice_channel(ctx):
    if not ctx.author.voice:
        await ctx.send("You're not in a voice channel.")
        return None
    return ctx.author.voice.channel

async def join_voice_channel(ctx):
    voice_channel = await get_voice_channel(ctx)
    if not voice_channel:
        return False

    if ctx.voice_client is None:
        try:
            await voice_channel.connect()
        except discord.ClientException as e:
            await ctx.send(f"Cannot connect to voice channel: {e}")
            return False
    elif ctx.voice_client.channel != voice_channel:
        try:
            await ctx.voice_client.move_to(voice_channel)
        except discord.ClientException as e:
            await ctx.send(f"Cannot move to voice channel: {e}")
            return False
    return True

async def clear_user_roles(member: discord.Member, level: int):
    """Removes all lower level roles from the specified member."""
    roles_to_remove = []
    for i in range(1, level):
        role_name = f"Level {i}"
        role = discord.utils.get(member.guild.roles, name=role_name)
        if role:
            roles_to_remove.append(role)
    if roles_to_remove:
        try:
            await member.remove_roles(*roles_to_remove)
        except discord.errors.Forbidden:
            logging.error(f"Insufficient permissions to remove roles from {member.name}.")
        except Exception as e:
            logging.error(f"Error while removing roles from {member.name}: {e}")

def calculate_next_level_xp(level: int) -> int:
    return 100 + (level * 50)
