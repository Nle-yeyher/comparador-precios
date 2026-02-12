from flask import Flask, render_template, request
from tiendas.mercadolibre import buscar_productos as buscar_ml
from tiendas.falabella import buscar_productos as buscar_falabella
from tiendas.amazon import buscar_productos as buscar_amazon
from comparador.comparar import comparar_producto
from models.producto import Producto
import concurrent.futures

app = Flask(__name__)


def buscar_en_todas(query: str):
    """Busca en todas las tiendas en paralelo para mayor velocidad."""
    todas_las_ofertas = []

    def buscar_tienda(func, nombre):
        try:
            return func(query, limite=3)
        except Exception as e:
            print(f"  Error en {nombre}: {e}")
            return []

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futuro_ml = executor.submit(buscar_tienda, buscar_ml, "MercadoLibre")
        futuro_fb = executor.submit(buscar_tienda, buscar_falabella, "Falabella")
        futuro_az = executor.submit(buscar_tienda, buscar_amazon, "Amazon")

        todas_las_ofertas += futuro_ml.result()
        todas_las_ofertas += futuro_fb.result()
        todas_las_ofertas += futuro_az.result()

    return todas_las_ofertas


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/buscar")
def buscar():
    query = request.args.get("q", "").strip()

    if not query:
        return render_template("index.html", error="Escribe un producto para buscar.")

    producto = Producto(
        nombre=query,
        marca="",
        modelo="",
        categoria="General"
    )

    ofertas = buscar_en_todas(query)

    if not ofertas:
        return render_template("index.html", error="No se encontraron resultados para tu búsqueda.")

    for oferta in ofertas:
        producto.agregar_oferta(oferta)

    resultados = comparar_producto(producto)

    return render_template("resultados.html", query=query, resultados=resultados)


if __name__ == "__main__":
    app.run(debug=True)
