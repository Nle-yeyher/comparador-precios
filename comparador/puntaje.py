from typing import List
from models.producto import Oferta

# Pesos del sistema de comparación (deben sumar 1.0)
PESO_PRECIO = 0.50
PESO_ENVIO = 0.20
PESO_TIEMPO = 0.30


def calcular_puntaje(oferta: Oferta, todas_las_ofertas: List[Oferta]) -> float:
    """
    Calcula el puntaje de una oferta comparándola contra las demás.
    Menor puntaje = mejor opción.

    Se normaliza cada valor entre 0 y 1 usando el mínimo y máximo del grupo,
    para que el puntaje sea justo sin importar las unidades (pesos, días, etc.)
    """
    precios_finales = [o.precio_final for o in todas_las_ofertas]
    costos_envio = [o.costo_envio for o in todas_las_ofertas]
    tiempos = [o.tiempo_entrega_dias for o in todas_las_ofertas]

    puntaje_precio = _normalizar(oferta.precio_final, precios_finales)
    puntaje_envio = _normalizar(oferta.costo_envio, costos_envio)
    puntaje_tiempo = _normalizar(oferta.tiempo_entrega_dias, tiempos)

    return (
        puntaje_precio * PESO_PRECIO +
        puntaje_envio * PESO_ENVIO +
        puntaje_tiempo * PESO_TIEMPO
    )


def _normalizar(valor: float, lista: List[float]) -> float:
    """
    Normaliza un valor entre 0 y 1 dentro de una lista.
    Si todos los valores son iguales, retorna 0 (empate perfecto).
    """
    minimo = min(lista)
    maximo = max(lista)

    if maximo == minimo:
        return 0.0

    return (valor - minimo) / (maximo - minimo)
