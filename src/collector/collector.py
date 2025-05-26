"""
Realiza las tareas de recolección de datos de forma concurrente.
"""

from concurrent.futures import ThreadPoolExecutor
import logging
from functools import partial
from itertools import cycle
from typing import Generator
from bs4 import BeautifulSoup
from src.network.fetcher import fetch_with_random_proxy
from src.parser.parser import get_item_data
from src.utils.io_utils import read_txt

logging.basicConfig(
    level=logging.INFO,
    filename='registro.log',
    filemode='w',
    format="%(asctime)s - [%(levelname)s en %(module)s] %(message)s"
)


def url_maker() -> list[str]:
    """
    Produce las URLs de MercadoLibre a scrapear. 
    
    Params:
        None
    Returns:
        Una matriz donde cada registro es una URL de la página de
        inmuebles en venta de MercadoLibre.
    """
    urls = []

    #Mercado Libre solo permite ver hasta la pagina 42 en las busquedas
    for page_num in range(42):
        end = f"_Desde_{page_num * 48 + 1}" if page_num else ''

        url = "https://inmuebles.mercadolibre.com.ar/venta/" + end

        urls.append(url)

    return urls


def collect_data(proxies_url:str) -> Generator[list[str], None, None]:
    """
    Función principal del módulo collector. Extrae datos de los artículos de venta
    de inmuebles en MercadoLibre que esten completos.

    Params:
        None
    Returns:
        Un generador que produce una lista de atributos por propiedad (list[str])
    """
    proxy_pool = cycle(read_txt(proxies_url))
    urls = url_maker()

    with ThreadPoolExecutor(max_workers=30) as executor:
        fetch = partial(fetch_with_random_proxy, proxies=proxy_pool)
        archivos = list(executor.map(fetch, urls))


    for archivo in archivos:
        if not archivo:
            logging.info("Error en la request. ¿Proxy fallido?")
            continue

        try:
            articles = BeautifulSoup(archivo,
                                        features='html.parser'
                            ).find_all('li',class_='ui-search-layout__item')
        except Exception as e:
            logging.warning("Error de parseo %s", e)
            continue

        for article in articles:
            item_data = get_item_data(article)
            if item_data and len(item_data) == 7:
                yield item_data
