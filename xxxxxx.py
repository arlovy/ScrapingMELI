def url_maker() -> list[str]:
    urls = []
    for page_num in range(42):
        end = f"_Desde_{page_num * 48 + 1}" if page_num else ''

        url = "https://inmuebles.mercadolibre.com.ar/venta/" + end

        urls.append(url)

    return None
