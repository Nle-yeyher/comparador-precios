from driver_config import crear_driver
from selenium.webdriver.common.by import By
from models.producto import Oferta
import time


def buscar_productos(query: str, limite: int = 5) -> list:
    url = f"https://listado.mercadolibre.com.co/{query.replace(' ', '-')}"
    driver = crear_driver()
    ofertas = []

    try:
        print(f"🔎 Buscando '{query}' en MercadoLibre...")
        driver.get(url)
        time.sleep(4)

        items = driver.find_elements(
            By.CSS_SELECTOR,
            ".ui-search-result__wrapper, .poly-card, .ui-search-layout__item"
        )

        print(f"🟡 MercadoLibre → items encontrados: {len(items)}")

        for item in items[:limite]:
            try:
                # 📌 Nombre
                try:
                    nombre = item.find_element(
                        By.CSS_SELECTOR,
                        ".poly-component__title, .ui-search-item__title"
                    ).text
                except:
                    nombre = "Producto MercadoLibre"

                # 💰 Precio
                try:
                    precio_texto = item.find_element(
                        By.CSS_SELECTOR,
                        ".andes-money-amount__fraction"
                    ).text
                    precio = float(precio_texto.replace(".", ""))
                except:
                    precio = 0.0

                # 🚚 Envío
                try:
                    envio_texto = item.text.lower()
                    envio_gratis = "gratis" in envio_texto
                except:
                    envio_gratis = False

                # 🔗 URL
                try:
                    url_producto = item.find_element(
                        By.TAG_NAME, "a"
                    ).get_attribute("href")
                except:
                    url_producto = ""

                # 🖼 Imagen
                try:
                    img = item.find_element(By.TAG_NAME, "img")
                    imagen_url = (
                        img.get_attribute("src")
                        or img.get_attribute("data-src")
                        or ""
                    )
                except:
                    imagen_url = ""

                costo_envio = 0 if envio_gratis else 15000

                oferta = Oferta(
                    tienda="MercadoLibre",
                    precio_producto=precio,
                    costo_envio=costo_envio,
                    envio_gratis=envio_gratis,
                    tiempo_entrega_dias=3 if envio_gratis else 5,
                    disponible=True,
                    url_compra=url_producto,
                    imagen_url=imagen_url,
                    nombre_producto=nombre
                )

                ofertas.append(oferta)
                print(f"✅ {nombre[:45]} — ${precio:,.0f}")

            except Exception as e:
                print(f"⚠️ Error procesando producto: {e}")

    except Exception as e:
        print(f"❌ Error general MercadoLibre: {e}")

    finally:
        driver.quit()

    return ofertas
