import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
TOKEN = os.getenv('DISCORD_TOKEN')
WELCOME_CHANNEL_ID = int(os.getenv('WELCOME_CHANNEL'))
RULES_CHANNEL_ID = int(os.getenv('RULES_CHANNEL'))
MEMBER_ROLE_NAME = os.getenv("MEMBER_ROLE_NAME")

# yt-dlp Configuration
YTDL_FORMAT_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'no_check_certificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'prefer_insecure': True
}

FFMPEG_OPTIONS = {
    'options': '-vn'
}

# Database Configuration
DATABASE_PATH = 'data/levels.db'
