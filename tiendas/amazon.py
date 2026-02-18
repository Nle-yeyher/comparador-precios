from driver_config import crear_driver
from selenium.webdriver.common.by import By
from models.producto import Oferta
import time
import re


def extraer_url_producto(item):
    try:
        asin = item.get_attribute("data-asin")
        if asin and len(asin) == 10:
            return f"https://www.amazon.com/-/es/dp/{asin}"
    except:
        pass
    try:
        item_id = item.get_attribute("data-csa-c-item-id") or ""
        match = re.search(r'asin\.([A-Z0-9]{10})', item_id)
        if match:
            return f"https://www.amazon.com/-/es/dp/{match.group(1)}"
    except:
        pass
    try:
        href = item.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href")
        match = re.search(r'/dp/([A-Z0-9]{10})', href)
        if match:
            return f"https://www.amazon.com/-/es/dp/{match.group(1)}"
        if href.startswith("http"):
            return href
    except:
        pass
    return "https://www.amazon.com"


def buscar_productos(query: str, limite: int = 5) -> list:
    url = f"https://www.amazon.com/s?k={query.replace(' ', '+')}&language=es"
    driver = crear_driver()
    ofertas = []

    try:
        print(f"  Buscando '{query}' en Amazon...")
        driver.get(url)
        time.sleep(3)  # Reducido de 4 a 3

        items = driver.find_elements(By.CSS_SELECTOR, "div[data-component-type='s-search-result']")
        print(f"  Se encontraron {len(items)} items en Amazon")

        for item in items[:limite * 2]:
            try:
                try:
                    nombre = item.find_element(By.CSS_SELECTOR, "h2").text.strip()
                    if not nombre:
                        continue
                except:
                    continue

                try:
                    precio_texto = item.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
                    precio = float(precio_texto.replace(",", "").replace(".", "").strip())
                except:
                    continue

                url_producto = extraer_url_producto(item)

                try:
                    imagen_url = item.find_element(By.CSS_SELECTOR, "img.s-image").get_attribute("src") or ""
                except:
                    imagen_url = ""

                oferta = Oferta(
                    tienda="Amazon",
                    precio_producto=precio,
                    costo_envio=25000,
                    envio_gratis=False,
                    tiempo_entrega_dias=20,
                    disponible=True,
                    url_compra=url_producto,
                    imagen_url=imagen_url,
                    nombre_producto=nombre
                )
                ofertas.append(oferta)
                print(f"  ✅ {nombre[:50]} — ${precio:,.0f}")

                if len(ofertas) >= limite:
                    break

            except Exception as e:
                continue

    except Exception as e:
        print(f"  ❌ Error general en Amazon: {e}")
    finally:
        driver.quit()

    return ofertas
