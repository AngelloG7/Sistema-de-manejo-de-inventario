class Product:
    def __init__(self, product_id, name, price, quantity):
        # Constructor de la clase Producto
        self.product_id = product_id      # ID único del producto
        self.name = name                  # Nombre del producto
        self.price = price                # Precio de venta del producto
        self.quantity = quantity          # Cantidad disponible en inventario

    def update_quantity(self, amount):
        self.quantity += amount

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
        }