from discord_easy_commands import discord
import yt_dlp

# Configuración YT-DLP
ytdl_opts = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
}
ytdl = yt_dlp.YoutubeDL(ytdl_opts)

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

# 🎵 Entrar al canal de voz
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("🎵 Me conecté al canal de voz")
    else:
        await ctx.send("❌ Tenés que estar en un canal de voz")

# 🎵 Salir del canal
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Me desconecté")
    else:
        await ctx.send("❌ No estoy en ningún canal")

# 🎵 Reproducir música
async def play(ctx, url: str):
    if not ctx.voice_client:  
        await join(ctx)

    vc = ctx.voice_client
    if vc.is_playing():
        vc.stop()

    info = ytdl.extract_info(url, download=False)
    audio_url = info["url"]

    vc.play(discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS))
    await ctx.send(f"▶️ Reproduciendo: **{info['title']}**")

# 🎵 Detener música
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏹️ Música detenida")
    else:
        await ctx.send("❌ No estoy reproduciendo nada")
