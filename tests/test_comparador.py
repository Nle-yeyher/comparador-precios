import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.producto import Producto, Oferta
from comparador.comparar import comparar_producto, imprimir_resultados


def test_comparacion_basica():
    """
    Prueba con datos simulados de audífonos en 3 tiendas.
    Verifica que el sistema ordene correctamente y genere explicaciones.
    """
    producto = Producto(
        nombre="Audífonos Bluetooth",
        marca="Sony",
        modelo="WH-1000XM4",
        categoria="Tecnología"
    )

    producto.agregar_oferta(Oferta(
        tienda="MercadoLibre",
        precio_producto=280000,
        costo_envio=0,
        envio_gratis=True,
        tiempo_entrega_dias=3,
        disponible=True,
        url_compra="https://mercadolibre.com/producto/123"
    ))

    producto.agregar_oferta(Oferta(
        tienda="AliExpress",
        precio_producto=250000,
        costo_envio=35000,
        envio_gratis=False,
        tiempo_entrega_dias=20,
        disponible=True,
        url_compra="https://aliexpress.com/producto/456"
    ))

    producto.agregar_oferta(Oferta(
        tienda="Temu",
        precio_producto=260000,
        costo_envio=15000,
        envio_gratis=False,
        tiempo_entrega_dias=12,
        disponible=True,
        url_compra="https://temu.com/producto/789"
    ))

    resultados = comparar_producto(producto)
    imprimir_resultados(producto, resultados)

    # Verificaciones
    assert len(resultados) == 3, "Deben haber 3 resultados"
    assert resultados[0]["es_mejor"] == True, "El primero debe ser la mejor opción"
    assert resultados[0]["puntaje"] < resultados[1]["puntaje"], "El puntaje debe estar ordenado"
    print("\n✅ Todas las pruebas pasaron correctamente.")


def test_producto_sin_disponibilidad():
    """
    Prueba que las ofertas no disponibles se excluyan del resultado.
    """
    producto = Producto(
        nombre="Celular",
        marca="Samsung",
        modelo="Galaxy A54",
        categoria="Tecnología"
    )

    producto.agregar_oferta(Oferta(
        tienda="MercadoLibre",
        precio_producto=900000,
        costo_envio=0,
        envio_gratis=True,
        tiempo_entrega_dias=2,
        disponible=True,
        url_compra="https://mercadolibre.com/producto/999"
    ))

    producto.agregar_oferta(Oferta(
        tienda="Temu",
        precio_producto=750000,
        costo_envio=20000,
        envio_gratis=False,
        tiempo_entrega_dias=15,
        disponible=False,  # No disponible
        url_compra="https://temu.com/producto/888"
    ))

    resultados = comparar_producto(producto)
    assert len(resultados) == 1, "Solo debe aparecer la oferta disponible"
    print("✅ Test de disponibilidad pasó correctamente.")


if __name__ == "__main__":
    print("Ejecutando pruebas del núcleo de comparación...\n")
    test_comparacion_basica()
    test_producto_sin_disponibilidad()
