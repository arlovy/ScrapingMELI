"""
Extrae datos de los elementos HTML.
"""

from bs4 import Tag
from .logic import set_attributes_for_special_property, append_item_attributes

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
            sublist.append(property_type)

            sublist.append(price[3:].replace(".","")) # US$3.942  >> 3942

            set_attributes_for_special_property(property_type, sublist, attributes)

            append_item_attributes(attributes, sublist)

            #la ciudad
            sublist.append(location.text.split(",")[-1])
            #el barrio
            sublist.append(location.text.split(",")[-2])
    return sublist
