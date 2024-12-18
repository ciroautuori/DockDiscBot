from discord.ext import commands
import discord
import yt_dlp
from collections import deque
import asyncio
from utils.logger import setup_logger
from utils.helpers import join_voice_channel
from config import YTDL_FORMAT_OPTIONS, FFMPEG_OPTIONS

logger = setup_logger('music')

class VoiceEntry:
    def __init__(self, message, url, audio_source, title):
        self.requester = message.author
        self.channel = message.channel
        self.url = url
        self.audio_source = audio_source
        self.title = title

    def __str__(self):
        return f'**{self.title}** requested by {self.requester.name}'

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music_queue = {}
        self.playing_now = {}
        self.ytdl = yt_dlp.YoutubeDL(YTDL_FORMAT_OPTIONS)

    async def queue_song(self, ctx, url):
        """Adds a song to the queue and downloads it if not already downloaded"""
        try:
            with yt_dlp.YoutubeDL(YTDL_FORMAT_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info:
                    info = info['entries'][0]
                url = info['url']
                title = info['title']
                audio_source = discord.PCMVolumeTransformer(
                    discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS),
                    volume=0.5
                )
                song = VoiceEntry(ctx.message, url, audio_source, title)

                guild_id = ctx.guild.id
                if guild_id not in self.music_queue:
                    self.music_queue[guild_id] = deque()
                self.music_queue[guild_id].append(song)
                await ctx.send(f'Added to queue: {title}')
                logger.info(f"Added song {title} to queue in server {guild_id}")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
            logger.error(f"Error while adding song to queue: {e}")

    async def play_next(self, ctx):
        """Plays the next song in queue."""
        guild_id = ctx.guild.id
        if guild_id in self.music_queue and self.music_queue[guild_id]:
            try:
                song = self.music_queue[guild_id].popleft()
                ctx.voice_client.play(
                    song.audio_source, 
                    after=lambda error: self.bot.loop.create_task(self.play_next(ctx))
                )
                self.playing_now[guild_id] = song
                await ctx.send(f'Now playing: {song.title} requested by {song.requester.mention}')
                logger.info(f"Playing song {song.title} in server {guild_id}")
            except Exception as e:
                await ctx.send(f"Error during playback: {e}")
                logger.error(f"Error during playback: {e}")
        else:
            self.playing_now[guild_id] = None
            await ctx.send("Queue ended.")
            logger.info(f"Music queue ended in server {guild_id}")
            if ctx.voice_client:
                await asyncio.sleep(10)
                if not self.music_queue.get(guild_id) and not ctx.voice_client.is_playing():
                    await ctx.voice_client.disconnect()
                    await ctx.send("Disconnected from voice channel due to inactivity")
                    logger.info(f"Disconnected from voice channel in server {guild_id} due to inactivity")

    async def play_song(self, ctx, url):
        """Handles song playback."""
        if not await join_voice_channel(ctx):
            return

        try:
            voice_client = ctx.voice_client
            if voice_client.is_playing() or voice_client.is_paused():
                await self.queue_song(ctx, url)
                return

            await self.queue_song(ctx, url)
            await self.play_next(ctx)
        except Exception as e:
            await ctx.send(f'An error occurred: {e}')
            logger.error(f"Error during play command: {e}")

    async def pause_song(self, ctx):
        """Pauses the playback."""
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await ctx.send("Playback paused")
            logger.info(f"Playback paused in server {ctx.guild.id}")

    async def resume_song(self, ctx):
        """Resumes the playback."""
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await ctx.send("Playback resumed")
            logger.info(f"Playback resumed in server {ctx.guild.id}")

    async def skip_song(self, ctx):
        """Skips the current song."""
        if not ctx.voice_client or not ctx.voice_client.is_connected():
            await ctx.send("I'm not in a voice channel.")
            return
        ctx.voice_client.stop()
        await ctx.send("Song skipped")
        logger.info(f"Song skipped in server {ctx.guild.id}")

    async def stop_music(self, ctx):
        """Stops playback and disconnects the bot."""
        voice_client = ctx.voice_client
        guild_id = ctx.guild.id
        if voice_client and voice_client.is_connected():
            voice_client.stop()
            await voice_client.disconnect()
            if guild_id in self.music_queue:
                self.music_queue[guild_id].clear()
            if guild_id in self.playing_now:
                self.playing_now[guild_id] = None
            await ctx.send("Playback stopped and disconnected from channel")
            logger.info(f"Bot disconnected from voice channel in server {guild_id}")

    async def show_queue(self, ctx):
        """Shows the playback queue."""
        guild_id = ctx.guild.id
        if guild_id in self.music_queue and self.music_queue[guild_id]:
            queue_list = [f"{i+1}. {str(song)}" for i, song in enumerate(self.music_queue[guild_id])]
            embed = discord.Embed(
                title="Server playback queue",
                description="\n".join(queue_list),
                color=discord.Color.blue()
            )
            if guild_id in self.playing_now and self.playing_now[guild_id] is not None:
                embed.add_field(
                    name="Now playing",
                    value=str(self.playing_now[guild_id]),
                    inline=False
                )
            await ctx.send(embed=embed)
            logger.info(f"Showed playback queue in server {guild_id}")
        else:
            await ctx.send("The playback queue is empty.")

    async def show_current(self, ctx):
        """Shows the currently playing song."""
        guild_id = ctx.guild.id
        if guild_id in self.playing_now and self.playing_now[guild_id]:
            await ctx.send(f"Now playing: {str(self.playing_now[guild_id])}")
            logger.info(f"Showed current song in server {guild_id}")
        else:
            await ctx.send("No song currently playing.")

async def setup(bot):
    await bot.add_cog(Music(bot))
