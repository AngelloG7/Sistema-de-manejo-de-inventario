from domain.models import Product
import json
import os
import tkinter

class JsonRepository:
    def __init__(self, file_path):
        # Inicializa el repositorio con la ruta del archivo JSON
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        # Verifica que el archivo exista, si no, lo crea vacío
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def load_data(self):
        # Carga los datos del archivo JSON y los convierte en objetos Product
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            return [Product(**item) for item in data]

    def save_data(self, products):
        # Guarda la lista de productos en el archivo JSON
        with open(self.file_path, 'w') as f:
            json.dump([product.__dict__ for product in products], f, indent=4)

    def add_product(self, product):
        # Agrega un nuevo producto al archivo JSON
        products = self.load_data()
        products.append(product)
        self.save_data(products)

    def update_product(self, updated_product):
        # Actualiza un producto existente en el archivo JSON
        products = self.load_data()
        for i, product in enumerate(products):
            if product.product_id == updated_product.product_id:
                products[i] = updated_product
                break
        self.save_data(products)

    def delete_product(self, product_id):
        # Elimina un producto del archivo JSON por su ID
        products = self.load_data()
        products = [product for product in products if product.product_id != product_id]
        self.save_data(products)

    def clear(self):
        # Limpia todos los productos del archivo JSON (para pruebas)
        with open(self.file_path, 'w') as f:
            json.dump([], f)

    def get_all_products(self):
        # Devuelve la lista de todos los productos almacenados
        return self.load_data()