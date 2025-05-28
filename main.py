"""
Archivo principal
"""
from typing import Annotated
import logging
from psycopg import Error
import typer
import src.db_operations.db as db
import src.collector.collector as dcol

app = typer.Typer()

logging.basicConfig(level=logging.INFO,
                    filename="registros.log",
                    filemode="w",
                    format="%(asctime)s - [%(levelname)s en %(module)s] %(message)s")

@app.command()
def scrape(db_:Annotated[str, typer.Argument(help="Nombre de la base de datos")],
        user:Annotated[str, typer.Argument(help="Usuario de la base de datos")],
        pass_:Annotated[str, typer.Argument(help="Contraseña de la base de datos")],
        proxy_path:Annotated[str,
                             typer.Option(
                                 "--proxy-path", help="Ruta al archivo de proxies"
                                 )] = "") -> None:
    """
    Inicializa el programa.
    
    Params:
        db_: El nombre de la base de datos con la que interactuará el programa.
        user: El usuario de la BD.
        pass_: La contraseña del usuario de la BD.
    Returns:
        None
    """
    try:
        with db.connect_to_db(db_name=db_, user=user, password=pass_) as conn:
            cursor = conn.cursor()
            for item in dcol.collect_data(proxies_url=proxy_path):

                query_string = """INSERT INTO properties(property_type,
                         property_price,
                         property_ambients,
                         property_bathrooms,
                         property_size,
                         property_district,
                         property_location)
                         VALUES(%s,%s,%s,%s,%s,%s,%s)"""

                db.execute_query(cursor_=cursor,
                            connection_=conn,
                            query_=query_string,
                            params_=item)
    except Error as e:
        logging.error("Error al conectar a la base de datos. %s", e)
        exit()


if __name__ == "__main__":
    #insertar datos aca
    app()
