"""
Este modulo trae datos de distintos sitios web de venta de inmuebles.
"""

import bs4
import requests as r

lista = []
house_id = 0

#Mercado Libre solo permite ver hasta la pagina 42 en las busquedas
for i in range(42):
    if i == 0:
        #si es la primera pagina, no se especifica en la URL desde qué post empieza
        file = r.get("https://inmuebles.mercadolibre.com.ar/venta/")
    else:
        #todas las paginas de mercado libre tienen 48 posts
        file = r.get(f"https://inmuebles.mercadolibre.com.ar/venta/_Desde_{i * 48 + 1}_NoIndex_True")

    texto = bs4.BeautifulSoup(file.text, features='html.parser')
    results = texto.find_all('li',class_='ui-search-layout__item') #cada result en results es un articulo de la pagina

    for item in results:
        #definir el registro
        sublist = []

        #trae el precio
        price = item.find('div', class_="poly-component__price").text
        if price[:2] == "US": #solo lee posts con precios en dolares

            property_type = item.find('span', class_="poly-component__headline").text.split()[0]
            if property_type == "Otro": #no lee propiedades con tipo "Otro"
                continue 

            #aca se leen los atributos de la propiedad
            # metros cuadrados, ambientes, etc.
            attributes = item.find_all('li')

            if attributes:
                house_id += 1 
                sublist.append(house_id) 
                sublist.append(property_type)

                sublist.append(price[3:].replace(".","")) # US$3.942  >> 3942
            
                if property_type == "Terreno":
                    #si el tipo de propiedad es terreno, puede pasar que en la publicación
                    #se especifique que tiene 1 ambiente. si pasa esto, salto directamente
                    # al segundo atributo (los metros cuadrados/ hectareas del terreno)
                    if len(attributes) > 1:
                        attributes = attributes[1]
                    #appendeo 2 campos vacíos porque no hay baño ni ambientes 
                    for i in range(2):
                        sublist.append("")
                
                #los locales pueden tener baños, asi que me salteo los ambientes porque no se
                #especifican y los pongo como un campo vacío.
                if property_type == "Local":
                    if len(attributes) == 1:
                        for _ in range(2):
                            sublist.append("")
                    else:
                        sublist.append("")

                #para cada atributo del articulo
                for attribute in attributes:
                    #lo spliteo, tal que si "32 m2 cubiertos" entonces ["32","m2","cubiertos"]
                    info = attribute.text.split()

                    #los terrenos pueden tener el tamaño en hectareas
                    if info[1] != "ha": #si no son hectareas, son m2
                        sublist.append(info[0].replace(".",""))
                    else:
                        sublist.append(int(info[0].replace(".","")) * 1000) # 1 hectarea = 10000 m2

                
                lista.append(sublist)

for item in lista:
    print(item)

"""
TO DO:
- Revisar error relacionado con las listas. Cuando en los terrenos hay (1 amb | m2) se loopea dos veces por articulo de la pagina. (HECHO)
- Terminar de diseñar el script. Falta traer los datos de ubicacion.
- Configurar proxys para que no se bloquee la aplicacion por la cantidad de requests.
- Diseñar carga a la BD cuando termine todo.
"""