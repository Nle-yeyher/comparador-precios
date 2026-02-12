import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions


def crear_driver():
    """
    Crea el driver correcto según el entorno:
    - Producción (Railway/Linux): Chromium headless
    - Local (Windows): Edge headless
    """
    en_produccion = os.environ.get("RAILWAY_ENVIRONMENT") or os.environ.get("PORT")

    if en_produccion:
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        options.binary_location = "/nix/store/chromium"

        # Buscar chromedriver en paths conocidos de Railway
        chromedriver_paths = [
            "/nix/store/chromedriver",
            "/usr/bin/chromedriver",
            "/usr/local/bin/chromedriver",
        ]
        service = None
        for path in chromedriver_paths:
            if os.path.exists(path):
                service = ChromeService(executable_path=path)
                break

        if service:
            return webdriver.Chrome(service=service, options=options)
        return webdriver.Chrome(options=options)

    else:
        options = EdgeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0")
        return webdriver.Edge(options=options)
