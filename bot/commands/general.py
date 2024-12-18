from discord.ext import commands
import discord
from utils.logger import setup_logger

logger = setup_logger('general_commands')

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        latency = self.bot.latency * 1000
        await ctx.send(f'Pong! Latency: {latency:.2f}ms')
        logger.info(f"Ping command invoked by {ctx.author.name}, latency: {latency:.2f}ms")

    @commands.command()
    async def info(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"Info for {member.name}", color=discord.Color.blue())
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Name", value=member.name, inline=False)
        embed.add_field(name="Tag", value=member.discriminator, inline=False)
        embed.add_field(name="Nickname", value=member.nick if member.nick else "None", inline=False)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Server Join Date", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        await ctx.send(embed=embed)
        logger.info(f"Info command invoked by {ctx.author.name} for user {member.name}")

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"Avatar of {member.name}", color=discord.Color.blue())
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)
        logger.info(f"Avatar command invoked by {ctx.author.name} for user {member.name}")

async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))
