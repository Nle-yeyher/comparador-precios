import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions


def encontrar_binario(nombres):
    """Busca un binario en el PATH del sistema."""
    for nombre in nombres:
        try:
            resultado = subprocess.run(
                ["which", nombre],
                capture_output=True, text=True
            )
            ruta = resultado.stdout.strip()
            if ruta and os.path.exists(ruta):
                return ruta
        except:
            continue

    # Buscar en directorios nix
    try:
        resultado = subprocess.run(
            ["find", "/nix", "-name", nombres[0], "-type", "f"],
            capture_output=True, text=True, timeout=5
        )
        lineas = resultado.stdout.strip().split('\n')
        for linea in lineas:
            if linea and os.path.exists(linea):
                return linea
    except:
        pass

    return None


def crear_driver():
    en_produccion = os.environ.get("RAILWAY_ENVIRONMENT") or os.environ.get("PORT")

    if en_produccion:
        options = ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        chromium = encontrar_binario(["chromium", "chromium-browser", "google-chrome"])
        chromedriver = encontrar_binario(["chromedriver"])

        print(f"Chromium: {chromium}")
        print(f"Chromedriver: {chromedriver}")

        if chromium:
            options.binary_location = chromium

        if chromedriver:
            return webdriver.Chrome(
                service=ChromeService(executable_path=chromedriver),
                options=options
            )

        return webdriver.Chrome(options=options)

    else:
        options = EdgeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0")
        return webdriver.Edge(options=options)