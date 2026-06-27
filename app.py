import json
import os
import sys
import threading
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk

from descargador import descargar

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

# Archivo donde recordamos preferencias entre sesiones
CONFIG = Path.home() / ".downloadermp3.json"


def recurso(rel):
    """Ruta a un archivo incluido. Funciona en desarrollo y dentro del .exe (PyInstaller)."""
    base = getattr(sys, "_MEIPASS", Path(__file__).parent)
    return Path(base) / rel

# ----- Ventana -----
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("DownloaderMP3: ByJano")
app.geometry("480x640")
app.configure(fg_color=FONDO)

# Icono de la ventana (y de la barra de tareas)
ICONO = recurso("icono.ico")
if ICONO.exists():
    app.iconbitmap(str(ICONO))


# ----- Configuración (persistencia con JSON) -----
def cargar_config():
    if CONFIG.exists():
        return json.loads(CONFIG.read_text(encoding="utf-8"))
    return {}


def guardar_config(datos):
    CONFIG.write_text(json.dumps(datos), encoding="utf-8")


# ----- Funciones -----
def elegir_carpeta():
    ruta = filedialog.askdirectory()
    if ruta:
        entry_carpeta.delete(0, "end")
        entry_carpeta.insert(0, ruta)
        guardar_config({"ultima_carpeta": ruta})  # recuerda para la próxima


def ver_carpeta():
    carpeta = entry_carpeta.get().strip()
    if carpeta and os.path.isdir(carpeta):
        os.startfile(carpeta)  # abre el Explorador de Windows
    else:
        estado.configure(text="⚠️  Elige una carpeta válida primero", text_color=GRIS)


def on_progress(d):
    if d["status"] == "downloading":
        total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
        bajado = d.get("downloaded_bytes", 0)
        frac = bajado / total if total else 0
        app.after(0, lambda v=frac: barra.set(v))
        app.after(0, lambda v=frac: estado.configure(text=f"Descargando...  {int(v * 100)}%"))
    elif d["status"] == "finished":
        app.after(0, lambda: barra.set(1))
        app.after(0, lambda: estado.configure(text="Procesando..."))


def worker(url, nombre, carpeta, formato):
    try:
        descargar(url, nombre, carpeta, on_progress, formato)
        app.after(0, lambda: estado.configure(text=f"✅ Listo:  {nombre}", text_color=AMBAR))
    except ValueError as e:
        app.after(0, lambda err=e: estado.configure(text=f"⚠️  {err}", text_color=GRIS))
    except Exception as e:
        app.after(0, lambda err=e: estado.configure(text=f"❌ Error: {err}", text_color=GRIS))
    finally:
        app.after(0, lambda: boton.configure(state="normal", text="Descargar"))


def iniciar_descarga():
    url = entry_url.get().strip()
    nombre = entry_nombre.get().strip()
    carpeta = entry_carpeta.get().strip()
    formato = selector_formato.get().lower()  # "mp3" | "mp4" | "ambos"
    barra.set(0)
    estado.configure(text="Iniciando...", text_color=GRIS)
    boton.configure(state="disabled", text="Descargando...")
    threading.Thread(target=worker, args=(url, nombre, carpeta, formato), daemon=True).start()


# ----- Interfaz -----
titulo = ctk.CTkLabel(app, text="Downloader", font=FUENTE_TITULO)
titulo.pack(pady=(28, 2))

subtitulo = ctk.CTkLabel(app, text="YouTube  →  MP3 · MP4", font=FUENTE_LABEL, text_color=GRIS)
subtitulo.pack(pady=(0, 24))

# URL
ctk.CTkLabel(app, text="URL del video", font=FUENTE_LABEL).pack(anchor="w", padx=24)
entry_url = ctk.CTkEntry(app, font=FUENTE_MONO, placeholder_text="https://www.youtube.com/watch?v=...")
entry_url.pack(fill="x", padx=24, pady=(4, 14))

# Nombre
ctk.CTkLabel(app, text="Nombre del archivo", font=FUENTE_LABEL).pack(anchor="w", padx=24)
entry_nombre = ctk.CTkEntry(app, font=FUENTE_LABEL, placeholder_text="mi cancion")
entry_nombre.pack(fill="x", padx=24, pady=(4, 14))

# Formato (selector mp3 / mp4 / ambos)
ctk.CTkLabel(app, text="Formato", font=FUENTE_LABEL).pack(anchor="w", padx=24)
selector_formato = ctk.CTkSegmentedButton(
    app, values=["MP3", "MP4", "Ambos"], font=FUENTE_LABEL,
    selected_color=AMBAR, selected_hover_color=AMBAR_HOVER,
    unselected_color="#2A2A2E", unselected_hover_color="#3A3A3E",
    text_color="#FFFFFF",
)
selector_formato.set("MP3")
selector_formato.pack(fill="x", padx=24, pady=(4, 14))

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

# Rellenar la carpeta con la última usada (si existe en el config)
_cfg = cargar_config()
if _cfg.get("ultima_carpeta"):
    entry_carpeta.insert(0, _cfg["ultima_carpeta"])

# Botón descargar (la firma: ámbar)
boton = ctk.CTkButton(
    app, text="Descargar", height=44, font=FUENTE_BOTON,
    fg_color=AMBAR, hover_color=AMBAR_HOVER, text_color=TEXTO_OSCURO,
    command=iniciar_descarga,
)
boton.pack(fill="x", padx=24, pady=(0, 14))

# Barra de progreso (ámbar)
barra = ctk.CTkProgressBar(app, progress_color=AMBAR)
barra.set(0)
barra.pack(fill="x", padx=24)

# Estado
estado = ctk.CTkLabel(app, text="", font=FUENTE_LABEL, text_color=GRIS)
estado.pack(pady=12)

# Botón secundario: abrir la carpeta de salida
ctk.CTkButton(
    app, text="📂  Ver carpeta de salida", height=36, font=FUENTE_LABEL,
    fg_color="transparent", border_width=1, border_color=GRIS,
    text_color="#FFFFFF", hover_color="#2A2A2E",
    command=ver_carpeta,
).pack(fill="x", padx=24, pady=(0, 10))

app.mainloop()
