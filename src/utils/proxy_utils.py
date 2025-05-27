"""
Herramientas relacionadas al manejo de proxies.
"""

import random as rn
from typing import List, Dict
from urllib.parse import urlparse


def random_proxy(proxies: Dict[str, List[str]]) -> Dict[str, str]:
    """
    Elije una proxy aleatoriamente y la devuelve.
    
    Params:
        proxies: Las proxies ya formateadas en un diccionario.
    Returns:
        un diccionario con una sola key: value:
        {protocolo: url}
    """
    if not proxies:
        return {}
    protocol = rn.choice(list(proxies.keys()))
    proxy = rn.choice(proxies[protocol])
    return {protocol: proxy}


def format_proxies(proxies: List[str]) -> Dict[str, List[str]]:
    """
    Formatea las proxys desde una lista, las convierte en elementos de
    un diccionario.
    
    Params:
        proxies: Una lista de proxys(strings)
    
    Returns:
        Un diccionario donde cada elemento es una proxy.
        {protocol: url}
    """
    if not proxies:
        return {}
    formatted = {}
    for proxy in proxies:
        parsed = urlparse(proxy)
        scheme = parsed.scheme
        if scheme in {"http", "https", "socks4", "socks5"}:
            if scheme not in formatted:
                formatted[scheme] = []
            formatted[scheme].append(proxy)
    return formatted
