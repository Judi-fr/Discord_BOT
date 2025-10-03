import discord
from discord.ext import commands
import os

SOUND_FILES = {
    "bruh": "sounds/bruh.mp3",
    "vine": "sounds/vine_boom.mp3",
    "wtf": "sounds/wtf.mp3",
    "error": "sounds/windows_error.mp3",
    "airhorn": "sounds/airhorn.mp3",
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

def setup_soundboard_commands(bot):
    @bot.command()
    async def sounds(ctx):
        """Muestra la lista de sonidos disponibles"""
        sound_list = ", ".join(f"`{sound}`" for sound in SOUND_FILES.keys())
        await ctx.send(f"🔊 **Sonidos disponibles:**\n{sound_list}\n\nUsa `!play_sound <nombre>` para reproducir")

    @bot.command()
    async def play_sound(ctx, sound_name: str = None):
        """Reproduce un sonido del soundboard"""
        if sound_name is None:
            await ctx.send("❌ Especifica un sonido. Usa `!sounds` para ver la lista")
            return

        sound_name = sound_name.lower()
        
        if sound_name not in SOUND_FILES:
            await ctx.send(f"❌ Sonido '{sound_name}' no encontrado. Usa `!sounds` para ver la lista")
            return

        if not ctx.author.voice:
            await ctx.send("❌ Tenés que estar en un canal de voz")
            return

        if not ctx.voice_client:
            channel = ctx.author.voice.channel
            try:
                await channel.connect()
            except Exception as e:
                await ctx.send(f"❌ No pude conectarme al canal de voz: {str(e)}")
                return

        vc = ctx.voice_client
        
        if vc.is_playing():
            vc.stop()

        sound_path = SOUND_FILES[sound_name]
        
        if not os.path.exists(sound_path):
            await ctx.send(f"⚠️ El archivo de sonido '{sound_name}' no existe en el servidor")
            return

        try:
            vc.play(discord.FFmpegPCMAudio(sound_path, **FFMPEG_OPTIONS))  # type: ignore
            await ctx.send(f"🔊 Reproduciendo: **{sound_name}**")
        except Exception as e:
            await ctx.send(f"❌ Error al reproducir: {str(e)}")
