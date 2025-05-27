"""
Extrae datos de los elementos HTML.
"""
import logging
from bs4 import Tag
from .logic import set_attributes_for_special_property, append_item_attributes

logger = logging.getLogger(__name__)

def get_item_data(item: Tag) -> list[str]:
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
            Una lista vacía
    """
    #defino el registro del item como sublist
    sublist = []

    try:
        price = parse_price(item)
    except ValueError:
        return sublist

    if price:

        property_type = item.find('span', class_="poly-component__headline").text.split()[0]
        if property_type == "Otro": #no lee propiedades con tipo "Otro"
            logger.info("Artículo descartado por tipo 'Otro'.")
            return []

        #aca se leen los atributos de la propiedad
        # metros cuadrados, ambientes, etc.
        attributes = item.find_all('li')

        #lee la ubicacion
        location = item.find('span',class_="poly-component__location")

        if attributes and location: #si el articulo esta completo
            sublist.append(property_type)

            sublist.append(price) # 'US$3.942'  >> 3942

            set_attributes_for_special_property(property_type, sublist, attributes)

            append_item_attributes(attributes, sublist)

            parts = location.text.split(",")
            if len(parts) < 2:
                logger.warning("Ubicación incompleta: %s", location.text)
                return []

            #la ciudad
            sublist.append(parts[-1])
            #el barrio
            sublist.append(parts[-2])
    return sublist


def parse_price(item: Tag) -> int:
    """
    Lee el precio de un artículo y lo retorna en formato entero.

    Params:
        item: Un artículo leído con BeautifulSoup.
    Returns:
        Un entero que representa el precio del artículo.
    Raises:
        ValueError ante cualquier error en la lectura del precio, o si
        no está expresado en dolares.
    """
    price = item.find('div', class_="poly-component__price")

    #si no encuentra el atributo o no tiene precio
    if not price or not price.text:
        logger.error("Error de lectura de precio en artículo.")
        raise ValueError("Error de lectura de precio de artículo")

    price = price.text
    if price.startswith("US$"): #solo lee posts con precios en dolares
        try:
            price = int(price[3:].replace(".",""))
        except ValueError as exc:
            logger.warning("Error de conversión de precio: %s", price)
            raise ValueError("Error de conversión de precio") from exc
    else:
        logger.info("Precio no expresado en dólares.")
        raise ValueError("Precio no expresado en dolares")

    return price
