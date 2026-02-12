from models.producto import Oferta
from typing import List


def generar_explicacion(oferta: Oferta, es_mejor: bool, todas_las_ofertas: List[Oferta]) -> str:
    """
    Genera una explicación en lenguaje natural para cada oferta.
    Compara la oferta contra la mejor para explicar sus desventajas.
    """
    if es_mejor:
        razones = []

        precio_minimo = min(o.precio_final for o in todas_las_ofertas)
        envio_minimo = min(o.costo_envio for o in todas_las_ofertas)
        tiempo_minimo = min(o.tiempo_entrega_dias for o in todas_las_ofertas)

        if oferta.precio_final == precio_minimo:
            razones.append("menor precio final")
        if oferta.costo_envio == envio_minimo:
            razones.append("envío más conveniente")
        if oferta.tiempo_entrega_dias == tiempo_minimo:
            razones.append("entrega más rápida")

        if razones:
            return f"✅ Mejor opción por {' y '.join(razones)}."
        return "✅ Mejor opción general."

    else:
        mejor = min(todas_las_ofertas, key=lambda o: o.precio_final)
        razones = []

        if oferta.precio_final > mejor.precio_final:
            diferencia = oferta.precio_final - mejor.precio_final
            razones.append(f"el precio final es ${diferencia:,.0f} más caro")
        if oferta.costo_envio > mejor.costo_envio:
            razones.append("el envío es más caro")
        if oferta.tiempo_entrega_dias > mejor.tiempo_entrega_dias:
            dias_extra = oferta.tiempo_entrega_dias - mejor.tiempo_entrega_dias
            razones.append(f"tarda {dias_extra} día(s) más en llegar")

        if razones:
            return f"❌ No es la mejor opción porque {' y '.join(razones)}."
        return "❌ No es la mejor opción en comparación general."
