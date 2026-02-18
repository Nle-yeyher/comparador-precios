from flask import Flask, render_template, request, jsonify
from tiendas.mercadolibre import buscar_productos as buscar_ml
from tiendas.falabella import buscar_productos as buscar_falabella
from tiendas.amazon import buscar_productos as buscar_amazon
from comparador.comparar import comparar_producto
from models.producto import Producto
import subprocess
import os

app = Flask(__name__)


def buscar_en_todas(query: str):
    """Busca en todas las tiendas SECUENCIALMENTE para ahorrar memoria."""
    todas_las_ofertas = []

    # Buscar una tienda a la vez para no sobrecargar RAM
    try:
        ofertas_ml = buscar_ml(query, limite=3)
        todas_las_ofertas += ofertas_ml
    except Exception as e:
        print(f"Error en MercadoLibre: {e}")

    try:
        ofertas_fb = buscar_falabella(query, limite=3)
        todas_las_ofertas += ofertas_fb
    except Exception as e:
        print(f"Error en Falabella: {e}")

    try:
        ofertas_az = buscar_amazon(query, limite=3)
        todas_las_ofertas += ofertas_az
    except Exception as e:
        print(f"Error en Amazon: {e}")

    return todas_las_ofertas


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/buscar")
def buscar():
    query = request.args.get("q", "").strip()
    precio_min = request.args.get("precio_min", type=int)
    precio_max = request.args.get("precio_max", type=int)

    if not query:
        return render_template("index.html", error="Escribe un producto para buscar.")

    producto = Producto(nombre=query, marca="", modelo="", categoria="General")
    ofertas = buscar_en_todas(query)

    if not ofertas:
        return render_template("index.html", error="No se encontraron resultados para tu búsqueda.")

    # Aplicar filtros de precio
    if precio_min is not None:
        ofertas = [o for o in ofertas if o.precio_final >= precio_min]
    if precio_max is not None:
        ofertas = [o for o in ofertas if o.precio_final <= precio_max]

    if not ofertas:
        return render_template("index.html", error="No hay resultados con esos filtros de precio.")

    for oferta in ofertas:
        producto.agregar_oferta(oferta)

    resultados = comparar_producto(producto)

    precios = [r['oferta'].precio_final for r in resultados]
    precio_min_disponible = int(min(precios)) if precios else 0
    precio_max_disponible = int(max(precios)) if precios else 0

    return render_template(
        "resultados.html",
        query=query,
        resultados=resultados,
        precio_min_disponible=precio_min_disponible,
        precio_max_disponible=precio_max_disponible,
        filtro_min=precio_min,
        filtro_max=precio_max
    )


@app.route("/diagnostico")
def diagnostico():
    info = {}
    for cmd in ["chromium", "chromium-browser", "google-chrome", "chromedriver"]:
        try:
            r = subprocess.run(["which", cmd], capture_output=True, text=True)
            info[cmd] = r.stdout.strip() or "no encontrado"
        except:
            info[cmd] = "error"

    try:
        r = subprocess.run(
            ["find", "/nix", "-name", "chromium", "-type", "f"],
            capture_output=True, text=True, timeout=5
        )
        info["nix_chromium"] = r.stdout.strip()[:200] or "no encontrado"
    except:
        info["nix_chromium"] = "error"

    info["env_port"] = os.environ.get("PORT", "no definido")
    info["env_railway"] = os.environ.get("RAILWAY_ENVIRONMENT", "no definido")

    return jsonify(info)


if __name__ == "__main__":
    app.run(debug=True)
