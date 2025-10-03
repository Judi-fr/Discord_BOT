# Overview

This is a Discord bot built with Python that provides entertainment and utility features. The bot supports music playback from YouTube (requires UDP - works outside Replit), soundboard with short audio clips, reminders with timers, meme generation, and basic commands. It uses Discord.py for bot functionality, yt-dlp for audio streaming, and file-based storage for reminders.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Bot Framework
- **Technology**: Discord.py with commands extension
- **Rationale**: Standard Discord.py bot with decorator-based command registration
- **Authentication**: Uses environment variable `TOKEN` for Discord bot token
- **Intents**: Message content intent enabled to read command messages
- **Web Server**: Flask server on port 8181 for keep-alive functionality

## Command System
- **Pattern**: Command-based architecture using prefix `!`
- **Implementation**: Commands registered through decorators `@bot.command()`
- **Types supported**:
  - Static string responses (e.g., `!github`)
  - Function-based responses (e.g., `!meme`)
  - Async context-aware handlers for Discord interactions
  - Timed reminders with persistence
  - Soundboard audio clips

## Music Playback Architecture (Requires UDP - Not available on Replit)
- **Audio Source**: YouTube videos via yt-dlp
- **Streaming Strategy**: Direct audio URL extraction without downloading
- **Audio Processing**: FFmpeg for audio codec handling and streaming
- **Connection Management**: 
  - Bot joins user's current voice channel
  - Single active stream (stops previous if playing)
  - Manual disconnect command available
- **Limitation**: UDP connections required for voice - blocked on Replit, works on local/VPS hosting

## Soundboard System
- **Location**: `soundboard.py`
- **Audio Files**: Stored in `sounds/` directory
- **Supported Sounds**: bruh, vine, wtf, error, airhorn (configurable)
- **Commands**: 
  - `!sounds` - List available sounds
  - `!play_sound <name>` - Play a sound
- **Limitation**: Requires voice connection (UDP) - blocked on Replit

## Reminders System
- **Location**: `recordatorios.py`
- **Storage**: JSON file (`recordatorios.json`) for persistence
- **Time Formats**: s (seconds), m (minutes), h (hours), d (days)
- **Commands**:
  - `!recordar <time> <message>` - Create reminder
  - `!mis_recordatorios` - View active reminders
  - `!borrar_recordatorios` - Delete all your reminders
- **Background Task**: Checks every 10 seconds for due reminders

## Meme Generation
- **API**: meme-api.com (Spanish meme subreddit /r/MemesESP)
- **Approach**: Direct HTTP request to public endpoint
- **Response**: Returns image URL for Discord to embed

# File Structure

```
├── main.py              # Main bot entry point, command setup
├── music.py             # Music playback commands (YouTube)
├── soundboard.py        # Soundboard audio clips
├── recordatorios.py     # Reminder system with persistence
├── sounds/              # Directory for audio files
│   └── README.txt
├── recordatorios.json   # Reminders storage (auto-generated)
└── replit.md           # This documentation
```

# External Dependencies

## Core Libraries
- **discord.py**: Discord API wrapper for bot functionality
- **yt-dlp**: YouTube video/audio extraction and streaming
- **requests**: HTTP client for external API calls
- **python-dateutil**: Date/time utilities for reminders
- **flask**: Web server for keep-alive

## External APIs
- **Discord API**: Bot communication platform (requires bot token)
- **meme-api.com**: Meme image provider (no authentication)
- **YouTube**: Audio content source (accessed via yt-dlp)

## System Dependencies
- **FFmpeg**: Audio processing and streaming (installed via Nix)
- **Environment Variables**: 
  - `TOKEN`: Discord bot authentication token

# Available Commands

## General Commands
- `!github` - Share GitHub link
- `!meme` - Get a random Spanish meme

## Music Commands (requires voice connection - limited on Replit)
- `!join` - Join your voice channel
- `!leave` - Leave voice channel
- `!play <url>` - Play YouTube audio
- `!stop` - Stop current playback

## Soundboard Commands (requires voice connection - limited on Replit)
- `!sounds` - List available sounds
- `!play_sound <name>` - Play a sound effect

## Reminder Commands
- `!recordar <time> <message>` - Set a reminder (e.g., `!recordar 10m take a break`)
- `!mis_recordatorios` - View your active reminders
- `!borrar_recordatorios` - Delete all your reminders

# Known Limitations

- **Voice Features on Replit**: Music playback and soundboard require UDP connections which are blocked on Replit's infrastructure. These features work when hosting the bot locally or on a VPS.
- **Audio File Storage**: Soundboard audio files must be manually added to the `sounds/` directory
- **Reminder Persistence**: Reminders survive bot restarts via JSON file storage
