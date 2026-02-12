import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tiendas.mercadolibre import buscar_productos
from comparador.comparar import comparar_producto, imprimir_resultados
from models.producto import Producto


def test_busqueda_mercadolibre():
    """
    Prueba la búsqueda real de productos en MercadoLibre Colombia.
    """
    print("Buscando 'audífonos bluetooth' en MercadoLibre...\n")

    ofertas = buscar_productos("audífonos bluetooth", limite=3)

    print(f"Se encontraron {len(ofertas)} ofertas:\n")

    for i, oferta in enumerate(ofertas):
        print(f"  #{i+1} — {oferta.tienda}")
        print(f"  Precio producto : ${oferta.precio_producto:,.0f}")
        print(f"  Envío gratis    : {'Sí' if oferta.envio_gratis else 'No'}")
        print(f"  Precio final    : ${oferta.precio_final:,.0f}")
        print(f"  Disponible      : {'Sí' if oferta.disponible else 'No'}")
        print(f"  🔗 {oferta.url_compra}")
        print()

    assert len(ofertas) > 0, "No se encontraron ofertas"
    print("✅ Conexión con MercadoLibre exitosa.")


def test_comparacion_con_datos_reales():
    """
    Busca productos reales y los compara con el núcleo de comparación.
    """
    print("\nComparando ofertas reales de MercadoLibre...\n")

    producto = Producto(
        nombre="Audífonos Bluetooth",
        marca="",
        modelo="",
        categoria="Tecnología"
    )

    ofertas = buscar_productos("audífonos bluetooth", limite=4)

    for oferta in ofertas:
        producto.agregar_oferta(oferta)

    from comparador.comparar import comparar_producto, imprimir_resultados
    resultados = comparar_producto(producto)
    imprimir_resultados(producto, resultados)


if __name__ == "__main__":
    print("=== Test de conexión con MercadoLibre ===\n")
    test_busqueda_mercadolibre()
    test_comparacion_con_datos_reales()
