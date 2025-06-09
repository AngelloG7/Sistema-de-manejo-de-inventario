import tkinter as tk
from tkinter import Tk, ttk, messagebox
from application.services import InventoryService
from application.dto import ProductDTO
from adapters.persistence.json_repository import JsonRepository

class InventoryApp:
    def __init__(self, root):
        # Inicializa el repositorio y el servicio de inventario
        repository = JsonRepository("inventario.json")
        self.service = InventoryService(repository)

        # Inicializa la ventana principal
        self.root = root
        self.root.title("Sistema de Gestión de Inventario")
        self.root.geometry("1100x600")
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        # Configura las pestañas principales de la interfaz
        tabcontrol = ttk.Notebook(self.root)
        inventory_tab = ttk.Frame(tabcontrol)
        billing_tab = ttk.Frame(tabcontrol)
        tabcontrol.add(inventory_tab, text='Inventario')
        tabcontrol.add(billing_tab, text="Facturación")
        tabcontrol.pack(expand=1, fill="both")

        self.setup_inventory_tab(inventory_tab)
        self.setup_billing_tab(billing_tab)

    def setup_inventory_tab(self, tab):
        # Configura la pestaña de gestión de inventario
        labelFrame = ttk.LabelFrame(tab, text="Gestión de Inventario")
        labelFrame.grid(column=0, row=0, padx=12, pady=12, sticky="N")

        # Variables para los campos de entrada
        self.product_id_var = tk.StringVar()
        self.product_name_var = tk.StringVar()
        self.product_price_var = tk.StringVar()
        self.product_quantity_var = tk.StringVar()
        self.search_var = tk.StringVar()

        # Elementos de la interfaz para la gestión de inventario
        ttk.Label(labelFrame, text="ID Producto:").grid(column=0, row=0, sticky='W', pady=2)
        ttk.Entry(labelFrame, textvariable=self.product_id_var, width=25).grid(column=0, row=1, sticky='W', pady=2)
        ttk.Label(labelFrame, text="Nombre del Producto:").grid(column=0, row=2, sticky='W', pady=2)
        ttk.Entry(labelFrame, textvariable=self.product_name_var, width=25).grid(column=0, row=3, sticky='W', pady=2)
        ttk.Label(labelFrame, text="Precio de Venta:").grid(column=0, row=4, sticky='W', pady=2)
        ttk.Entry(labelFrame, textvariable=self.product_price_var, width=25).grid(column=0, row=5, sticky='W', pady=2)
        ttk.Label(labelFrame, text="Cantidad:").grid(column=0, row=6, sticky='W', pady=2)
        ttk.Entry(labelFrame, textvariable=self.product_quantity_var, width=25).grid(column=0, row=7, sticky='W', pady=2)

        # Barra de búsqueda
        ttk.Label(labelFrame, text="Buscar:").grid(column=0, row=8, sticky='W', pady=2)
        search_entry = ttk.Entry(labelFrame, textvariable=self.search_var, width=25)
        search_entry.grid(column=0, row=9, sticky='W', pady=2)
        ttk.Button(labelFrame, text='Buscar', command=self.search_products).grid(column=0, row=10, sticky='W', pady=2)

        # Botones para las acciones CRUD
        ttk.Button(labelFrame, text='Insertar', command=self.insert_product).grid(column=0, row=11, sticky='W', pady=7)
        ttk.Button(labelFrame, text='Mostrar', command=self.show_products).grid(column=0, row=11, sticky='E', padx=5)
        ttk.Button(labelFrame, text='Actualizar', command=self.update_product).grid(column=0, row=12, sticky='W', pady=2)
        ttk.Button(labelFrame, text='Eliminar', command=self.delete_product).grid(column=0, row=13, sticky='W', pady=2)
        ttk.Button(labelFrame, text='Limpiar', command=self.clear_fields).grid(column=0, row=14, sticky='W', pady=2)

        # Tabla (Treeview) para mostrar los productos del inventario
        self.tree = ttk.Treeview(labelFrame, columns=('ID Producto', 'Nombre Producto', 'Precio Venta', 'Cantidad'), height=20, show='headings')
        self.tree.heading('ID Producto', text='ID Producto')
        self.tree.heading('Nombre Producto', text='Nombre')
        self.tree.heading('Precio Venta', text='Precio Venta')
        self.tree.heading('Cantidad', text='Cantidad')
        for col in ('ID Producto', 'Nombre Producto', 'Precio Venta', 'Cantidad'):
            self.tree.column(col, anchor='center', width=110)
        self.tree.grid(row=0, column=1, rowspan=15, sticky='nsew')
        scroll_inv = ttk.Scrollbar(labelFrame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_inv.set)
        scroll_inv.grid(row=0, column=2, rowspan=15, sticky='ns')

        # Selección automática para edición
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.show_products()

    def setup_billing_tab(self, tab):
        # Variables para facturación
        self.invoice_items = []
        self.selected_product_var = tk.StringVar()
        self.invoice_quantity_var = tk.StringVar()

        labelFrame = ttk.LabelFrame(tab, text="Facturación")
        labelFrame.grid(column=0, row=0, padx=12, pady=12, sticky="N")

        # Selección de producto
        ttk.Label(labelFrame, text="Producto ID:").grid(column=0, row=0, sticky='W', pady=2)
        self.product_combo = ttk.Combobox(labelFrame, textvariable=self.selected_product_var, width=25)
        self.product_combo['values'] = [f"{p.product_id} - {p.name}" for p in self.service.get_all_products()]
        self.product_combo.grid(column=0, row=1, sticky='W', pady=2)

        ttk.Label(labelFrame, text="Cantidad:").grid(column=0, row=2, sticky='W', pady=2)
        ttk.Entry(labelFrame, textvariable=self.invoice_quantity_var, width=25).grid(column=0, row=3, sticky='W', pady=2)

        ttk.Button(labelFrame, text="Agregar a Factura", command=self.add_to_invoice).grid(column=0, row=4, sticky='W', pady=7)
        ttk.Button(labelFrame, text="Calcular Total", command=self.calculate_invoice_total).grid(column=0, row=5, sticky='W', pady=2)

        # Tabla de factura
        self.invoice_tree = ttk.Treeview(labelFrame, columns=('ID', 'Nombre', 'Precio', 'Cantidad', 'Total'), height=10, show='headings')
        for col in ('ID', 'Nombre', 'Precio', 'Cantidad', 'Total'):
            self.invoice_tree.heading(col, text=col)
            self.invoice_tree.column(col, anchor='center', width=90)
        self.invoice_tree.grid(row=0, column=1, rowspan=8, sticky='nsew')

        self.invoice_total_var = tk.StringVar()
        ttk.Label(labelFrame, text="Total Factura:").grid(column=0, row=6, sticky='W', pady=2)
        ttk.Label(labelFrame, textvariable=self.invoice_total_var).grid(column=0, row=7, sticky='W', pady=2)

    def insert_product(self):
        # Valida los campos antes de insertar
        if not self.product_id_var.get() or not self.product_name_var.get() or not self.product_price_var.get() or not self.product_quantity_var.get():
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        try:
            price = float(self.product_price_var.get())
            quantity = int(self.product_quantity_var.get())
            if price <= 0 or quantity < 0:
                messagebox.showerror("Error", "El precio debe ser mayor a 0 y la cantidad no puede ser negativa.")
                return
        except ValueError:
            messagebox.showerror("Error", "Precio y cantidad deben ser valores numéricos.")
            return
        product_dto = ProductDTO(
            product_id=self.product_id_var.get(),
            name=self.product_name_var.get(),
            price=price,
            quantity=quantity
        )
        try:
            self.service.add_product(product_dto)
            self.show_products()
            self.clear_fields()
            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_products(self):
        # Muestra todos los productos en la tabla del inventario
        products = self.service.get_all_products()
        self.tree.delete(*self.tree.get_children())
        for product in products:
            self.tree.insert('', 'end', values=(product.product_id, product.name, product.price, product.quantity))

    def update_product(self):
        # Actualiza el producto seleccionado en la tabla
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para actualizar.")
            return
        try:
            price = float(self.product_price_var.get())
            quantity = int(self.product_quantity_var.get())
            if price <= 0 or quantity < 0:
                messagebox.showerror("Error", "El precio debe ser mayor a 0 y la cantidad no puede ser negativa.")
                return
        except ValueError:
            messagebox.showerror("Error", "Precio y cantidad deben ser valores numéricos.")
            return
        product_dto = ProductDTO(
            product_id=self.product_id_var.get(),
            name=self.product_name_var.get(),
            price=price,
            quantity=quantity
        )
        try:
            self.service.update_product(product_dto)
            self.show_products()
            self.clear_fields()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_product(self):
        # Elimina el producto seleccionado en la tabla con confirmación
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar.")
            return
        item = self.tree.item(selected[0])
        product_id = item['values'][0]
        confirm = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el producto con ID {product_id}?")
        if not confirm:
            return
        try:
            self.service.delete_product(product_id)
            self.show_products()
            self.clear_fields()
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_fields(self):
        # Limpia los campos de entrada del formulario
        self.product_id_var.set("")
        self.product_name_var.set("")
        self.product_price_var.set("")
        self.product_quantity_var.set("")

    def on_tree_select(self, event):
        # Autollenado de campos al seleccionar un producto en la tabla
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            self.product_id_var.set(values[0])
            self.product_name_var.set(values[1])
            self.product_price_var.set(values[2])
            self.product_quantity_var.set(values[3])

    def search_products(self):
        # Busca productos por nombre o ID
        query = self.search_var.get().lower()
        products = self.service.get_all_products()
        filtered = [
            p for p in products
            if query in str(p.product_id).lower() or query in str(p.name).lower()
        ]
        self.tree.delete(*self.tree.get_children())
        for product in filtered:
            self.tree.insert('', 'end', values=(product.product_id, product.name, product.price, product.quantity))

    def add_to_invoice(self):
        # Agrega el producto seleccionado a la factura
        try:
            product_id = self.selected_product_var.get().split(" - ")[0]
            quantity = int(self.invoice_quantity_var.get())
            product = next((p for p in self.service.get_all_products() if p.product_id == product_id), None)
            if not product or quantity <= 0 or quantity > product.quantity:
                messagebox.showerror("Error", "Cantidad inválida o producto no disponible.")
                return
            total = product.price * quantity
            self.invoice_items.append({'id': product.product_id, 'name': product.name, 'price': product.price, 'quantity': quantity, 'total': total})
            self.refresh_invoice_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_invoice_tree(self):
        # Refresca la tabla de la factura
        self.invoice_tree.delete(*self.invoice_tree.get_children())
        for item in self.invoice_items:
            self.invoice_tree.insert('', 'end', values=(item['id'], item['name'], item['price'], item['quantity'], item['total']))

    def calculate_invoice_total(self):
        # Calcula el total de la factura
        total = sum(item['total'] for item in self.invoice_items)
        self.invoice_total_var.set(f"${total:.2f}")

def main():
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()