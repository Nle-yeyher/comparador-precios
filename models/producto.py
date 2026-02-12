from dataclasses import dataclass, field
from typing import List


@dataclass
class Oferta:
    """
    Representa una oferta de un producto en una tienda específica.
    Un mismo producto puede tener muchas ofertas de diferentes tiendas.
    """
    tienda: str              # Nombre de la tienda (ej: "MercadoLibre")
    precio_producto: float   # Precio del producto sin envío
    costo_envio: float       # Costo del envío (0 si es gratis)
    envio_gratis: bool       # True si el envío es gratis
    tiempo_entrega_dias: int # Días estimados de entrega
    disponible: bool         # True si está disponible para comprar
    url_compra: str          # URL directa a la tienda
    imagen_url: str = ""     # URL de la imagen del producto
    nombre_producto: str = ""  # Nombre del producto en la tienda

    @property
    def precio_final(self) -> float:
        """Precio real que paga el usuario: producto + envío."""
        return self.precio_producto + self.costo_envio


@dataclass
class Producto:
    """
    Representa un producto con todas sus ofertas disponibles en distintas tiendas.
    """
    nombre: str
    marca: str
    modelo: str
    categoria: str
    ofertas: List[Oferta] = field(default_factory=list)

    def agregar_oferta(self, oferta: Oferta):
        """Agrega una oferta al producto."""
        self.ofertas.append(oferta)

    def __str__(self):
        return f"{self.marca} {self.nombre} {self.modelo} ({self.categoria})"
