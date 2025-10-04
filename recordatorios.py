import discord
from discord.ext import commands, tasks
import json
import os
from datetime import datetime, timedelta
import re

RECORDATORIOS_FILE = "recordatorios.json"

def cargar_recordatorios():
    """Carga los recordatorios desde el archivo JSON"""
    if os.path.exists(RECORDATORIOS_FILE):
        try:
            with open(RECORDATORIOS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def guardar_recordatorios(recordatorios):
    """Guarda los recordatorios en el archivo JSON"""
    with open(RECORDATORIOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(recordatorios, f, indent=2, ensure_ascii=False)

def parsear_tiempo(tiempo_str):
    """Convierte string como '10m', '2h', '30s' a segundos"""
    match = re.match(r'^(\d+)([smhd])$', tiempo_str.lower())
    if not match:
        return None
    
    cantidad = int(match.group(1))
    unidad = match.group(2)
    
    conversiones = {
        's': 1,           
        'm': 60,          
        'h': 3600,        
        'd': 86400,       
    }
    
    return cantidad * conversiones[unidad]

recordatorios = []
verificar_recordatorios_task = None
_setup_completed = False

def setup_recordatorios_commands(bot):
    global recordatorios, verificar_recordatorios_task, _setup_completed
    
    if _setup_completed:
        return
    
    recordatorios = cargar_recordatorios()
    
    @tasks.loop(seconds=10)
    async def verificar_recordatorios():
        """Verifica si hay recordatorios que enviar"""
        global recordatorios
        ahora = datetime.now().timestamp()
        recordatorios_pendientes = []
        
        for recordatorio in recordatorios:
            if recordatorio['timestamp'] <= ahora:
                try:
                    canal = bot.get_channel(recordatorio['canal_id'])
                    usuario = bot.get_user(recordatorio['usuario_id'])
                    
                    if canal and usuario:
                        await canal.send(f"⏰ {usuario.mention} Recordatorio: **{recordatorio['mensaje']}**")
                        print(f"✅ Recordatorio enviado a {usuario.name}: {recordatorio['mensaje']}")
                    else:
                        print(f"⚠️ No se pudo enviar recordatorio - Canal: {canal}, Usuario: {usuario}")
                except Exception as e:
                    print(f"❌ Error enviando recordatorio: {e}")
            else:
                recordatorios_pendientes.append(recordatorio)
        
        if len(recordatorios_pendientes) != len(recordatorios):
            recordatorios = recordatorios_pendientes
            guardar_recordatorios(recordatorios)
    
    verificar_recordatorios_task = verificar_recordatorios
    
    async def on_ready_listener():
        if verificar_recordatorios_task and not verificar_recordatorios_task.is_running():
            verificar_recordatorios_task.start()
            print("✅ Sistema de recordatorios iniciado")
    
    bot.add_listener(on_ready_listener, 'on_ready')
    _setup_completed = True
    
    @bot.command()
    async def recordar(ctx, tiempo: str = None, *, mensaje: str = None):
        """Crea un recordatorio. Ejemplo: !recordar 10m tomar agua"""
        global recordatorios
        if tiempo is None or mensaje is None:
            await ctx.send("❌ Uso: `!recordar <tiempo> <mensaje>`\nEjemplo: `!recordar 10m tomar agua`\nTiempos: s (segundos), m (minutos), h (horas), d (días)")
            return
        
        segundos = parsear_tiempo(tiempo)
        if segundos is None:
            await ctx.send("❌ Formato de tiempo inválido. Usa: 30s, 10m, 2h, 1d")
            return
        
        timestamp_recordatorio = datetime.now().timestamp() + segundos
        
        nuevo_recordatorio = {
            'usuario_id': ctx.author.id,
            'canal_id': ctx.channel.id,
            'mensaje': mensaje,
            'timestamp': timestamp_recordatorio,
            'creado': datetime.now().isoformat()
        }
        
        recordatorios.append(nuevo_recordatorio)
        guardar_recordatorios(recordatorios)
        
        tiempo_legible = f"{segundos // 60} minuto(s)" if segundos >= 60 else f"{segundos} segundo(s)"
        await ctx.send(f"✅ Te recordaré en {tiempo_legible}: **{mensaje}**")
    
    @bot.command()
    async def mis_recordatorios(ctx):
        """Muestra tus recordatorios activos"""
        global recordatorios
        mis_recordatorios = [r for r in recordatorios if r['usuario_id'] == ctx.author.id]
        
        if not mis_recordatorios:
            await ctx.send("📭 No tenés recordatorios activos")
            return
        
        embed = discord.Embed(title="📋 Tus Recordatorios", color=discord.Color.blue())
        
        for i, recordatorio in enumerate(mis_recordatorios, 1):
            tiempo_restante = recordatorio['timestamp'] - datetime.now().timestamp()
            minutos = int(tiempo_restante // 60)
            
            embed.add_field(
                name=f"{i}. {recordatorio['mensaje'][:50]}",
                value=f"⏱️ En {minutos} minuto(s)" if minutos > 0 else "⏱️ Próximamente",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @bot.command()
    async def borrar_recordatorios(ctx):
        """Borra todos tus recordatorios"""
        global recordatorios
        recordatorios_anteriores = len(recordatorios)
        recordatorios = [r for r in recordatorios if r['usuario_id'] != ctx.author.id]
        
        borrados = recordatorios_anteriores - len(recordatorios)
        
        if borrados > 0:
            guardar_recordatorios(recordatorios)
            await ctx.send(f"🗑️ Se borraron {borrados} recordatorio(s)")
        else:
            await ctx.send("📭 No tenías recordatorios para borrar")
