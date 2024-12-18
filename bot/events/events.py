from discord.ext import commands
import discord
from utils.logger import setup_logger
from utils.helpers import clear_user_roles, calculate_next_level_xp
from database.database import DatabaseHandler
from config import WELCOME_CHANNEL_ID, RULES_CHANNEL_ID, MEMBER_ROLE_NAME

logger = setup_logger('events')
db = DatabaseHandler()

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'Bot connected as {self.bot.user.name}')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        rules_channel = self.bot.get_channel(RULES_CHANNEL_ID)
        await channel.send(
            f'Welcome {member.mention}! Please read the rules in '
            f'{rules_channel.mention} before starting to interact in the server!'
        )
        role = discord.utils.get(member.guild.roles, name=MEMBER_ROLE_NAME)
        await member.add_roles(role)
        logger.info(f"User {member.name} joined the server, role assigned: {role}")

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
            logger.error(f"Error during XP update for {message.author.name}: {e}")

async def setup(bot):
    await bot.add_cog(Events(bot))
