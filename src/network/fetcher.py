"""
Provee herramientas para las consultas a la página de MELI.
"""
from typing import Dict, List
import logging
import requests as r
from src.utils.proxy_utils import random_proxy

logger = logging.getLogger(__name__)

def fetch_with_random_proxy(url: str, formatted: Dict[str, List[str]]) -> str:
    """
    Elige un proxy aleatorio de una pool de proxies y hace una request usándolo.

    Params:
        url: La url de la página a la cual se va a hacer la request.
        proxies: Una pool de proxies.
    Returns:
        La página en formato texto.
    """

    proxy = random_proxy(formatted)
    return fetch_page(url, proxy)


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
        file.raise_for_status()
    except r.HTTPError:
        logger.warning("Error HTTP %s en %s",file.status_code,url)
        return ""
    except r.exceptions.RequestException:
        logger.warning("Error de conexión: %s", url)
        return ""

    return file.text
