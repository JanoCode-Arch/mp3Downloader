import pytest
from descargador import validar

def test_validar_url_vacia_lanza_error():
    with pytest.raises(ValueError):
        validar("", "cancion", "C:/musica")

def test_validar_todo_lleno_no_lanza():
    validar("https://www.youtube.com/watch?v=IT_dC-ziqs0", "Lumare-Tutto-Passa", "C:/Users/avla2/Music/Testing")