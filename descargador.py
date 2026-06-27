import yt_dlp
def validar (url,nombre, carpeta):
    if not url:
        raise ValueError("Falta URL")
    if not nombre:
        raise ValueError("Falta nombre")
    if not carpeta:
        raise ValueError("Falta la carpeta")
    
def construir_opciones(nombre, carpeta, on_progress):
    return {
        "format": "bestaudio/best",
        "outtmpl": f"{carpeta}/{nombre}.%(ext)s",
        "progress_hooks": [on_progress],
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "0",
        }],
    }
def descargar_mp3(url, nombre, carpeta, on_progress):
    validar(url, nombre, carpeta)              # 1. revisa entrada
    opciones = construir_opciones(nombre, carpeta, on_progress)  # 2. arma ficha
    with yt_dlp.YoutubeDL(opciones) as ydl:    # 3. prepara yt-dlp
        ydl.download([url])                     # 4. ¡baja!