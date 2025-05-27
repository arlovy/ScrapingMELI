"""
Operaciones de lógica de negocio.
"""
from bs4 import Tag

def append_item_attributes(attr:Tag, row:list) -> None:
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
        if isinstance(attribute, str) and attribute.isdigit():
            attribute = int(attribute)
        #lo spliteo, tal que si "32 m2 cubiertos" entonces ["32","m2","cubiertos"]
        info = attribute.text.split()

        #los terrenos pueden tener el tamaño en hectareas
        if info[1] != "ha": #si no son hectareas, son m2
            row.append(info[0].replace(".",""))
        else:
            row.append(int(info[0].replace(".","")) * 10000) # 1 hectarea = 10000 m2
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
                row.append(None)
        case "Local":
            #los locales pueden tener baños, en ese caso me salteo los
            #ambientes porque no se especifican
            #y los pongo como un campo vacío.
            if len(attr) == 1:
                for _ in range(2):
                    row.append(None)
            else:
                row.append(None)
    return None
