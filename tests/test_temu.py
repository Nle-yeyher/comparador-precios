import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tiendas.temu import buscar_productos


def test_busqueda_temu():
    print("=== Test de scraping en Temu ===\n")
    print("Buscando 'audífonos bluetooth' en Temu...\n")

    ofertas = buscar_productos("audífonos bluetooth", limite=3)

    if not ofertas:
        print("❌ No se encontraron ofertas en Temu.")
        print("   Posibles causas:")
        print("   - Temu bloqueó el scraping")
        print("   - Los selectores CSS cambiaron")
        print("   - Temu muestra captcha")
        return

    print(f"\nSe encontraron {len(ofertas)} ofertas:\n")
    for i, oferta in enumerate(ofertas):
        print(f"  #{i+1} — {oferta.tienda}")
        print(f"  Precio    : ${oferta.precio_producto:,.0f}")
        print(f"  Envío     : {'Gratis' if oferta.envio_gratis else f'${oferta.costo_envio:,.0f}'}")
        print(f"  Entrega   : {oferta.tiempo_entrega_dias} días")
        print(f"  🔗 {oferta.url_compra[:80]}...")
        print()

    print("✅ Temu scraping exitoso.")


if __name__ == "__main__":
    test_busqueda_temu()
