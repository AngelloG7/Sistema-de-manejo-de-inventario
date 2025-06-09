class InventoryRepository:
    def add_product(self, product):
        # Método para agregar un producto al repositorio
        # Debe ser implementado por una subclase
        raise NotImplementedError("This method should be overridden.")

    def update_product(self, product_id, updated_product):
        # Método para actualizar un producto existente en el repositorio
        # Debe ser implementado por una subclase
        raise NotImplementedError("This method should be overridden.")

    def delete_product(self, product_id):
        # Método para eliminar un producto del repositorio por su ID
        # Debe ser implementado por una subclase
        raise NotImplementedError("This method should be overridden.")

    def get_all_products(self):
        # Método para obtener todos los productos del repositorio
        # Debe ser implementado por una subclase
        raise NotImplementedError("This method should be overridden.")

    def get_product_by_id(self, product_id):
        # Método para obtener un producto específico por su ID
        # Debe ser implementado por una subclase
        raise NotImplementedError("This method should be overridden.")