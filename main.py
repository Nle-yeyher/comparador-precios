from models.producto import Producto, Oferta
from comparador.comparar import comparar_producto, imprimir_resultados


def main():
    """
    Punto de entrada del comparador.
    Por ahora usa datos simulados. En Fase 2 se conectará a tiendas reales.
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


if __name__ == "__main__":
    main()
