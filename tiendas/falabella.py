from driver_config import crear_driver
from selenium.webdriver.common.by import By
from models.producto import Oferta
import re
import time


def buscar_productos(query: str, limite: int = 5) -> list:
    url = f"https://www.falabella.com.co/falabella-co/search?Ntt={query.replace(' ', '+')}"
    driver = crear_driver()
    ofertas = []

    try:
        print(f"  Buscando '{query}' en Falabella...")
        driver.get(url)
        time.sleep(10)
        driver.execute_script("window.scrollTo(0, 1000);")
        time.sleep(3)

        items = driver.find_elements(By.CSS_SELECTOR, "div[class*='pod-4_GRID'], li[class*='pod-4_GRID']")
        if not items:
            items = driver.find_elements(By.CSS_SELECTOR, "div[class*='pod']")
            items = [i for i in items
                     if i.find_elements(By.CSS_SELECTOR, "img")
                     and '$' in i.text
                     and 'Tipo de Entrega' not in i.text
                     and 'Categoría' not in i.text]

        print(f"  Se encontraron {len(items)} items en Falabella")

        for item in items[:limite * 2]:
            try:
                texto = item.text.strip()
                if not texto or 'Tipo de Entrega' in texto or 'Categoría' in texto:
                    continue

                lineas = [l.strip() for l in texto.split('\n') if l.strip() and len(l.strip()) > 5]
                nombre = lineas[0] if lineas else "Producto Falabella"

                precios = re.findall(r'\$\s*[\d\.]+', texto)
                precio = 0.0
                for p_texto in precios:
                    p_limpio = p_texto.replace("$", "").replace(".", "").replace(" ", "").strip()
                    if p_limpio.isdigit() and int(p_limpio) > 10000:
                        precio = float(p_limpio)
                        break

                if precio == 0:
                    continue

                try:
                    url_producto = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    if url_producto and not url_producto.startswith("http"):
                        url_producto = "https://www.falabella.com.co" + url_producto
                except:
                    url_producto = "https://www.falabella.com.co"

                try:
                    img = item.find_element(By.CSS_SELECTOR, "img")
                    imagen_url = img.get_attribute("src") or img.get_attribute("data-src") or ""
                except:
                    imagen_url = ""

                envio_gratis = "gratis" in texto.lower()
                costo_envio = 0 if envio_gratis else 12000

                oferta = Oferta(
                    tienda="Falabella",
                    precio_producto=precio,
                    costo_envio=costo_envio,
                    envio_gratis=envio_gratis,
                    tiempo_entrega_dias=2 if envio_gratis else 4,
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
        print(f"  ❌ Error general en Falabella: {e}")
    finally:
        driver.quit()

    return ofertas
