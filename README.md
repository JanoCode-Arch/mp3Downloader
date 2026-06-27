# DownloaderMP3: ByJano

App de escritorio para descargar audio (**MP3**) o video (**MP4**) de YouTube, con interfaz simple.

Pegas la URL, le pones nombre, eliges carpeta y formato, y descarga. Recuerda la última carpeta usada.

---

## Requisitos previos

Necesitas dos cosas instaladas en la computadora (una sola vez):

1. **Python 3** — https://www.python.org/downloads/ (o `winget install Python.Python.3.13`)
2. **ffmpeg** — necesario para convertir a MP3 y unir video+audio en MP4:
   ```powershell
   winget install Gyan.FFmpeg
   ```
   > Tras instalarlo, **cierra y reabre la terminal** para que tome el PATH.

---

## Instalar y correr (en una compu nueva)

Abre PowerShell **normal** (no como administrador) y corre:

```powershell
git clone https://github.com/JanoCode-Arch/mp3Downloader.git
cd mp3Downloader
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

> Si al activar el venv sale error de *execution policy*, corre una vez:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```
> y vuelve a activar. Cuando el prompt muestre `(.venv)`, ya estás dentro del entorno.

---

## Crear el `.exe` (para usarlo sin consola)

Con el venv activo (`(.venv)` visible), desde la carpeta del proyecto:

```powershell
pyinstaller --noconsole --onefile --icon=icono.ico --add-data "icono.ico;." --collect-all customtkinter --name "DownloaderMP3" app.py
```

Qué hace cada parte:

| Flag | Para qué |
|------|----------|
| `--noconsole` | No abre ventana de terminal |
| `--onefile` | Genera un solo `.exe` |
| `--icon=icono.ico` | Pone el icono al `.exe` |
| `--add-data "icono.ico;."` | Incluye el icono dentro (para el icono de la ventana) |
| `--collect-all customtkinter` | Empaqueta los recursos de customtkinter (sin esto, el `.exe` truena) |
| `--name "DownloaderMP3"` | Nombre del ejecutable |

El resultado queda en **`dist\DownloaderMP3.exe`**. Ese archivo lo puedes mover al Escritorio, anclarlo a la barra de tareas o crearle un acceso directo.

> **Nota:** el `.exe` sigue necesitando que **ffmpeg** esté instalado en la computadora donde se ejecute (paso de Requisitos).

---

## Estructura del proyecto

```
mp3Downloader/
├── app.py               # La interfaz (ventana customtkinter)
├── descargador.py       # La lógica de descarga (usa yt-dlp)
├── test_descargador.py  # Pruebas (pytest)
├── icono.ico            # Icono de la app
├── requirements.txt     # Dependencias
└── README.md            # Este archivo
```

## Correr las pruebas

```powershell
pytest
```

## Notas

- La última carpeta de descarga se recuerda en `~/.downloadermp3.json` (tu carpeta de usuario).
- "Ambos" descarga dos archivos: el `.mp3` y el `.mp4`.
