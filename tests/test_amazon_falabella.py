import sys
sys.path.insert(0, '.')
from tiendas.amazon import buscar_productos as buscar_amazon
from tiendas.falabella import buscar_productos as buscar_falabella

print("=== TEST AMAZON ===")
ofertas_amazon = buscar_amazon("audífonos bluetooth", limite=3)
if ofertas_amazon:
    for o in ofertas_amazon:
        print(f"  ✅ {o.nombre_producto[:50]} | ${o.precio_producto:,.0f}")
else:
    print("  ❌ Sin resultados")

print("\n=== TEST FALABELLA ===")
ofertas_falabella = buscar_falabella("audífonos bluetooth", limite=3)
if ofertas_falabella:
    for o in ofertas_falabella:
        print(f"  ✅ {o.nombre_producto[:50]} | ${o.precio_producto:,.0f}")
else:
    print("  ❌ Sin resultados")
