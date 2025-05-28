"""
Ejecuta las operaciones de carga de datos en una BD de PostgreSQL.
"""

from typing import Tuple, List, Optional
import logging
from contextlib import contextmanager
from psycopg import connect, Connection, Cursor, Error

logger = logging.getLogger(__name__)

@contextmanager
def connect_to_db(db_name:str,
                  user:str,
                  password:str) -> Tuple[Connection, Cursor]:
    """
    Establece una conexión a una base de datos y retorna los objetos de conexión y
    el cursor para ejecutar consultas.

    IMPORTANTE: La conexión a la base de datos debe ser cerrada manualmente desde el
    objeto Connection posteriormente.

    Params:
        db_name: El nombre de la base de datos.
        user: El usuario de la base de datos.
        password: La contraseña de la base de datos.
    Returns:
        Una tupla tal que (Conexión, Cursor)
    """
    try:
        conn = connect(f"dbname={db_name} user={user} password={password}")
        yield conn
    except Error as exc:
        logger.error("Error de conexión a la base de datos: %s", exc)
        raise Error(f"Ocurrió un error de conexión a la base de datos: {exc}") from exc
    finally:
        if conn:
            conn.close()


def execute_query(connection_:Connection,
                  cursor_:Cursor,
                  query_:str,
                  params_: Optional[List[str]]) -> None:
    """
    Ejecuta una consulta SQL en una base de datos y confirma los cambios.

    Como precondición, se debe haber establecido una conexión exitosa a una BD.

    Params:
        connection_: Un objeto Connection de psycopg.
        cursor_: Un objeto Cursor de psycopg, de la misma conexión que se está pasando
        como argumento.
        query_: Un string con la query a ejecutar.
        params_: Parámetros a ser utilizados en la query.
    Returns:
        None
    """
    try:
        cursor_.execute(query_,params_ or [])
        connection_.commit()
    except Error as exc:
        logger.error("Error en la consulta SQL: %s", exc)
        raise Error from exc
