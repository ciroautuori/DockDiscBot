from discord.ext import commands
import discord
from utils.logger import setup_logger
from database.database import DatabaseHandler
from utils.helpers import calculate_next_level_xp

logger = setup_logger('levels_commands')
db = DatabaseHandler()

class LevelCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        try:
            result = db.get_user_level(member.id)
            if result:
                xp, level = result
                next_level_xp = calculate_next_level_xp(level)
                embed = discord.Embed(title=f"Level of {member.name}", color=discord.Color.blue())
                embed.add_field(name="Level", value=level, inline=False)
                embed.add_field(name="Experience", value=f"{xp}/{next_level_xp}", inline=False)
                embed.add_field(name="Next level in", value=f"{next_level_xp - xp} XP", inline=False)
                await ctx.send(embed=embed)
                logger.info(f"Level command invoked by {ctx.author.name} for user {member.name}")
            else:
                await ctx.send(f"{member.mention} hasn't started their adventure yet!")
                logger.info(f"Level command invoked for unregistered user: {member.name}")
        except Exception as e:
            logger.error(f"Error while reading level for {member.name}: {e}")
            await ctx.send("An error occurred while reading the level.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reset_level(self, ctx, member: discord.Member):
        try:
            db.update_user_xp(member.id, 0, 1)
            await ctx.send(f"Level of {member.mention} reset to 1")
            logger.info(f"Level of {member.name} reset by {ctx.author.name}")
        except Exception as e:
            logger.error(f"Error during level reset for {member.name}: {e}")
            await ctx.send("An error occurred while resetting the level.")

async def setup(bot):
    await bot.add_cog(LevelCommands(bot))
