# 🤖 Comandos del Bot de Discord

## 📋 Comandos Generales

### `!github`
Comparte el enlace de GitHub

### `!meme`
Obtiene un meme aleatorio en español desde Reddit

---

## 🎵 Comandos de Música
**⚠️ Nota:** Requieren conexión de voz. No funcionan en Replit debido a limitaciones de red UDP.

### `!join`
El bot se une a tu canal de voz actual

### `!leave`
El bot sale del canal de voz

### `!play <url de YouTube>`
Reproduce audio desde un video de YouTube
- **Ejemplo:** `!play https://www.youtube.com/watch?v=dQw4w9WgXcQ`

### `!stop`
Detiene la reproducción actual

---

## 🔊 Soundboard
**⚠️ Nota:** Requieren conexión de voz. No funcionan en Replit debido a limitaciones de red UDP.

### `!sounds`
Muestra la lista de sonidos disponibles en el soundboard

### `!play_sound <nombre>`
Reproduce un sonido del soundboard
- **Ejemplo:** `!play_sound bruh`
- **Sonidos disponibles:** bruh, vine, wtf, error, airhorn

**Para agregar más sonidos:**
1. Sube archivos .mp3 a la carpeta `sounds/`
2. Edita el archivo `soundboard.py` y agrega el nombre y ruta en `SOUND_FILES`

---

## ⏰ Recordatorios

### `!recordar <tiempo> <mensaje>`
Crea un recordatorio que te notificará después del tiempo especificado

**Formatos de tiempo:**
- `s` = segundos
- `m` = minutos  
- `h` = horas
- `d` = días

**Ejemplos:**
- `!recordar 30s revisar el horno`
- `!recordar 10m tomar agua`
- `!recordar 2h llamar a mamá`
- `!recordar 1d pagar la factura`

### `!mis_recordatorios`
Muestra todos tus recordatorios activos con el tiempo restante

### `!borrar_recordatorios`
Elimina todos tus recordatorios activos

---

## 💡 Consejos

- Los recordatorios se guardan en un archivo, así que sobreviven si el bot se reinicia
- Puedes tener múltiples recordatorios activos al mismo tiempo
- Los comandos de música y soundboard funcionarán perfectamente si ejecutas el bot fuera de Replit (en tu PC o en un servidor VPS)
