from discord.ext import commands
import discord
import datetime
from utils.logger import setup_logger

logger = setup_logger('moderation_commands')

class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"{amount} messages deleted by {ctx.author.mention}", delete_after=5)
        logger.info(f"{amount} messages deleted by {ctx.author.name} in the channel {ctx.channel.name}")

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self, ctx, member: discord.Member, *, nick):
        try:
            await member.edit(nick=nick)
            await ctx.send(f"Nickname of {member.mention} changed to `{nick}`")
            logger.info(f"Nickname of {member.name} changed to {nick} by {ctx.author.name}")
        except discord.errors.Forbidden:
            await ctx.send("I don't have the required permissions to change this user's nickname.")
            logger.warning(f"Insufficient permissions to change nickname of {member.name}")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, minutes: int, *, reason=None):
        duration = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
        try:
            await member.timeout(duration, reason=reason)
            await ctx.send(f"{member.mention} has been put in timeout for {minutes} minutes. Reason: {reason if reason else 'No reason specified'}")
            logger.info(f"User {member.name} put in timeout by {ctx.author.name} for {minutes} minutes")
        except discord.errors.Forbidden:
            await ctx.send("I don't have the required permissions to timeout this user.")
            logger.warning(f"Insufficient permissions to timeout {member.name}")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def untimeout(self, ctx, member: discord.Member):
        try:
            await member.timeout(None)
            await ctx.send(f"Timeout removed for {member.mention}")
            logger.info(f"Timeout removed for user {member.name} by {ctx.author.name}")
        except discord.errors.Forbidden:
            await ctx.send("I don't have the required permissions to remove the timeout from this user.")
            logger.warning(f"Insufficient permissions to remove timeout of {member.name}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.ban(reason=reason)
            await ctx.send(f"{member.mention} has been banned from the server. Reason: {reason if reason else 'No reason specified'}")
            logger.info(f"User {member.name} banned from the server by {ctx.author.name}")
        except discord.errors.Forbidden:
            await ctx.send("I don't have the required permissions to ban this user.")
            logger.warning(f"Insufficient permissions to ban {member.name}")

async def setup(bot):
    await bot.add_cog(ModerationCommands(bot))
