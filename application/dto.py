class ProductDTO:
    def __init__(self, product_id, name, price, quantity):
        # Data Transfer Object para productos
        self.product_id = product_id  # ID del producto
        self.name = name              # Nombre del producto
        self.price = price            # Precio del producto
        self.quantity = quantity      # Cantidad disponible

class InvoiceItemDTO:
    def __init__(self, product_id, name, price, quantity, total):
        # Data Transfer Object para un ítem de factura
        self.product_id = product_id  # ID del producto
        self.name = name              # Nombre del producto
        self.price = price            # Precio unitario
        self.quantity = quantity      # Cantidad facturada
        self.total = total            # Total por este ítem

class InvoiceDTO:
    def __init__(self, items):
        # Data Transfer Object para una factura completa
        self.items = items  # Lista de ítems de la factura
        # Calcula el monto total de la factura sumando los totales de cada ítem
        self.total_amount = sum(item.total for item in items) if items else 0.0