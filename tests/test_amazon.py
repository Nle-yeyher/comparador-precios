import sys
sys.path.insert(0, '.')
from tiendas.amazon import buscar_productos

ofertas = buscar_productos("audífonos bluetooth", limite=3)
for o in ofertas:
    print(f"{o.tienda} | {o.nombre_producto[:50]} | ${o.precio_producto:,.0f}")