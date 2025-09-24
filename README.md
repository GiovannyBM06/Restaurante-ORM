# Restaurante

## Autores
**Giovanny Bedoya Montes**  
**Sergio Alejandro Diosa Laverde**  
Instituto Tecnológico Metropolitano (ITM)  
Período Académico: 2025-2

## Estructura del Proyecto

El proyecto está organizado en las siguientes carpetas y archivos principales:

- `entities/`: Contiene modelos de datos (ORM) para cada entidad del restaurante (Usuario, Cliente, Empleado, Factura, Mesa, Orden, Plato, Plato_Orden, Reserva, Categoria).
- `crud/`: Clases CRUD para cada entidad, con validaciones y operaciones básicas realizadas en las bases de datos (crear, obtener, actualizar, eliminar).
- `database/`: Configuración de la base de datos y migraciones.
- `main.py`: Punto de entrada del sistema, contiene la lógica principal y menús interactivos por medio de consola.
- `README.md`: Documento de guía (Este archivo).
- `requirements.txt`: Dependencias del proyecto.

## Cómo ejecutar el sistema
Antes de continuar debes estar seguro de tener instalado Python:
	```
	py --version
	```
1. Clona el Repositorio
    ```
	git clone https://github.com/GiovannyBM06/Restaurante-ORM.git
	```
2. Instala las dependencias:
	```
	pip install -r requirements.txt
	```
    En caso de que no funcionar, instala cada dependencia individualmente  
3. Configura las variables de entorno necesarias en un archivo `.env` (verifica los parámetros requeridos en `database/config.py`).
4. Realiza las migraciones de la base de datos si es necesario (usando Alembic).
5. Ejecuta el sistema:
	```
	python main.py
	```

## Descripción de la lógica de negocio

El sistema permite gestionar un restaurante, esto a travez de un menú gráfico mostrado por medio de cosola, la gestion se da por medio de operaciones CRUD (Create, Read, Update y Delete) sobre las entidades principales:

- **Usuarios**: Representa a los administradores 
    - Permite:
        + Registro y autenticación.
        + Actualización de información personal.
        + Gestión de credenciales y contraseñas.
        + Es quien puede realizar las operaciones CRUD sobre el resto de entidades

- **Clientes**: Representa a las personas que consumen los servicios del restaurante.
    - Permite:
        + Registrar datos personales de clientes.
        + Asociar clientes con una mesa a través de una reserva.

- **Empleados**:Representa al personal del restaurante  
    - Permite: 
        + Registrar información personal, sobre su rol y salario.
        + Asociar empleados con órdenes.

- **Mesas**: Representa las mesas físicas del restaurante.
    - Permite:
        + Registrar disponibilidad de mesas.
        + Asociar mesas con las reservas de clientes.

- **Reservas**:Representa una reserva de mesa realizada por un cliente.
    - Permite:
        + Asignar mesas disponibles a clientes.
        + Controlar fechas, horarios y estado de la reserva.

- **Platos**: Representa cada uno de los platos disponibles en el restaurante.
    - Permite:
        + Registrar nombre, descripción y precio unitario.
        + Asociar platos con órdenes específicas mediante la entidad intermedia Plato_Orden.

- **Categorías**: Representa la clasificación de los platos (ej. entradas, principales, postres, bebidas).
    - Permite:
        + Asociar categorías a múltiples platos.

- **Órdenes** Representa una orden generada por un cliente (pedido).
    - Permite:
        + Asociar órdenes a una mesa y empleado que la atiende.
        + Relacionar órdenes con los platos pedidos a través de Plato_Orden.
        + Controlar estado de la orden.

- **Facturas**: Representa el documento de cobro generado a partir de una orden.
    - Registrar métodos de pago, fecha de emisión y monto total.

El sistema cuenta con menús interactivos para cada módulo, validaciones de datos y control de acceso según el tipo de usuario.