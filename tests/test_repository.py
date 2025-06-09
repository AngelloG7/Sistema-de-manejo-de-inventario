import unittest
import tkinter
from application.services import InventoryService
from domain.models import Product
from adapters.persistence.json_repository import JsonRepository

class TestInventoryRepository(unittest.TestCase):
    def setUp(self):
        # Configura el entorno de pruebas antes de cada test
        self.repository = JsonRepository('test_inventory.json')
        self.repository.clear()  # Limpia antes de cada test para evitar datos residuales
        self.service = InventoryService(self.repository)
        self.product = Product("1", "Test Product", 10.0, 5)

    def test_add_product(self):
        # Prueba la adición de un producto al inventario
        self.service.add_product(self.product)
        products = self.service.get_all_products()
        # Compara por atributos para evitar problemas de referencia
        self.assertTrue(any(p.product_id == self.product.product_id and p.name == self.product.name for p in products))

    def test_update_product(self):
        # Prueba la actualización de un producto existente
        self.service.add_product(self.product)
        self.product.price = 12.0
        self.service.update_product(self.product)
        updated_product = next((p for p in self.service.get_all_products() if p.product_id == "1"), None)
        self.assertIsNotNone(updated_product)
        self.assertEqual(updated_product.price, 12.0)

    def test_delete_product(self):
        # Prueba la eliminación de un producto del inventario
        self.service.add_product(self.product)
        self.service.delete_product("1")
        products = self.service.get_all_products()
        self.assertFalse(any(p.product_id == self.product.product_id for p in products))

    def test_get_all_products(self):
        # Prueba la obtención de todos los productos del inventario
        self.service.add_product(self.product)
        products = self.service.get_all_products()
        self.assertEqual(len(products), 1)

    def tearDown(self):
        # Limpia los datos de prueba después de cada test
        self.repository.clear()

if __name__ == '__main__':
    unittest.main()