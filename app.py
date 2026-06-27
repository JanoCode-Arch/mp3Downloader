import threading
from tkinter import filedialog

import customtkinter as ctk

from descargador import descargar_mp3

# ----- Tokens de diseño -----
FONDO = "#1A1A1D"      # carbón
AMBAR = "#E8A04B"      # acento (glow de medidor VU)
AMBAR_HOVER = "#CF8A3A"
TEXTO_OSCURO = "#1A1A1D"  # texto sobre ámbar
GRIS = "#8A8A8E"       # texto secundario

FUENTE_TITULO = ("Segoe UI Semibold", 26)
FUENTE_LABEL = ("Segoe UI", 13)
FUENTE_MONO = ("Consolas", 12)
FUENTE_BOTON = ("Segoe UI Semibold", 14)

# ----- Ventana -----
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("DownloaderMP3: ByJano")
app.geometry("480x560")
app.configure(fg_color=FONDO)


# ----- Funciones -----
def elegir_carpeta():
    ruta = filedialog.askdirectory()
    if ruta:
        entry_carpeta.delete(0, "end")
        entry_carpeta.insert(0, ruta)


def on_progress(d):
    if d["status"] == "downloading":
        total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
        bajado = d.get("downloaded_bytes", 0)
        frac = bajado / total if total else 0
        app.after(0, lambda v=frac: barra.set(v))
        app.after(0, lambda v=frac: estado.configure(text=f"Descargando...  {int(v * 100)}%"))
    elif d["status"] == "finished":
        app.after(0, lambda: barra.set(1))
        app.after(0, lambda: estado.configure(text="Convirtiendo a mp3..."))


def worker(url, nombre, carpeta):
    try:
        descargar_mp3(url, nombre, carpeta, on_progress)
        app.after(0, lambda: estado.configure(text=f"✅ Listo:  {nombre}.mp3", text_color=AMBAR))
    except ValueError as e:
        app.after(0, lambda err=e: estado.configure(text=f"⚠️  {err}", text_color=GRIS))
    except Exception as e:
        app.after(0, lambda err=e: estado.configure(text=f"❌ Error: {err}", text_color=GRIS))
    finally:
        app.after(0, lambda: boton.configure(state="normal", text="Descargar MP3"))


def descargar():
    url = entry_url.get().strip()
    nombre = entry_nombre.get().strip()
    carpeta = entry_carpeta.get().strip()
    barra.set(0)
    estado.configure(text="Iniciando...", text_color=GRIS)
    boton.configure(state="disabled", text="Descargando...")
    threading.Thread(target=worker, args=(url, nombre, carpeta), daemon=True).start()


# ----- Interfaz -----
titulo = ctk.CTkLabel(app, text="Downloader", font=FUENTE_TITULO)
titulo.pack(pady=(28, 2))

subtitulo = ctk.CTkLabel(app, text="YouTube  →  MP3", font=FUENTE_LABEL, text_color=GRIS)
subtitulo.pack(pady=(0, 24))

# URL
ctk.CTkLabel(app, text="URL del video", font=FUENTE_LABEL).pack(anchor="w", padx=24)
entry_url = ctk.CTkEntry(app, font=FUENTE_MONO, placeholder_text="https://www.youtube.com/watch?v=...")
entry_url.pack(fill="x", padx=24, pady=(4, 14))

# Nombre
ctk.CTkLabel(app, text="Nombre del archivo", font=FUENTE_LABEL).pack(anchor="w", padx=24)
entry_nombre = ctk.CTkEntry(app, font=FUENTE_LABEL, placeholder_text="mi cancion")
entry_nombre.pack(fill="x", padx=24, pady=(4, 14))

# Carpeta (campo + botón Examinar en una fila)
ctk.CTkLabel(app, text="Guardar en", font=FUENTE_LABEL).pack(anchor="w", padx=24)
fila = ctk.CTkFrame(app, fg_color="transparent")
fila.pack(fill="x", padx=24, pady=(4, 22))
entry_carpeta = ctk.CTkEntry(fila, font=("Consolas", 11), placeholder_text="Elige una carpeta...")
entry_carpeta.pack(side="left", fill="x", expand=True)
ctk.CTkButton(
    fila, text="Examinar", width=92, font=FUENTE_LABEL,
    fg_color="transparent", border_width=1, border_color=GRIS,
    text_color="#FFFFFF", hover_color="#2A2A2E",
    command=elegir_carpeta,
).pack(side="left", padx=(8, 0))

# Botón descargar (la firma: ámbar)
boton = ctk.CTkButton(
    app, text="Descargar MP3", height=44, font=FUENTE_BOTON,
    fg_color=AMBAR, hover_color=AMBAR_HOVER, text_color=TEXTO_OSCURO,
    command=descargar,
)
boton.pack(fill="x", padx=24, pady=(0, 16))

# Barra de progreso (ámbar)
barra = ctk.CTkProgressBar(app, progress_color=AMBAR)
barra.set(0)
barra.pack(fill="x", padx=24)

# Estado
estado = ctk.CTkLabel(app, text="", font=FUENTE_LABEL, text_color=GRIS)
estado.pack(pady=14)

app.mainloop()
