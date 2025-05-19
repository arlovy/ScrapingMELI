"""
Provee herramientas de lectura y escritura de archivos.
"""

def read_txt(path:str) -> list[str]:
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
        text = []

    return text

def clean_value(value) -> str:
    if isinstance(value, str):
        if value.strip() == "":
            return None
        elif value.isdigit():
            return int(value)
    return value