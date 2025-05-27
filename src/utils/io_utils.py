"""
Provee herramientas de lectura y escritura de archivos.
"""
from typing import List
import logging

logger = logging.getLogger(__name__)

def read_txt(path:str) -> List[str]:
    """
    Lee un archivo de texto.

    Params:
        path: La ubicacion del archivo de texto a leer.
    Returns:
        Una lista de strings.
    """
    try:
        with open(path, 'r', encoding='utf-8-sig') as archivo:
            text = [linea.strip() for linea in archivo]
    except FileNotFoundError:
        logging.warning("Error en la lectura del archivo %s", path)
        text = []

    return text
