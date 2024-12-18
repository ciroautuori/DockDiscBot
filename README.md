# Bob Marrano - Multifunctional Discord Bot

A robust, feature-rich Discord bot built with Python, featuring music playback, leveling system, moderation tools, and utility commands. Built with modularity and scalability in mind.

## Features

### 🎵 Music System

- Play music from YouTube
- Queue management
- Basic playback controls
- Auto-disconnect when inactive

### ⭐ Leveling System

- Experience (XP) tracking
- Automatic role assignments
- Level progress visualization
- Custom level-up messages

### 🛡️ Moderation Tools

- Message management
- User timeout control
- Nickname management
- Ban functionality

### 🤖 General Commands

- Server information
- User profiles
- Avatar display
- Latency checking

## Command List

### Music Commands

- `!play <url>` - Play a song from YouTube
- `!pause` - Pause current playback
- `!resume` - Resume playback
- `!skip` - Skip current song
- `!stop` - Stop playback and clear queue
- `!queue` - Display current queue

### Level Commands

- `!level [user]` - Display user's level and XP
- `!reset_level <user>` - Reset user's level (Admin only)

### Moderation Commands

- `!clear <number>` - Delete specified number of messages
- `!timeout <user> <minutes> [reason]` - Timeout user
- `!untimeout <user>` - Remove user's timeout
- `!ban <user> [reason]` - Ban user from server

### Utility Commands

- `!ping` - Check bot latency
- `!info [user]` - Display user information
- `!avatar [user]` - Show user's avatar

## Installation

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Discord Bot Token
- FFmpeg

### Quick Start

1. Clone the repository:

```bash
git clone https://github.com/yourusername/bob-marrano-bot.git
cd bob-marrano-bot
```

2. Configure environment variables:
   - Copy `docker/.env.example` to `docker/.env`
   - Fill in your Discord bot token and other required values

3. Start the bot:

```bash
chmod +x start.sh
./start.sh
```

### Manual Installation

1. Install dependencies:

```bash
pip install -r bot/requirements.txt
```

2. Configure environment variables in `docker/.env`:

```env
DISCORD_TOKEN=your_token_here
WELCOME_CHANNEL=channel_id_here
RULES_CHANNEL=channel_id_here
MEMBER_ROLE_NAME=role_name_here 
```

3. Run with Docker:

```bash
docker-compose -f docker/docker-compose.yml up --build
```

## Project Structure

```
.
├── bot/
│   ├── cogs/          # Feature modules
│   ├── commands/      # Command handlers
│   ├── database/      # Database operations
│   ├── events/        # Event handlers
│   └── utils/         # Utility functions
└── docker/           # Docker configuration
```

## Development

### Adding New Features

1. Create a new module in the appropriate directory
2. Implement the feature using the existing patterns
3. Register the module in `main.py`

### Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Troubleshooting

### Common Issues

- **Bot not responding**: Check your Discord token
- **Music not playing**: Verify FFmpeg installation
- **Database errors**: Check write permissions in data directory

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [discord.py](https://github.com/Rapptz/discord.py)
- Music playback powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Support

For support, questions, or feature requests, please open an issue on GitHub.
