"""
Este modulo trae datos de distintos sitios web de venta de inmuebles.
"""

import bs4
import requests as r

lista = []
house_id = 0

for i in range(42): #get data until page 30
    if i == 0:
        file = r.get("https://inmuebles.mercadolibre.com.ar/venta/")
    else:
        file = r.get(f"https://inmuebles.mercadolibre.com.ar/venta/_Desde_{i * 48 + 1}_NoIndex_True") #every page has 48 posts

    texto = bs4.BeautifulSoup(file.text, features='html.parser')
    results = texto.find_all('li',class_='ui-search-layout__item') #class to get every article

    for item in results:
        sublist = []
        price = item.find('div', class_="poly-component__price").text
        if price[:2] == "US": #only fetch properties in prices in US$

            property_type = item.find('span', class_="poly-component__headline").text.split()[0]
            if property_type == "Otro":
                continue 

            house_id += 1 #increment house id
            sublist.append(house_id)
            sublist.append(property_type)

            sublist.append(price[3:].replace(".",""))

            attributes = item.find_all('li')

            if property_type == "Terreno":
                if len(attributes) > 1:
                    attributes = attributes[1]
                for i in range(2):
                     sublist.append("")
            
            if property_type == "Local":
                if len(attributes) == 1:
                    for _ in range(2):
                        sublist.append("")
                else:
                    sublist.append("")


            for attribute in attributes:
                info = attribute.text.split()

                if info[1] != "ha": #si no son hectareas, son m2
                    sublist.append(info[0].replace(".",""))
                else:
                    sublist.append(int(info[0].replace(".","")) * 1000) # 1 hectarea = 10000 m2

        if sublist:
            lista.append(sublist)

for item in lista:
    if item[1] == "Local":
        print(item)
print()

"""
TO DO:
- Revisar error relacionado con las listas. Cuando en los terrenos hay (1 amb | m2) se loopea dos veces por articulo de la pagina. (HECHO)
- Terminar de diseñar el script. Falta traer los datos de ubicacion.
- Configurar proxys para que no se bloquee la aplicacion por la cantidad de requests.
- Diseñar carga a la BD cuando termine todo.
"""