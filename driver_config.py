import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions


def crear_driver():
    """
    Crea el driver correcto según el entorno:
    - Producción (Railway con Docker): Chrome desde imagen selenium/standalone-chrome
    - Local (Windows): Edge headless
    """
    en_produccion = os.environ.get("RAILWAY_ENVIRONMENT") or os.environ.get("PORT")

    if en_produccion:
        # En la imagen selenium/standalone-chrome todo está configurado
        options = ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # Chrome y chromedriver vienen en /usr/bin en esta imagen
        options.binary_location = "/usr/bin/google-chrome"
        service = ChromeService(executable_path="/usr/bin/chromedriver")

        print(f"[Producción] Usando Chrome desde imagen Docker")
        return webdriver.Chrome(service=service, options=options)

    else:
        # Entorno local con Edge
        options = EdgeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0")
        return webdriver.Edge(options=options)
