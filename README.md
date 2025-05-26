# ScrapingMELI
Este es un proyecto de webscraping  en Python, que extrae datos de inmuebles en venta de MercadoLibre. Si bien MercadoLibre tiene una API para realizar este tipo de consultas de manera más eficiente, estaba interesado en desarrollar este programa para experimentar con la librería BeautifulSoup y manejo de consultas a bases de datos usando Python. 

### Tecnologías
- Python. 
    - Librería requests para la descarga del HTML. 
    - Librería BeautifulSoup4 para el parseo de los archivos.
    - Librería psycopg3 para la conexión y ejecución de consultas a la base de datos.
- PostgreSQL.

### Funcionamiento
El programa hace consultas a la página de MercadoLibre, solo trayendo el contenido de 42 páginas debido al límite de navegación del sitio. Se le pueden pasar proxies al programa, para evitar bloqueos por exceso de solicitudes. Para hacer esto de forma más rápida, el programa hace uso de multihilado con ThreadPoolExecutor.
