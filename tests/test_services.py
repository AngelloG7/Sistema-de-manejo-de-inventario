import unittest
import tkinter
from application.services import add_product, update_product, delete_product, get_all_products
from domain.models import Product

class TestServices(unittest.TestCase):

    def setUp(self):
        # Configura un producto de prueba antes de cada test
        self.product = Product("1", "Test Product", 10.0, 5)

    def test_add_product(self):
        # Prueba la función para agregar un producto
        result = add_product(self.product)
        self.assertTrue(result)
        self.assertIn(self.product, get_all_products())

    def test_update_product(self):
        # Prueba la función para actualizar un producto existente
        add_product(self.product)
        updated_product = Product("1", "Updated Product", 12.0, 10)
        result = update_product(updated_product)
        self.assertTrue(result)
        self.assertIn(updated_product, get_all_products())

    def test_delete_product(self):
        # Prueba la función para eliminar un producto
        add_product(self.product)
        result = delete_product("1")
        self.assertTrue(result)
        self.assertNotIn(self.product, get_all_products())

    def test_get_all_products(self):
        # Prueba la función para obtener todos los productos
        add_product(self.product)
        products = get_all_products()
        self.assertGreater(len(products), 0)

if __name__ == '__main__':
    unittest.main()