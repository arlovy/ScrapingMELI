"""
Este modulo trae datos de distintos sitios web de venta de inmuebles.
"""

import random as rn
from concurrent.futures import ThreadPoolExecutor
import bs4
import requests as r
from functools import partial

house_id = 0

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


def format_proxy(proxy_url:str) -> dict:
    """
    Convierte una URL de un proxy en formato string a un 
    diccionario para ser leído por la libreria requests.

    Params:
        proxy_url: Una URL de un proxy.
    
    Returns:
        Un diccionario tal que {'http': [URL]}
    """
    return {"http": proxy_url}


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
        La página en formato texto.
    """

    file = r.get(url,
                proxies=proxy,
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=10)

    return file.text


def append_item_attributes(attr:list[str], row:list) -> None:
    """
    Lee los atributos de un artículo y los anexa a su registro.
    
    Params:
        attr: La lista de atributos del artículo.
        row: El registro al cual se anexarán los datos
    Returns:
        None
    """
    #para cada atributo del articulo
    for attribute in attr:
        #lo spliteo, tal que si "32 m2 cubiertos" entonces ["32","m2","cubiertos"]
        info = attribute.text.split()

        #los terrenos pueden tener el tamaño en hectareas
        if info[1] != "ha": #si no son hectareas, son m2
            row.append(info[0].replace(".",""))
        else:
            row.append(int(info[0].replace(".","")) * 1000) # 1 hectarea = 10000 m2
    return None


def set_attributes_for_special_property(property_:str, row:list, attr:list[str]) -> None:
    """
    Modifica los atributos del registro de un artículo en caso de que este sea
    de tipo no residencial, agregando valores nulos donde correspondan.
    
    Params:
        property_: El tipo de la propiedad.
        row: El registro correspondiente al artículo
        attr: La lista de atributos del artículo.
    Returns:
        None
    """
    match property_:
        case "Terreno":
            #si el tipo de propiedad es terreno, puede pasar que en la publicación
            #se especifique que tiene 1 ambiente. si pasa esto, salto directamente
            # al segundo atributo (los metros cuadrados/ hectareas del terreno)
            if len(attr) > 1:
                #reasigno los valores de la lista para que solo quede el segundo
                #atributo
                attr[:] = attr[1]
            #appendeo 2 campos vacíos porque no hay baño ni ambientes
            for _ in range(2):
                row.append("")
        case "Local":
            #los locales pueden tener baños, en ese caso me salteo los
            #ambientes porque no se especifican
            #y los pongo como un campo vacío.
            if property_ == "Local":
                if len(attr) == 1:
                    for _ in range(2):
                        row.append("")
            else:
                row.append("")
    return None


def get_item_data(item:list[str]) -> list[str]:
    """
    Lee los datos correspondientes a un artículo de MercadoLibre y
    los agrupa en un registro.

    Params:
        item: Un elemento de la página de búsqueda de inmuebles de 
        MercadoLibre, leído con BeautifulSoup.
    Returns:
        Si el articulo está completo:
            Los datos del artículo, con el siguiente formato:
            [id,tipo,precio,ambientes,baños,m2,ciudad,barrio]
        Si no está completo:
            Una lista
    """
    #defino el registro del item como sublist
    sublist = []

    price = item.find('div', class_="poly-component__price").text
    if price[:2] == "US": #solo lee posts con precios en dolares

        property_type = item.find('span', class_="poly-component__headline").text.split()[0]
        if property_type == "Otro": #no lee propiedades con tipo "Otro"
            return None

        #aca se leen los atributos de la propiedad
        # metros cuadrados, ambientes, etc.
        attributes = item.find_all('li')

        #lee la ubicacion
        location = item.find('span',class_="poly-component__location")

        if attributes and location: #si el articulo esta completo
            global house_id
            house_id += 1
            sublist.append(house_id)
            sublist.append(property_type)

            sublist.append(price[3:].replace(".","")) # US$3.942  >> 3942

            set_attributes_for_special_property(property_type, sublist, attributes)

            append_item_attributes(attributes, sublist)

            #la ciudad
            sublist.append(location.text.split(",")[-1])
            #el barrio
            sublist.append(location.text.split(",")[-2])
    return sublist

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


def collect_data() -> list[str]:
    """
    Función principal del módulo. Extrae datos de los artículos de venta
    de inmuebles en MercadoLibre que esten completos.

    Params:
        None
    Returns:
        Una matriz donde cada registro es una propiedad en venta
    """
    meli_data = []
    proxies = read_txt('proxies.txt')
    urls = url_maker()

    with ThreadPoolExecutor(max_workers=30) as executor:
        fetch = partial(fetch_page, proxy=format_proxy(rn.choice(proxies)))
        archivos = list(executor.map(fetch, urls))


    for archivo in archivos:
        articles = bs4.BeautifulSoup(archivo,
                                     features='html.parser'
                        ).find_all('li',class_='ui-search-layout__item')

        for article in articles:
            item_data = get_item_data(article)
            if item_data:
                meli_data.append(item_data)

    return meli_data
