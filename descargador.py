import yt_dlp
def validar (url,nombre, carpeta):
    if not url:
        raise ValueError("Falta URL")
    if not nombre:
        raise ValueError("Falta nombre")
    if not carpeta:
        raise ValueError("Falta la carpeta")
    
def construir_opciones(nombre, carpeta, on_progress, formato="mp3"):
    opciones = {
        "outtmpl": f"{carpeta}/{nombre}.%(ext)s",
        "progress_hooks": [on_progress],
    }
    if formato == "mp3":
        opciones["format"] = "bestaudio/best"
        opciones["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "0",
        }]
    elif formato == "mp4":
        opciones["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
        opciones["merge_output_format"] = "mp4"
    return opciones

def descargar(url, nombre, carpeta, on_progress, formato="mp3"):
    validar(url, nombre, carpeta)              # 1. revisa entrada
    if formato == "ambos":                     # 2. ambos = baja mp3 Y mp4
        descargar(url, nombre, carpeta, on_progress, "mp3")
        descargar(url, nombre, carpeta, on_progress, "mp4")
        return
    opciones = construir_opciones(nombre, carpeta, on_progress, formato)  # 3. arma ficha
    with yt_dlp.YoutubeDL(opciones) as ydl:    # 4. prepara yt-dlp
        ydl.download([url])                     # 5. ¡baja!