import requests
from bs4 import BeautifulSoup
from models.producto import Oferta

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def buscar_productos(query: str, limite: int = 5) -> list:
    url = f"https://listado.mercadolibre.com.co/{query.replace(' ', '-')}"
    ofertas = []

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "lxml")

        items = soup.select(".ui-search-result")[:limite]

        for item in items:
            try:
                nombre = item.select_one(".ui-search-item__title").get_text(strip=True)

                precio_tag = item.select_one(".andes-money-amount__fraction")
                precio = float(precio_tag.text.replace(".", "")) if precio_tag else 0.0

                link = item.select_one("a.ui-search-link")["href"]

                img = item.select_one("img")
                imagen_url = img["src"] if img else ""

                envio_gratis = bool(item.select_one(".ui-search-item__shipping--free"))
                costo_envio = 0 if envio_gratis else 15000

                ofertas.append(
                    Oferta(
                        tienda="MercadoLibre",
                        precio_producto=precio,
                        costo_envio=costo_envio,
                        envio_gratis=envio_gratis,
                        tiempo_entrega_dias=3 if envio_gratis else 5,
                        disponible=True,
                        url_compra=link,
                        imagen_url=imagen_url,
                        nombre_producto=nombre
                    )
                )
            except:
                continue

    except Exception as e:
        print("Error MercadoLibre:", e)

    return ofertas
