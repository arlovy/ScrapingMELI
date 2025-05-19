"""
Provee herramientas para las consultas a la página de MELI.
"""

import requests as r

def fetch_page(url:str, proxy=None) -> str:
    """
    Hace una petición la página de venta de inmuebles de MercadoLibre 
    y retorna la respuesta en formato texto. 

    Params: 
        page_num: El número de página a extraer.
        proxy: Un proxy utilizado para la request. Por defecto, es None.

        Formato del proxy:
        proxy = {
            'http': [URL]
        }
    Returns: 
        La página en formato texto unicode.
    Exceptions:
        En caso de algún error a la hora de hacer una request, retorna un
        string vacío.
    """

    try:
        file = r.get(url,
                    proxies=proxy,
                    headers={'User-Agent': 'Mozilla/5.0'},
                    timeout=10)
    except r.exceptions.RequestException as e:
        print(f"Error: {e}")
        return ""

    return file.text
