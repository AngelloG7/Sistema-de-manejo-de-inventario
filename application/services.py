from domain.models import Product
from domain.repository import InventoryRepository
from typing import List
import tkinter
import tkinter


class InventoryService:
    def __init__(self, repository: InventoryRepository):
        # Inicializa el servicio con un repositorio de productos
        self.repository = repository

    def add_product(self, product: Product):
        # Agrega un nuevo producto al inventario, validando que no exista otro con el mismo ID
        existing_products = self.repository.get_all_products()
        if any(p.product_id == product.product_id for p in existing_products):
            raise ValueError("Product with this ID already exists.")
        self.repository.add_product(product)

    def update_product(self, product: Product):
        # Actualiza un producto existente, validando que el producto exista
        if not self.repository.get_product_by_id(product.product_id):
            raise ValueError("Product not found.")
        self.repository.update_product(product)

    def delete_product(self, product_id: str):
        # Elimina un producto del inventario, validando que el producto exista
        if not self.repository.get_product_by_id(product_id):
            raise ValueError("Product not found.")
        self.repository.delete_product(product_id)

    def get_all_products(self):
        # Obtiene la lista de todos los productos del inventario
        return self.repository.get_all_products()