"""
Ejecuta las operaciones de carga de datos en una BD de PostgreSQL.
"""

from typing import Tuple
from psycopg import connect, Connection, Cursor, Error

def connect_to_db(db_name:str,
                  user:str,
                  password:str) -> Tuple[Connection, Cursor]:
    """
    Establece una conexión a una base de datos y retorna los objetos de conexión y
    el cursor para ejecutar consultas.

    IMPORTANTE: La conexión a la base de datos debe ser cerrada posteriormente.

    Params:
        db_name: El nombre de la base de datos.
        user: El usuario de la base de datos.
        password: La contraseña de la base de datos.
    Returns:
        Una tupla tal que (Conexión, Cursor)
    """
    try:
        conn = connect(f"dbname={db_name} user={user} password={password}")
        cursor = conn.cursor()
    except Exception:
        return None, None

    return conn,cursor


def execute_query(connection_:Connection,
                  cursor_:Cursor,
                  query_:str,
                  params_:list[str]) -> int:
    """
    Ejecuta una consulta SQL en una base de datos y confirma los cambios.

    Como precondición, se debe haber establecido una conexión exitosa a una BD.

    Params:
        connection_: Un objeto Connection de psycopg.
        cursor_: Un objeto Cursor de psycopg, de la misma conexión que se está pasando
        como argumento.
        query: Un string con la query a ejecutar.
    Returns:
        N
    """
    try:
        if params_:
            cursor_.execute(query_,params_)
        else:
            cursor_.execute(query_)
        connection_.commit()
        return cursor_
    except Error as exc:
        raise Error from exc

def close_connection(connection_: Connection) -> None:
    """
    Cierra la conexión a la base de datos.
    
    Params:
        connection_: Un objeto Connection de psycopg.
    Returns:
        None
    """
    connection_.close()

    return None
