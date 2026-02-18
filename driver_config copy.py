import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions


def encontrar_chromium():
    """Encuentra la ruta de chromium en el sistema."""
    try:
        resultado = subprocess.run(
            ["which", "chromium", "chromium-browser", "google-chrome"],
            capture_output=True, text=True
        )
        if resultado.stdout.strip():
            return resultado.stdout.strip().split('\n')[0]
    except:
        pass

    rutas = [
        "/run/current-system/sw/bin/chromium",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome",
        "/nix/var/nix/profiles/default/bin/chromium",
    ]
    for ruta in rutas:
        if os.path.exists(ruta):
            return ruta
    return None


def encontrar_chromedriver():
    """Encuentra la ruta de chromedriver en el sistema."""
    try:
        resultado = subprocess.run(
            ["which", "chromedriver"],
            capture_output=True, text=True
        )
        if resultado.stdout.strip():
            return resultado.stdout.strip()
    except:
        pass

    rutas = [
        "/run/current-system/sw/bin/chromedriver",
        "/usr/bin/chromedriver",
        "/usr/local/bin/chromedriver",
        "/nix/var/nix/profiles/default/bin/chromedriver",
    ]
    for ruta in rutas:
        if os.path.exists(ruta):
            return ruta
    return None


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

        chromium_path = encontrar_chromium()
        chromedriver_path = encontrar_chromedriver()

        print(f"Chromium encontrado en: {chromium_path}")
        print(f"Chromedriver encontrado en: {chromedriver_path}")

        if chromium_path:
            options.binary_location = chromium_path

        if chromedriver_path:
            service = ChromeService(executable_path=chromedriver_path)
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
