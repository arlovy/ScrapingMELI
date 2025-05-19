"""
Herramientas relacionadas al manejo de proxies.
"""

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
