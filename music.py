import discord
from discord.ext import commands
import yt_dlp

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

def setup_music_commands(bot):
    @bot.command()
    async def join(ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            try:
                await channel.connect()
                await ctx.send("🎵 Me conecté al canal de voz")
                print(f"✅ Conectado al canal de voz: {channel.name}")
            except Exception as e:
                await ctx.send(f"❌ Error al conectar: {str(e)}")
                print(f"❌ Error conectando al canal de voz: {e}")
        else:
            await ctx.send("❌ Tenés que estar en un canal de voz")

    @bot.command()
    async def leave(ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("👋 Me desconecté")
        else:
            await ctx.send("❌ No estoy en ningún canal")

    @bot.command()
    async def play(ctx, url: str):
        if not ctx.voice_client:  
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                try:
                    await channel.connect()
                    print(f"✅ Conectado automáticamente al canal: {channel.name}")
                except Exception as e:
                    await ctx.send(f"❌ Error al conectar al canal de voz: {str(e)}")
                    print(f"❌ Error en auto-conexión: {e}")
                    return
            else:
                await ctx.send("❌ Tenés que estar en un canal de voz")
                return

        vc = ctx.voice_client
        if vc.is_playing():
            vc.stop()

        try:
            await ctx.send("🔍 Buscando video...")
            info = ytdl.extract_info(url, download=False)
            if info is None:
                await ctx.send("❌ No pude obtener información del video")
                return

            audio_url = info["url"]
            print(f"🎵 Reproduciendo: {info['title']}")
            vc.play(discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS))  # type: ignore
            await ctx.send(f"▶️ Reproduciendo: **{info['title']}**")
        except Exception as e:
            error_msg = str(e)
            await ctx.send(f"❌ Error al reproducir: {error_msg}")
            print(f"❌ Error detallado en music.py: {error_msg}")
            print(f"   URL: {url}")
            import traceback
            traceback.print_exc()

    @bot.command()
    async def stop(ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("⏹️ Música detenida")
        else:
            await ctx.send("❌ No estoy reproduciendo nada")
