from typing import List, Dict
from models.producto import Producto, Oferta
from comparador.puntaje import calcular_puntaje
from comparador.explicacion import generar_explicacion


def comparar_producto(producto: Producto) -> List[Dict]:
    """
    Recibe un producto con sus ofertas y retorna una lista ordenada
    de resultados, de mejor a peor opción, con puntaje y explicación.
    """
    ofertas_disponibles = [o for o in producto.ofertas if o.disponible]

    if not ofertas_disponibles:
        return []

    # Calcular puntaje para cada oferta
    resultados = []
    for oferta in ofertas_disponibles:
        puntaje = calcular_puntaje(oferta, ofertas_disponibles)
        resultados.append({
            "oferta": oferta,
            "puntaje": puntaje
        })

    # Ordenar de menor a mayor puntaje (menor = mejor)
    resultados.sort(key=lambda r: r["puntaje"])

    # Marcar la mejor opción y generar explicaciones
    for i, resultado in enumerate(resultados):
        es_mejor = (i == 0)
        resultado["es_mejor"] = es_mejor
        resultado["explicacion"] = generar_explicacion(
            resultado["oferta"],
            es_mejor,
            ofertas_disponibles
        )

    return resultados


def imprimir_resultados(producto: Producto, resultados: List[Dict]):
    """
    Imprime los resultados de comparación de forma clara en consola.
    """
    print(f"\n{'='*60}")
    print(f"  Producto: {producto}")
    print(f"{'='*60}")

    for i, resultado in enumerate(resultados):
        oferta = resultado["oferta"]
        print(f"\n  #{i+1} — {oferta.tienda}")
        print(f"  Precio producto : ${oferta.precio_producto:,.0f}")
        print(f"  Costo envío     : ${oferta.costo_envio:,.0f} {'(gratis)' if oferta.envio_gratis else ''}")
        print(f"  Precio final    : ${oferta.precio_final:,.0f}")
        print(f"  Entrega         : {oferta.tiempo_entrega_dias} día(s)")
        print(f"  Puntaje         : {resultado['puntaje']:.4f}")
        print(f"  {resultado['explicacion']}")
        print(f"  🔗 {oferta.url_compra}")
        print(f"  {'-'*56}")
