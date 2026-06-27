import pytest
from descargador import validar
from descargador import construir_opciones

def test_validar_url_vacia_lanza_error():
    with pytest.raises(ValueError):
        validar("", "cancion", "C:/musica")

def test_validar_todo_lleno_no_lanza():
    validar("https://www.youtube.com/watch?v=IT_dC-ziqs0", "Lumare-Tutto-Passa", "C:/Users/avla2/Music/Testing")
    
def test_construir_opciones_arma_ruta_correc():
    opts = construir_opciones("cancion","C:/musica",None)
    assert opts["outtmpl"] == "C:/musica/cancion.%(ext)s"

def test_construir_opciones_es_mp3():
    opts = construir_opciones("c", "d", None)
    post = opts["postprocessors"][0]
    assert post["preferredcodec"] == "mp3"
    assert post["preferredquality"] == "0"

def test_construir_opciones_mp4_es_video():
    opts = construir_opciones("c", "d", None, "mp4")
    assert opts["merge_output_format"] == "mp4"
    assert "postprocessors" not in opts  # mp4 no extrae audio