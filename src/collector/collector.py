"""
Realiza las tareas de recolección de datos de forma concurrente.
"""

from concurrent.futures import ThreadPoolExecutor
import random as rn
from functools import partial
from bs4 import BeautifulSoup
from src.network.fetcher import fetch_page
from src.parser.parser import get_item_data
from src.utils.io_utils import read_txt
from src.utils.proxy_utils import format_proxy

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


def collect_data(proxies_url:str) -> list[str]:
    """
    Función principal del módulo. Extrae datos de los artículos de venta
    de inmuebles en MercadoLibre que esten completos.

    Params:
        None
    Returns:
        Una matriz donde cada registro es una propiedad en venta
    """
    meli_data = []
    proxies = read_txt(proxies_url)
    urls = url_maker()

    with ThreadPoolExecutor(max_workers=30) as executor:
        fetch = partial(fetch_page, proxy=format_proxy(rn.choice(proxies)))
        archivos = list(executor.map(fetch, urls))


    for archivo in archivos:
        articles = BeautifulSoup(archivo,
                                     features='html.parser'
                        ).find_all('li',class_='ui-search-layout__item')

        for article in articles:
            item_data = get_item_data(article)
            if item_data and len(item_data) == 7:
                meli_data.append(item_data)

    return meli_data
