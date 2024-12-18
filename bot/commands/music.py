from discord.ext import commands
import discord
from utils.logger import setup_logger
from utils.helpers import join_voice_channel

logger = setup_logger('music_commands')

class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music_cog = None
        print("MusicCommands initialized")

    async def get_music_cog(self):
        if not self.music_cog:
            self.music_cog = self.bot.get_cog('Music')
        return self.music_cog

    @commands.command()
    async def join(self, ctx):
        """Joins the user's voice channel."""
        if await join_voice_channel(ctx):
            await ctx.send("Joined voice channel")
            logger.info(f"Bot joined voice channel in server {ctx.guild.id}")
        else:
            await ctx.send("Music system not available")
            logger.error("Music cog not found")

    @commands.command()
    async def play(self, ctx, *, url):
        """Plays a song from the specified URL."""
        music = await self.get_music_cog()
        if music:
            await music.play_song(ctx, url)
        else:
            await ctx.send("Music system not available")
            logger.error("Music cog not found")

    @commands.command()
    async def pause(self, ctx):
        """Pauses the playback."""
        music = await self.get_music_cog()
        if music:
            await music.pause_song(ctx)
        else:
            await ctx.send("Music system not available")

    @commands.command()
    async def resume(self, ctx):
        """Resumes the playback."""
        music = await self.get_music_cog()
        if music:
            await music.resume_song(ctx)
        else:
            await ctx.send("Music system not available")

    @commands.command()
    async def skip(self, ctx):
        """Skips the current song."""
        music = await self.get_music_cog()
        if music:
            await music.skip_song(ctx)
        else:
            await ctx.send("Music system not available")

    @commands.command()
    async def stop(self, ctx):
        """Stops playback and disconnects the bot."""
        music = await self.get_music_cog()
        if music:
            await music.stop_music(ctx)
        else:
            await ctx.send("Music system not available")

    @commands.command()
    async def queue(self, ctx):
        """Shows the playback queue."""
        music = await self.get_music_cog()
        if music:
            await music.show_queue(ctx)
        else:
            await ctx.send("Music system not available")

    @commands.command()
    async def current(self, ctx):
        """Shows the currently playing song."""
        music = await self.get_music_cog()
        if music:
            await music.show_current(ctx)
        else:
            await ctx.send("Music system not available")

    @commands.command()
    async def musictest(self, ctx):
        """Tests if music commands are active."""
        await ctx.send("Music commands are active!")
        logger.info(f"Music command test executed by {ctx.author.name}")

async def setup(bot):
    await bot.add_cog(MusicCommands(bot))
