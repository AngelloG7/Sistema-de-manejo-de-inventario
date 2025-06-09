# Sistema de Gestion de Inventario

## Descripción General
Este proyecto es un Sistema de Gestión de Inventario desarrollado en Python. Utiliza una arquitectura hexagonal para separar responsabilidades y mejorar el mantenimiento. El sistema permite a los usuarios gestionar productos, incluyendo agregar, actualizar, eliminar y consultar información de productos.

## Estructura del Proyecto
El proyecto está organizado en varios directorios, cada uno con un propósito específico:

- **adapters**: Contiene la implementación de la interfaz de usuario y la persistencia de datos.
  - **gui**: Implementa la interfaz gráfica de usuario utilizando Tkinter.
  - **persistence**: Implementa el almacenamiento y recuperación de datos usando archivos JSON.

- **application**: Contiene la lógica de negocio de la aplicación.
  - **services.py**: Gestiona las operaciones relacionadas con la administración de productos.
  - **dto.py**: Define los Data Transfer Objects para el intercambio de datos entre capas.

- **domain**: Contiene los modelos de negocio principales y las interfaces de los repositorios.
  - **models.py**: Define el modelo de producto y sus atributos.
  - **repository.py**: Especifica la interfaz del repositorio para el acceso a datos.

- **tests**: Contiene pruebas unitarias para la aplicación.
  - **test_services.py**: Prueba la lógica de negocio en services.py.
  - **test_repository.py**: Prueba los métodos de acceso a datos en repository.py.

- **requirements.txt**: Lista las dependencias necesarias para el proyecto.

## Instrucciones de Instalación
1. Clona el repositorio:
   ```
   git clone <repository-url>
   cd inventory-management-system
   ```

2. Instala las dependencias requeridas:
   ```
   pip install -r requirements.txt
   ```

3. Ejecuta la aplicación:
   ```
   python main.py
   ```

## Uso
Una vez que la aplicación esté en ejecución, los usuarios pueden interactuar con la interfaz gráfica para gestionar el inventario. La interfaz permite agregar nuevos productos, actualizar existentes, eliminar productos y ver el inventario actual.

## Contribuciones
¡Las contribuciones son bienvenidas! Por favor, envía un pull request o abre un issue para cualquier mejora o corrección de errores.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
