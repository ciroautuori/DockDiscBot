from discord.ext import commands
import discord
from utils.logger import setup_logger
from database.database import DatabaseHandler
from utils.helpers import calculate_next_level_xp, clear_user_roles

logger = setup_logger('levels_cog')
db = DatabaseHandler()

class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = message.author.id
        xp_to_add = 5

        try:
            result = db.get_user_level(user_id)
            
            if result:
                xp, level = result
                xp += xp_to_add
                next_level_xp = calculate_next_level_xp(level)

                if xp >= next_level_xp:
                    level += 1
                    role = discord.utils.get(message.guild.roles, name=f"Level {level}")
                    if role:
                        await clear_user_roles(message.author, level)
                        await message.author.add_roles(role)
                        await message.channel.send(
                            f"Congratulations {message.author.mention}! "
                            f"You've reached level {level}!"
                        )
                        logger.info(f"User {message.author.name} leveled up to {level}")
                
                db.update_user_xp(user_id, xp, level)
            else:
                db.add_new_user(user_id, xp_to_add)
                logger.info(f"New user {message.author.name} added to the database.")

        except Exception as e:
            logger.error(f"Error during xp update for {message.author.name}: {e}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            if not db.get_user_level(member.id):
                db.add_new_user(member.id)
                logger.info(f"New member {member.name} added to the level database")
        except Exception as e:
            logger.error(f"Error during new member addition to the database: {e}")

async def setup(bot):
    await bot.add_cog(LevelSystem(bot))
