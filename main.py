from typing import Optional
from uuid import uuid4, UUID

from entities.Usuario import Usuario

from crud.Categoria_crud import CategoriaCRUD
from crud.Cliente_crud import ClienteCRUD
from crud.Empleado_crud import EmpleadoCRUD
from crud.Factura_crud import FacturaCRUD
from crud.Mesa_crud import MesaCRUD
from crud.Orden_crud import OrdenCRUD
from crud.Plato_crud import PlatoCRUD
from crud.Plato_Orden_crud import PlatoOrdenCRUD
from crud.Reserva_crud import ReservaCRUD
from crud.Usuario_crud import UsuarioCRUD
from database.config import SessionLocal, create_tables
from datetime import datetime


class SistemaPrincipal:
    def __init__(self):
        self.db = SessionLocal()
        self.categoria_crud = CategoriaCRUD(self.db)
        self.cliente_crud = ClienteCRUD(self.db)
        self.empleado_crud = EmpleadoCRUD(self.db)
        self.factura_crud = FacturaCRUD(self.db)
        self.mesa_crud = MesaCRUD(self.db)
        self.orden_crud = OrdenCRUD(self.db)
        self.plato_crud = PlatoCRUD(self.db)
        self.plato_orden_crud = PlatoOrdenCRUD(self.db)
        self.reserva_crud = ReservaCRUD(self.db)
        self.usuario_crud = UsuarioCRUD(self.db)
        self.usuario_actual: Optional[Usuario] = None

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.db.close()

    def pantalla_login(self) -> bool:
        print("\n" + "=" * 50)
        print("        SISTEMA DE GESTION DE PRODUCTOS")
        print("=" * 50)
        print("INICIAR SESION")
        print("=" * 50)

        intentos = 0
        max_intentos = 3

        while intentos < max_intentos:
            try:
                print(f"\nIntento {intentos + 1} de {max_intentos}")
                email_usuario = input("ingrese el correo del usuario").strip()

                if not email_usuario:
                    print("ERROR: El correo del usuario es obligatorio")
                    intentos += 1
                    continue

                contrasena = input("ingrese la contraseña").strip()

                if not contrasena:
                    print("ERROR: La contrasena es obligatoria")
                    intentos += 1
                    continue

                usuario = self.usuario_crud.autenticar_usuario(
                    email_usuario, contrasena
                )

                if usuario:
                    self.usuario_actual = usuario
                    print(f"\nEXITO: ¡Bienvenido, {usuario.nombre}!")
                    return True
                else:
                    print("ERROR: Credenciales incorrectas")
                    intentos += 1
            except Exception as e:
                print(f"ERROR: Error durante el login: {e}")
                intentos += 1

    def menu_principal_autentificado(self) -> None:
        print("\n" + "=" * 50)
        print("    SISTEMA DE GESTION DE PRODUCTOS")
        print("=" * 50)
        print(f"Usuario: {self.usuario_actual.nombre}")
        print(f"Email: {self.usuario_actual.email}")
        print("=" * 50)
        print("1. Gestion de Usuarios")
        print("2. Gestion de Categorias")
        print("3. Gestion de Clientes")
        print("4. Gestión de Empleados")
        print("5. Gestión de Facturas")
        print("6. Gestion de Mesas")
        print("7. Gestión de Orden")
        print("8. Gestion de Platos")
        print("9. Gestion de Reservas")
        print("10. Mi Perfil")
        print("0. Cerrar Sesion")
        print("=" * 50)

    def mostrar_menu_perfil(self) -> None:
        """Mostrar menu de perfil del usuario"""
        while True:
            print("\n" + "-" * 30)
            print("   MI PERFIL")
            print("-" * 30)
            print("1. Ver Informacion Personal")
            print("2. Actualizar Informacion")
            print("3. Cambiar Contrasena")
            print("0. Volver al menu principal")

            opcion = input("\nSeleccione una opcion: ").strip()

            if opcion == "1":
                self.ver_informacion_usuario()
            elif opcion == "2":
                self.actualizar_informacion_usuario()
            elif opcion == "3":
                self.cambiar_contrasena()
            elif opcion == "0":
                break
            else:
                print("ERROR: Opcion invalida. Intente nuevamente.")

    def ver_informacion_usuario(self) -> None:
        """Ver informacion del usuario"""
        try:
            print(f"\n--- INFORMACION PERSONAL ---")
            print(f"Nombre: {self.usuario_actual.nombre}")
            print(f"Apellido: {self.usuario_actual.apellido}")
            print(f"Email: {self.usuario_actual.email}")
            print(f"Fecha de creacion: {self.usuario_actual.fecha_creacion}")

        except Exception as e:
            print(f"ERROR: Error: {e}")

    def actualizar_informacion_usuario(self) -> None:
        """Actualizar informacion personal del usuario"""
        try:
            print(f"\n--- ACTUALIZAR INFORMACION PERSONAL ---")
            print("Deje en blanco para mantener el valor actual")

            nuevo_nombre = input(
                f"Nombre actual ({self.usuario_actual.nombre}): "
            ).strip()
            nuevo_apellido = input(
                f"Apellido actual ({self.usuario_actual.apellido}): "
            ).strip()
            nuevo_email = input(f"Email actual ({self.usuario_actual.email}): ").strip()

            cambios = {}
            if nuevo_nombre:
                cambios["nombre"] = nuevo_nombre
            if nuevo_apellido:
                cambios["apellido"] = nuevo_apellido
            if nuevo_email:
                cambios["email"] = nuevo_email

            if cambios:
                usuario_actualizado = self.usuario_crud.actualizar_usuario(
                    self.usuario_actual.id, **cambios
                )
                if usuario_actualizado:
                    self.usuario_actual = usuario_actualizado
                    print(f"EXITO: Informacion actualizada exitosamente")
                else:
                    print("ERROR: Error al actualizar la informacion")
            else:
                print("INFO: No se realizaron cambios.")

        except ValueError as e:
            print(f"ERROR: Error: {e}")
        except Exception as e:
            print(f"ERROR: Error inesperado: {e}")

    def cambiar_contrasena(self) -> None:
        """Cambiar contraseña del usuario autenticado"""
        try:
            print("\n--- CAMBIAR CONTRASEÑA ---")
            contrasena_actual = input("Ingrese su contraseña actual: ").strip()
            contrasena_nueva = input("Ingrese la nueva contraseña: ").strip()
            confirmar_nueva = input("Confirme la nueva contraseña: ").strip()

            if not contrasena_actual or not contrasena_nueva or not confirmar_nueva:
                print("ERROR: Todos los campos son obligatorios.")
                return

            if contrasena_nueva != confirmar_nueva:
                print("ERROR: Las contraseñas nuevas no coinciden.")
                return

            self.usuario_crud.cambiar_contraseña(
                self.usuario_actual.id, contrasena_actual, contrasena_nueva
            )
            print("ÉXITO: Contraseña cambiada correctamente.")
        except ValueError as e:
            print(f"ERROR: {e}")
        except Exception as e:
            print(f"ERROR inesperado: {e}")

    def mostrar_menu_usuarios(self) -> None:
        """Mostrar menu de gestion de usuarios"""
        while True:
            print("\n" + "-" * 30)
            print("   GESTION DE USUARIOS")
            print("-" * 30)
            print("1. Crear Usuario")
            print("2. Listar Usuarios")
            print("3. Buscar Usuario por Email")
            print("4. Buscar Usuario por Nombre de Usuario")
            print("5. Actualizar Usuario")
            print("6. Eliminar Usuario")
            print("0. Volver al menu principal")

            opcion = input("\nSeleccione una opcion: ").strip()

            if opcion == "1":
                self.crear_usuario()
            elif opcion == "2":
                self.listar_usuarios()
            elif opcion == "3":
                self.buscar_usuario_por_email()
            elif opcion == "4":
                self.buscar_usuarios_por_nombre()
            elif opcion == "5":
                self.actualizar_usuario()
            elif opcion == "6":
                self.eliminar_usuario()
            elif opcion == "0":
                break
            else:
                print("ERROR: Opcion invalida. Intente nuevamente.")

    def crear_usuario(self) -> None:
        """Crear un nuevo usuario"""
        try:
            print("\n--- CREAR USUARIO ---")
            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            email = input("Email: ").strip()
            contrasena = input("Contraseña: ").strip()

            usuario = self.usuario_crud.crear_usuario(
                nombre=nombre, apellido=apellido, email=email, contraseña=contrasena
            )

            print(f"EXITO: Usuario creado exitosamente: {usuario}")

        except ValueError as e:
            print(f"ERROR: Error: {e}")
        except Exception as e:
            print(f"ERROR: Error inesperado: {e}")

    def listar_usuarios(self) -> None:
        """Listar todos los usuarios"""
        try:
            usuarios = self.usuario_crud.obtener_usuarios()
            if not usuarios:
                print("INFO: No hay usuarios registrados.")
                return

            print(f"\n--- USUARIOS ({len(usuarios)}) ---")
            for i, usuario in enumerate(usuarios, 1):
                print(f"{i}. {usuario.nombre} ({usuario.apellido}) - {usuario.email}")

        except Exception as e:
            print(f"ERROR: Error: {e}")

    def buscar_usuario_por_email(self) -> None:
        """Buscar usuario por email"""
        try:
            email = input("\nIngrese el email a buscar: ").strip()
            usuario = self.usuario_crud.obtener_usuario_con_email(email)

            if usuario:
                print(f"EXITO: Usuario encontrado:")
                print(f"   Nombre: {usuario.nombre}")
                print(f"   Apellido : {usuario.apellido}")
                print(f"   Email: {usuario.email}")
            else:
                print("ERROR: Usuario no encontrado.")

        except Exception as e:
            print(f"ERROR: Error: {e}")

    def buscar_usuarios_por_nombre(self) -> None:
        """Buscar y mostrar todos los usuarios por nombre"""
        try:
            nombre = input("\nIngrese el nombre a buscar: ").strip()
            usuarios = self.usuario_crud.obtener_usuarios_con_nombre(nombre)
            if usuarios:
                print(f"EXITO: Usuarios encontrados con el nombre '{nombre}':")
                for i, usuario in enumerate(usuarios, 1):
                    print(f"{i}. {usuario.nombre} {usuario.apellido} - {usuario.email}")
            else:
                print("ERROR: No se encontraron usuarios con ese nombre.")
        except Exception as e:
            print(f"ERROR: Error: {e}")

    def actualizar_usuario(self) -> None:
        """Actualizar un usuario"""
        try:
            email = input("\nIngrese el email del usuario a actualizar: ").strip()
            usuario = self.usuario_crud.obtener_usuario_con_email(email)

            if not usuario:
                print("ERROR: Usuario no encontrado.")
                return

            print(f"\nActualizando usuario: {usuario.nombre}")
            print("Deje en blanco para mantener el valor actual")

            nuevo_nombre = input(f"Nombre actual ({usuario.nombre}): ").strip()
            nuevo_nombre_usuario = input(
                f"Apellido actual ({usuario.apellido}): "
            ).strip()
            nuevo_email = input(f"Email actual ({usuario.email}): ").strip()

            cambios = {}
            if nuevo_nombre:
                cambios["nombre"] = nuevo_nombre
            if nuevo_nombre_usuario:
                cambios["nombre_usuario"] = nuevo_nombre_usuario
            if nuevo_email:
                cambios["email"] = nuevo_email

            if cambios:
                usuario_actualizado = self.usuario_crud.actualizar_usuario(
                    usuario.id, **cambios
                )
                print(f"EXITO: Usuario actualizado: {usuario_actualizado}")
            else:
                print("INFO: No se realizaron cambios.")

        except ValueError as e:
            print(f"ERROR: Error: {e}")
        except Exception as e:
            print(f"ERROR: Error inesperado: {e}")

    def eliminar_usuario(self) -> None:
        try:
            email = input("\nIngrese el email del usuario a eliminar: ").strip()
            usuario = self.usuario_crud.obtener_usuario_con_email(email)
            if not usuario:
                print("ERROR: Usuario no encontrado.")
                return
            confirm = (
                input(
                    f"¿Seguro que deseas eliminar a {usuario.nombre} {usuario.apellido}? (s/n): "
                )
                .strip()
                .lower()
            )
            if confirm == "s":
                eliminado = self.usuario_crud.eliminar_usuario(usuario.id)
                if eliminado:
                    print("ÉXITO: Usuario eliminado.")
                else:
                    print("ERROR: No se pudo eliminar el usuario.")
            else:
                print("INFO: Operación cancelada.")
        except Exception as e:
            print(f"ERROR: Error: {e}")

    def mostrar_menu_categorias(self) -> None:
        """Mostrar menú de gestión de categorías"""
        while True:
            print("\n" + "-" * 30)
            print("   GESTIÓN DE CATEGORÍAS")
            print("-" * 30)
            print("1. Crear Categoría")
            print("2. Listar Categorías")
            print("3. Buscar Categoría por ID")
            print("4. Actualizar Categoría")
            print("5. Eliminar Categoría")
            print("0. Volver al menú principal")

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                self.crear_categoria()
            elif opcion == "2":
                self.listar_categorias()
            elif opcion == "3":
                self.buscar_categoria_por_id()
            elif opcion == "4":
                self.actualizar_categoria()
            elif opcion == "5":
                self.eliminar_categoria()
            elif opcion == "0":
                break
            else:
                print("ERROR: Opción inválida. Intente nuevamente.")

    def crear_categoria(self) -> None:
        """Crear una nueva categoría"""
        try:
            print("\n--- CREAR CATEGORÍA ---")
            nombre = input("Nombre: ").strip()
            descripcion = input("Descripción (opcional): ").strip() or None
            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return
            id_usuario = self.usuario_actual.id

            categoria = self.categoria_crud.crear_categoria(
                nombre=nombre, descripcion=descripcion, id_usuario=id_usuario
            )

            print(f"ÉXITO: Categoría creada exitosamente: {categoria}")

        except ValueError as e:
            print(f"ERROR: {e}")
        except Exception as e:
            print(f"ERROR inesperado: {e}")

    def listar_categorias(self) -> None:
        """Listar todas las categorías"""
        try:
            categorias = self.categoria_crud.obtener_categorias()
            if not categorias:
                print("INFO: No hay categorías registradas.")
                return

            print(f"\n--- CATEGORÍAS ({len(categorias)}) ---")
            for i, categoria in enumerate(categorias, 1):
                print(
                    f"{i}. ID: {categoria.id} | {categoria.nombre} - {categoria.descripcion}"
                )

        except Exception as e:
            print(f"ERROR: {e}")

    def buscar_categoria_por_id(self) -> None:
        """Buscar una categoría por su ID"""
        try:
            categoria_id = input("\nIngrese el ID de la categoría: ").strip()
            categoria = self.categoria_crud.obtener_categoria(UUID(categoria_id))

            if categoria:
                print(f"ÉXITO: Categoría encontrada:")
                print(f"   ID: {categoria.id}")
                print(f"   Nombre: {categoria.nombre}")
                print(f"   Descripción: {categoria.descripcion}")
            else:
                print("ERROR: Categoría no encontrada.")

        except Exception as e:
            print(f"ERROR: {e}")

    def actualizar_categoria(self) -> None:
        """Actualizar una categoría"""
        try:
            categoria_id = input(
                "\nIngrese el ID de la categoría a actualizar: "
            ).strip()
            categoria = self.categoria_crud.obtener_categoria(UUID(categoria_id))

            if not categoria:
                print("ERROR: Categoría no encontrada.")
                return

            print(f"\nActualizando categoría: {categoria.nombre}")
            print("Deje en blanco para mantener el valor actual")

            nuevo_nombre = input(f"Nombre actual ({categoria.nombre}): ").strip()
            nueva_descripcion = input(
                f"Descripción actual ({categoria.descripcion}): "
            ).strip()

            cambios = {}
            if nuevo_nombre:
                cambios["nombre"] = nuevo_nombre
            if nueva_descripcion:
                cambios["descripcion"] = nueva_descripcion

            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return
            id_usuario_mod = self.usuario_actual.id

            if cambios:
                categoria_actualizada = self.categoria_crud.actualizar_categoria(
                    categoria.id,id_usuario_mod ,**cambios
                )
                print(f"ÉXITO: Categoría actualizada: {categoria_actualizada}")
            else:
                print("INFO: No se realizaron cambios.")

        except ValueError as e:
            print(f"ERROR: {e}")
        except Exception as e:
            print(f"ERROR inesperado: {e}")

    def eliminar_categoria(self) -> None:
        """Eliminar una categoría"""
        try:
            categoria_id = input("\nIngrese el ID de la categoría a eliminar: ").strip()
            confirm = input("¿Seguro que deseas eliminarla? (s/n): ").strip().lower()

            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return

            if confirm == "s":
                eliminado = self.categoria_crud.eliminar_categoria(UUID(categoria_id))
                if eliminado:
                    print("ÉXITO: Categoría eliminada.")
                else:
                    print("ERROR: Categoría no encontrada.")
            else:
                print("INFO: Operación cancelada.")

        except Exception as e:
            print(f"ERROR: {e}")

    def mostrar_menu_clientes(self) -> None:
        """Mostrar menú de gestión de clientes"""
        while True:
            print("\n" + "-" * 30)
            print("   GESTIÓN DE CLIENTES")
            print("-" * 30)
            print("1. Crear Cliente")
            print("2. Listar Clientes")
            print("3. Buscar Cliente por ID")
            print("4. Actualizar Cliente")
            print("5. Eliminar Cliente")
            print("0. Volver al menú principal")

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                self.crear_cliente()
            elif opcion == "2":
                self.listar_clientes()
            elif opcion == "3":
                self.buscar_cliente_por_id()
            elif opcion == "4":
                self.actualizar_cliente()
            elif opcion == "5":
                self.eliminar_cliente()
            elif opcion == "0":
                break
            else:
                print("ERROR: Opción inválida. Intente nuevamente.")

    def crear_cliente(self) -> None:
        """Crear un nuevo cliente"""
        try:
            print("\n--- CREAR CLIENTE ---")
            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            email = input("Email: ").strip()
            telefono = input("Teléfono: ").strip()

            usuarios = self.usuario_crud.obtener_usuarios()
            if not usuarios:
                print("ERROR: No hay usuarios registrados.")
                return
            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return
            id_usuario = self.usuario_actual.id

            cliente = self.cliente_crud.crear_cliente(
                nombre=nombre,
                apellido=apellido,
                Email=email,
                telefono=telefono,
                id_usuario=self.usuario_actual.id,
            )

            print(f"ÉXITO: Cliente creado exitosamente: {cliente}")

        except ValueError as e:
            print(f"ERROR: {e}")
        except Exception as e:
            print(f"ERROR inesperado: {e}")

    def listar_clientes(self) -> None:
        """Listar todos los clientes"""
        try:
            clientes = self.cliente_crud.obtener_clientes()
            if not clientes:
                print("INFO: No hay clientes registrados.")
                return

            print(f"\n--- CLIENTES ({len(clientes)}) ---")
            for i, cliente in enumerate(clientes, 1):
                print(
                    f"{i}. ID: {cliente.id} | {cliente.nombre} {cliente.apellido} "
                    f"- {cliente.Email} | Tel: {cliente.telefono}"
                )

        except Exception as e:
            print(f"ERROR: {e}")

    def buscar_cliente_por_id(self) -> None:
        """Buscar un cliente por su ID"""
        try:
            cliente_id = input("\nIngrese el ID del cliente: ").strip()
            cliente = self.cliente_crud.obtener_cliente(UUID(cliente_id))

            if cliente:
                print("ÉXITO: Cliente encontrado:")
                print(f"   ID: {cliente.id}")
                print(f"   Nombre: {cliente.nombre}")
                print(f"   Apellido: {cliente.apellido}")
                print(f"   Email: {cliente.Email}")
                print(f"   Teléfono: {cliente.telefono}")
            else:
                print("ERROR: Cliente no encontrado.")

        except Exception as e:
            print(f"ERROR: {e}")

    def actualizar_cliente(self) -> None:
        """Actualizar un cliente"""
        try:
            cliente_id = input("\nIngrese el ID del cliente a actualizar: ").strip()
            cliente = self.cliente_crud.obtener_cliente(UUID(cliente_id))

            if not cliente:
                print("ERROR: Cliente no encontrado.")
                return

            print(f"\nActualizando cliente: {cliente.nombre} {cliente.apellido}")
            print("Deje en blanco para mantener el valor actual")

            nuevo_nombre = input(f"Nombre actual ({cliente.nombre}): ").strip()
            nuevo_apellido = input(f"Apellido actual ({cliente.apellido}): ").strip()
            nuevo_email = input(f"Email actual ({cliente.Email}): ").strip()
            nuevo_telefono = input(f"Teléfono actual ({cliente.telefono}): ").strip()

            cambios = {}
            if nuevo_nombre:
                cambios["nombre"] = nuevo_nombre
            if nuevo_apellido:
                cambios["apellido"] = nuevo_apellido
            if nuevo_email:
                cambios["Email"] = nuevo_email
            if nuevo_telefono:
                cambios["telefono"] = nuevo_telefono

            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return
            id_usuario_mod = self.usuario_actual.id

            if cambios:
                cliente_actualizado = self.cliente_crud.actualizar_cliente(
                    cliente.id, id_usuario_mod,**cambios
                )
                print(f"ÉXITO: Cliente actualizado: {cliente_actualizado}")
            else:
                print("INFO: No se realizaron cambios.")

        except ValueError as e:
            print(f"ERROR: {e}")
        except Exception as e:
            print(f"ERROR inesperado: {e}")

    def eliminar_cliente(self) -> None:
        """Eliminar un cliente"""
        try:
            cliente_id = input("\nIngrese el ID del cliente a eliminar: ").strip()
            confirm = input("¿Seguro que deseas eliminarlo? (s/n): ").strip().lower()

            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return

            if confirm == "s":
                eliminado = self.cliente_crud.eliminar_cliente(UUID(cliente_id))
                if eliminado:
                    print("ÉXITO: Cliente eliminado.")
                else:
                    print("ERROR: Cliente no encontrado.")
            else:
                print("INFO: Operación cancelada.")

        except Exception as e:
            print(f"ERROR: {e}")

    def mostrar_menu_empleados(self):
        """Mostrar menú de gestión de empleados"""
        while True:
            print("\n" + "-" * 30)
            print("   GESTIÓN DE EMPLEADOS")
            print("-" * 30)
            print("1. Crear Empleado")
            print("2. Listar Empleados")
            print("3. Buscar Empleado por ID")
            print("4. Actualizar Empleado")
            print("5. Eliminar Empleado")
            print("0. Volver al menú principal")

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                self.crear_empleado()
            elif opcion == "2":
                self.listar_empleados()
            elif opcion == "3":
                self.buscar_empleado()
            elif opcion == "4":
                self.actualizar_empleado()
            elif opcion == "5":
                self.eliminar_empleado()
            elif opcion == "0":
                break
            else:
                print("ERROR: Opción inválida. Intente nuevamente.")

    def crear_empleado(self):
        """Crear un nuevo empleado"""
        try:
            print("\n--- CREAR EMPLEADO ---")
            usuarios = self.usuario_crud.obtener_usuarios()
            if not usuarios:
                print("ERROR: No hay usuarios registrados.")
                return
            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return
            id_usuario = self.usuario_actual.id
            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            rol = input("Rol: ").strip()
            salario = float(input("Salario: ").strip())

            empleado = self.empleado_crud.crear_empleado(
                nombre=nombre,
                apellido=apellido,
                rol=rol,
                salario=salario,
                id_usuario=id_usuario,
            )
            print(f"ÉXITO: Empleado creado -> {empleado.nombre} {empleado.apellido}")

        except ValueError as e:
            print(f"ERROR: {e}")
        except Exception as e:
            print(f"ERROR: {e}")

    def listar_empleados(self):
        """Listar todos los empleados"""
        try:
            empleados = self.empleado_crud.obtener_empleados()
            if not empleados:
                print("INFO: No hay empleados registrados.")
                return
            print(f"\n--- EMPLEADOS ({len(empleados)}) ---")
            for i, emp in enumerate(empleados, 1):
                print(
                    f"{i}. {emp.id} - {emp.nombre} {emp.apellido}, Rol: {emp.rol}, Salario: {emp.salario}"
                )
        except Exception as e:
            print(f"ERROR: {e}")

    def buscar_empleado(self):
        """Buscar empleado por ID"""
        try:
            emp_id = input("Ingrese el ID del empleado a buscar: ").strip()
            empleado = self.empleado_crud.obtener_empleado(emp_id)
            if empleado:
                print(
                    f"Empleado encontrado: {empleado.nombre} {empleado.apellido}, Rol: {empleado.rol}"
                )
            else:
                print("ERROR: Empleado no encontrado.")
        except Exception as e:
            print(f"ERROR: {e}")

    def actualizar_empleado(self):
        """Actualizar un empleado"""
        try:
            emp_id = input("Ingrese el ID del empleado a actualizar: ").strip()
            empleado = self.empleado_crud.obtener_empleado(emp_id)
            if not empleado:
                print("ERROR: Empleado no encontrado.")
                return

            print(f"\nActualizando empleado: {empleado.nombre} {empleado.apellido}")
            nuevo_nombre = input(f"Nuevo nombre (actual: {empleado.nombre}): ").strip()
            nuevo_apellido = input(
                f"Nuevo apellido (actual: {empleado.apellido}): "
            ).strip()
            nuevo_rol = input(f"Nuevo rol (actual: {empleado.rol}): ").strip()
            nuevo_salario = input(
                f"Nuevo salario (actual: {empleado.salario}): "
            ).strip()

            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return
            id_usuario_mod = self.usuario_actual.id

            cambios = {}
            if nuevo_nombre:
                cambios["nombre"] = nuevo_nombre
            if nuevo_apellido:
                cambios["apellido"] = nuevo_apellido
            if nuevo_rol:
                cambios["rol"] = nuevo_rol
            if nuevo_salario:
                cambios["salario"] = float(nuevo_salario)

            if cambios:
                actualizado = self.empleado_crud.actualizar_empleado(emp_id,id_usuario_mod, **cambios)
                print(
                    f"ÉXITO: Empleado actualizado -> {actualizado.nombre} {actualizado.apellido}"
                )
            else:
                print("INFO: No se realizaron cambios.")

        except Exception as e:
            print(f"ERROR: {e}")

    def eliminar_empleado(self):
        """Eliminar un empleado"""
        try:
            emp_id = input("Ingrese el ID del empleado a eliminar: ").strip()
            eliminado = self.empleado_crud.eliminar_empleado(emp_id)
            if eliminado:
                print("ÉXITO: Empleado eliminado.")
            else:
                print("ERROR: Empleado no encontrado.")
        except Exception as e:
            print(f"ERROR: {e}")

    def mostrar_menu_mesas(self):
        while True:
            print("\n" + "-" * 30)
            print("   GESTIÓN DE MESAS")
            print("-" * 30)
            print("1. Crear Mesa")
            print("2. Listar Mesas")
            print("3. Buscar Mesa por ID")
            print("4. Actualizar Mesa")
            print("5. Eliminar Mesa")
            print("0. Volver al menú principal")

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                self.crear_mesa()
            elif opcion == "2":
                self.listar_mesas()
            elif opcion == "3":
                self.buscar_mesa()
            elif opcion == "4":
                self.actualizar_mesa()
            elif opcion == "5":
                self.eliminar_mesa()
            elif opcion == "0":
                break
            else:
                print("ERROR: Opción inválida. Intente nuevamente.")

    def crear_mesa(self):
        try:
            print("\n--- CREAR MESA ---")
            capacidad = int(input("Capacidad: ").strip())

            usuarios = self.usuario_crud.obtener_usuarios()
            if not usuarios:
                print("ERROR: No hay usuarios registrados.")
                return
            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return
            id_usuario = self.usuario_actual.id

            mesa = self.mesa_crud.crear_mesa(
                 capacidad=capacidad, id_usuario=id_usuario
            )
            print(
                f"ÉXITO: Mesa creada -> Capacidad {mesa.capacidad}"
            )

        except ValueError as e:
            print(f"ERROR: {e}")
        except Exception as e:
            print(f"ERROR inesperado: {e}")

    def listar_mesas(self):
        try:
            mesas = self.mesa_crud.obtener_mesas()
            if not mesas:
                print("INFO: No hay mesas registradas.")
                return

            print(f"\n--- MESAS ({len(mesas)}) ---")
            for i, mesa in enumerate(mesas, 1):
                print(
                    f"{i}. ID: {mesa.id} | Capacidad: {mesa.capacidad}"
                )

        except Exception as e:
            print(f"ERROR: {e}")

    def buscar_mesa(self):
        try:
            mesa_id = input("Ingrese el ID de la mesa: ").strip()
            mesa = self.mesa_crud.obtener_mesa(mesa_id)
            if mesa:
                print(
                    f"Mesa encontrada -> ID: {mesa.id}, Capacidad: {mesa.capacidad}"
                )
            else:
                print("ERROR: Mesa no encontrada.")
        except Exception as e:
            print(f"ERROR: {e}")

    def actualizar_mesa(self):
        try:
            mesa_id = input("Ingrese el ID de la mesa a actualizar: ").strip()
            mesa = self.mesa_crud.obtener_mesa(mesa_id)
            if not mesa:
                print("ERROR: Mesa no encontrada.")
                return
            nueva_capacidad = input(
                f"Nueva capacidad (actual: {mesa.capacidad}): "
            ).strip()
            cambios = {}
            if nueva_capacidad:
                cambios["capacidad"] = int(nueva_capacidad)
            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return
            id_usuario_mod = self.usuario_actual.id
            
            if cambios:
                mesa_actualizada = self.mesa_crud.actualizar_mesa(mesa_id, id_usuario_mod, **cambios)
                print(
                    f"ÉXITO: Mesa actualizada -> Capacidad {mesa_actualizada.capacidad}"
                )
            else:
                print("INFO: No se realizaron cambios.")

        except ValueError as e:
            print(f"ERROR: {e}")
        except Exception as e:
            print(f"ERROR inesperado: {e}")

    def eliminar_mesa(self):
        try:
            mesa_id = input("Ingrese el ID de la mesa a eliminar: ").strip()
            confirm = input("¿Seguro que deseas eliminarla? (s/n): ").strip().lower()

            if confirm == "s":
                eliminado = self.mesa_crud.eliminar_mesa(mesa_id)
                if eliminado:
                    print("ÉXITO: Mesa eliminada.")
                else:
                    print("ERROR: Mesa no encontrada.")
            else:
                print("INFO: Operación cancelada.")

        except Exception as e:
            print(f"ERROR: {e}")

    def mostrar_menu_facturas(self):
        while True:
            print("\n" + "-" * 30)
            print("   GESTIÓN DE FACTURAS")
            print("-" * 30)
            print("1. Crear Factura")
            print("2. Listar Facturas")
            print("3. Buscar Factura por ID")
            print("4. Actualizar Factura")
            print("5. Eliminar Factura")
            print("0. Volver al menú principal")

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                self.crear_factura()
            elif opcion == "2":
                self.listar_facturas()
            elif opcion == "3":
                self.buscar_factura()
            elif opcion == "4":
                self.actualizar_factura()
            elif opcion == "5":
                self.eliminar_factura()
            elif opcion == "0":
                break
            else:
                print("ERROR: Opción inválida. Intente nuevamente.")

    def crear_factura(self):
        try:
            print("\n--- CREAR FACTURA ---")

            ordenes = self.orden_crud.obtener_ordenes()
            if not ordenes:
                print("ERROR: No hay ordenes registradas.")
                return
            print("\n--- ORDENES ---")
            for i, orden in enumerate(ordenes, 1):
                print(f"{i}. ID: {orden.id} | {orden.estado}")
            cliente_id = input("Ingrese el ID de la orden: ").strip()

            usuarios = self.usuario_crud.obtener_usuarios()
            if not usuarios:
                print("ERROR: No hay usuarios registrados.")
                return
            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return
            id_usuario = self.usuario_actual.id

            total = float(input("Total de la factura: ").strip())

            factura = self.factura_crud.crear_factura(
                id_cliente=cliente_id, id_usuario=id_usuario, total=total
            )
            print(f"ÉXITO: Factura creada -> ID {factura.id}, Total {factura.total}")

        except ValueError as e:
            print(f"ERROR: {e}")
        except Exception as e:
            print(f"ERROR inesperado: {e}")

    def listar_facturas(self):
        try:
            facturas = self.factura_crud.obtener_facturas()
            if not facturas:
                print("INFO: No hay facturas registradas.")
                return

            print(f"\n--- FACTURAS ({len(facturas)}) ---")
            for i, factura in enumerate(facturas, 1):
                print(
                    f"{i}. ID: {factura.id} | Cliente: {factura.id_cliente} | Total: {factura.total}"
                )

        except Exception as e:
            print(f"ERROR: {e}")

    def buscar_factura(self):
        try:
            factura_id = input("Ingrese el ID de la factura: ").strip()
            factura = self.factura_crud.obtener_factura(factura_id)
            if factura:
                print(
                    f"Factura encontrada -> ID: {factura.id}, Cliente: {factura.id_cliente}, Total: {factura.total}"
                )
            else:
                print("ERROR: Factura no encontrada.")
        except Exception as e:
            print(f"ERROR: {e}")

    def actualizar_factura(self):
        try:
            factura_id = input("Ingrese el ID de la factura a actualizar: ").strip()
            factura = self.factura_crud.obtener_factura(factura_id)
            if not factura:
                print("ERROR: Factura no encontrada.")
                return

            print(f"\nActualizando factura ID {factura.id}")
            nuevo_total = input(f"Nuevo total (actual: {factura.total}): ").strip()

            cambios = {}
            if nuevo_total:
                cambios["total"] = float(nuevo_total)
            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return
            id_usuario_mod = self.usuario_actual.id

            if cambios:
                factura_actualizada = self.factura_crud.actualizar_factura(
                    factura_id, id_usuario_mod,**cambios
                )
                print(
                    f"ÉXITO: Factura actualizada -> ID: {factura_actualizada.id}, Total: {factura_actualizada.total}"
                )
            else:
                print("INFO: No se realizaron cambios.")

        except ValueError as e:
            print(f"ERROR: {e}")
        except Exception as e:
            print(f"ERROR inesperado: {e}")

    def eliminar_factura(self):
        try:
            factura_id = input("Ingrese el ID de la factura a eliminar: ").strip()
            confirm = input("¿Seguro que deseas eliminarla? (s/n): ").strip().lower()

            if confirm == "s":
                eliminado = self.factura_crud.eliminar_factura(factura_id)
                if eliminado:
                    print("ÉXITO: Factura eliminada.")
                else:
                    print("ERROR: Factura no encontrada.")
            else:
                print("INFO: Operación cancelada.")

        except Exception as e:
            print(f"ERROR: {e}")

    def mostrar_menu_ordenes(self):
        while True:
            print("\n" + "-" * 30)
            print("   GESTIÓN DE ÓRDENES")
            print("-" * 30)
            print("1. Crear Orden")
            print("2. Listar Órdenes")
            print("3. Buscar Orden por ID")
            print("4. Actualizar Orden")
            print("5. Eliminar Orden")
            print("0. Volver al menú principal")

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                self.crear_orden()
            elif opcion == "2":
                self.listar_ordenes()
            elif opcion == "3":
                self.buscar_orden()
            elif opcion == "4":
                self.actualizar_orden()
            elif opcion == "5":
                self.eliminar_orden()
            elif opcion == "0":
                break
            else:
                print("ERROR: Opción inválida. Intente nuevamente.")

    def crear_orden(self):
        """Crear una nueva orden"""
        try:
            print("\n--- CREAR ORDEN ---")

            """Mostrar mesas disponibles"""
            mesas = self.mesa_crud.obtener_mesas()
            if not mesas:
                print("ERROR: No hay mesas registradas.")
                return
            print("\n--- MESAS DISPONIBLES ---")
            for i, mesa in enumerate(mesas, 1):
                print(f"{i}. ID: {mesa.id} | Capacidad: {mesa.capacidad}")
            id_mesa = input("Ingrese el ID de la mesa: ").strip()

            """Mostrar empleados disponibles"""
            empleados = self.empleado_crud.obtener_empleados()
            if not empleados:
                print("ERROR: No hay empleados registrados.")
                return
            print("\n--- EMPLEADOS DISPONIBLES ---")
            for i, empleado in enumerate(empleados, 1):
                print(f"{i}. ID: {empleado.id} | {empleado.nombre} {empleado.apellido}")
            id_empleado = input("Ingrese el ID del empleado: ").strip()

            """Mostrar usuarios disponibles"""
            usuarios = self.usuario_crud.obtener_usuarios()
            if not usuarios:
                print("ERROR: No hay usuarios registrados.")
                return
            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return
            id_usuario = self.usuario_actual.id
            estado = input(
                "Estado (Pendiente/En Proceso/Completada/Cancelada): "
            ).strip()

            orden = self.orden_crud.crear_orden(
                estado=estado,
                id_mesa=id_mesa,
                id_empleado=id_empleado,
                id_usuario=id_usuario,
            )
            print(f"ÉXITO: Orden creada -> ID {orden.id}, Estado: {orden.estado}")

        except ValueError as e:
            print(f"ERROR: {e}")
        except Exception as e:
            print(f"ERROR inesperado: {e}")

    def listar_ordenes(self):
        try:
            ordenes = self.orden_crud.obtener_ordenes()
            if not ordenes:
                print("INFO: No hay órdenes registradas.")
                return

            print(f"\n--- ÓRDENES ({len(ordenes)}) ---")
            for i, orden in enumerate(ordenes, 1):
                print(
                    f"{i}. ID: {orden.id} | Mesa: {orden.id_mesa} | Empleado: {orden.id_empleado} | Estado: {orden.estado}"
                )

        except Exception as e:
            print(f"ERROR: {e}")

    def buscar_orden(self):
        try:
            orden_id = input("Ingrese el ID de la orden: ").strip()
            orden = self.orden_crud.obtener_orden(orden_id)
            if orden:
                print(
                    f"Orden encontrada -> ID: {orden.id}, Mesa: {orden.id_mesa}, Empleado: {orden.id_empleado}, Estado: {orden.estado}"
                )
            else:
                print("ERROR: Orden no encontrada.")
        except Exception as e:
            print(f"ERROR: {e}")

    def actualizar_orden(self):
        try:
            orden_id = input("Ingrese el ID de la orden a actualizar: ").strip()
            orden = self.orden_crud.obtener_orden(orden_id)
            if not orden:
                print("ERROR: Orden no encontrada.")
                return

            print(f"\nActualizando orden ID {orden.id}")
            nuevo_estado = input(f"Nuevo estado (actual: {orden.estado}): ").strip()

            cambios = {}
            if nuevo_estado:
                cambios["estado"] = nuevo_estado
            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return
            id_usuario_mod = self.usuario_actual.id
            if cambios:
                orden_actualizada = self.orden_crud.actualizar_orden(
                    orden_id, id_usuario_mod,**cambios
                )
                print(
                    f"ÉXITO: Orden actualizada -> ID: {orden_actualizada.id}, Estado: {orden_actualizada.estado}"
                )
            else:
                print("INFO: No se realizaron cambios.")

        except ValueError as e:
            print(f"ERROR: {e}")
        except Exception as e:
            print(f"ERROR inesperado: {e}")

    def eliminar_orden(self):
        try:
            orden_id = input("Ingrese el ID de la orden a eliminar: ").strip()
            confirm = input("¿Seguro que deseas eliminarla? (s/n): ").strip().lower()

            if confirm == "s":
                eliminado = self.orden_crud.eliminar_orden(orden_id)
                if eliminado:
                    print("ÉXITO: Orden eliminada.")
                else:
                    print("ERROR: Orden no encontrada.")
            else:
                print("INFO: Operación cancelada.")

        except Exception as e:
            print(f"ERROR: {e}")

        """Eliminar una factura"""
        try:
            factura_id = input("\nIngrese el ID de la factura a eliminar: ").strip()
            confirmacion = input(
                "¿Está seguro de eliminar esta factura? (s/n): "
            ).lower()

            if confirmacion == "s":
                eliminado = self.factura_crud.eliminar_factura(factura_id)
                if eliminado:
                    print("ÉXITO: Factura eliminada exitosamente.")
                else:
                    print("ERROR: No se pudo eliminar la factura.")
            else:
                print("INFO: Operación cancelada.")

        except Exception as e:
            print(f"ERROR: {e}")

        """Eliminar un producto"""
        try:
            producto_id = input("\nIngrese el ID del producto a eliminar: ").strip()
            confirmacion = input(
                "¿Está seguro de eliminar este producto? (s/n): "
            ).lower()

            if confirmacion == "s":
                eliminado = self.producto_crud.eliminar_producto(producto_id)
                if eliminado:
                    print("ÉXITO: Producto eliminado exitosamente.")
                else:
                    print("ERROR: No se pudo eliminar el producto.")
            else:
                print("INFO: Operación cancelada.")

        except Exception as e:
            print(f"ERROR: {e}")

    def mostrar_menu_platos(self) -> None:
        while True:
            print("\n" + "-" * 30)
            print("   GESTIÓN DE PLATOS")
            print("-" * 30)
            print("1. Crear Plato")
            print("2. Listar Platos")
            print("3. Buscar Plato por ID")
            print("4. Actualizar Plato")
            print("5. Eliminar Plato")
            print("0. Volver al menú principal")

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                self.crear_plato()
            elif opcion == "2":
                self.listar_platos()
            elif opcion == "3":
                self.buscar_plato_por_id()
            elif opcion == "4":
                self.actualizar_plato()
            elif opcion == "5":
                self.eliminar_plato()
            elif opcion == "0":
                break
            else:
                print("ERROR: Opción inválida. Intente nuevamente.")

    def crear_plato(self) -> None:
        try:
            print("\n--- CREAR PLATO ---")

            """Mostrar categorías (FK)"""
            categorias = self.categoria_crud.obtener_categorias()
            if not categorias:
                print(
                    "ERROR: No hay categorías registradas. Cree una categoría primero."
                )
                return
            print("\n--- CATEGORÍAS DISPONIBLES ---")
            for i, cat in enumerate(categorias, 1):
                print(f"{i}. ID: {cat.id} | {cat.nombre} - {cat.descripcion}")
            id_categoria_input = input("Ingrese el ID de la categoría: ").strip()
            id_categoria = UUID(id_categoria_input)

            """Mostrar usuarios (FK)"""
            usuarios = self.usuario_crud.obtener_usuarios()
            if not usuarios:
                print("ERROR: No hay usuarios registrados.")
                return
            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return
            id_usuario = self.usuario_actual.id

            nombre = input("Nombre: ").strip()
            precio_unidad = int(input("Precio unidad (entero): ").strip())
            descripcion = input("Descripción (opcional): ").strip() or None

            plato = self.plato_crud.crear_plato(
                nombre=nombre,
                precio_unidad=precio_unidad,
                descripcion=descripcion,
                id_categoria=id_categoria,
                id_usuario=id_usuario,
            )
            print(f"ÉXITO: Plato creado -> ID: {plato.id}, Nombre: {plato.nombre}")

        except Exception as e:
            print(f"ERROR: {e}")

    def listar_platos(self) -> None:
        try:
            platos = self.plato_crud.obtener_platos()
            if not platos:
                print("INFO: No hay platos registrados.")
                return
            print(f"\n--- PLATOS ({len(platos)}) ---")
            for i, p in enumerate(platos, 1):
                print(
                    f"{i}. ID: {p.id} | {p.nombre} | Precio: {p.precio_unidad} | Categoria: {p.id_categoria} | Descripción: {p.descripcion}"
                )
        except Exception as e:
            print(f"ERROR: {e}")

    def buscar_plato_por_id(self) -> None:
        try:
            plato_id = input("\nIngrese el ID del plato: ").strip()
            plato = self.plato_crud.obtener_plato(UUID(plato_id))
            if plato:
                print(f"ÉXITO: Plato encontrado:")
                print(f"   ID: {plato.id}")
                print(f"   Nombre: {plato.nombre}")
                print(f"   Precio unidad: {plato.precio_unidad}")
                print(f"   Descripción: {plato.descripcion}")
                print(f"   Categoria ID: {plato.id_categoria}")
            else:
                print("ERROR: Plato no encontrado.")
        except Exception as e:
            print(f"ERROR: {e}")

    def actualizar_plato(self) -> None:
        try:
            plato_id = input("\nIngrese el ID del plato a actualizar: ").strip()
            plato = self.plato_crud.obtener_plato(UUID(plato_id))
            if not plato:
                print("ERROR: Plato no encontrado.")
                return

            print(f"\nActualizando plato: {plato.nombre}")
            print("Deje en blanco para mantener el valor actual")

            """Mostrar categorías (FK) antes de permitir cambio"""
            categorias = self.categoria_crud.obtener_categorias()
            if categorias:
                print("\n--- CATEGORÍAS DISPONIBLES ---")
                for i, cat in enumerate(categorias, 1):
                    print(f"{i}. ID: {cat.id} | {cat.nombre}")

            nuevo_nombre = input(f"Nombre actual ({plato.nombre}): ").strip()
            nuevo_precio = input(f"Precio actual ({plato.precio_unidad}): ").strip()
            nueva_descripcion = input(
                f"Descripción actual ({plato.descripcion}): "
            ).strip()
            nuevo_id_categoria = input(
                f"Categoria ID actual ({plato.id_categoria}): "
            ).strip()

            cambios = {}
            if nuevo_nombre:
                cambios["nombre"] = nuevo_nombre
            if nuevo_precio:
                cambios["precio_unidad"] = int(nuevo_precio)
            if nueva_descripcion:
                cambios["descripcion"] = nueva_descripcion
            if nuevo_id_categoria:
                cambios["id_categoria"] = UUID(nuevo_id_categoria)
            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return
            id_usuario_mod = self.usuario_actual.id

            """id_actualizador (si hay usuario autenticado)"""
            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return
            cambios["id_actualizador"] = self.usuario_actual.id

            if cambios:
                plato_actualizado = self.plato_crud.actualizar_plato(
                    plato.id, id_usuario_mod,**cambios
                )
                print(
                    f"ÉXITO: Plato actualizado -> ID: {plato_actualizado.id}, Nombre: {plato_actualizado.nombre}"
                )
            else:
                print("INFO: No se realizaron cambios.")

        except Exception as e:
            print(f"ERROR: {e}")

    def eliminar_plato(self) -> None:
        try:
            plato_id = input("\nIngrese el ID del plato a eliminar: ").strip()
            confirm = input("¿Seguro que deseas eliminarlo? (s/n): ").strip().lower()
            if confirm == "s":
                eliminado = self.plato_crud.eliminar_plato(UUID(plato_id))
                if eliminado:
                    print("ÉXITO: Plato eliminado.")
                else:
                    print("ERROR: Plato no encontrado.")
            else:
                print("INFO: Operación cancelada.")
        except Exception as e:
            print(f"ERROR: {e}")

    def mostrar_menu_plato_orden(self) -> None:
        while True:
            print("\n" + "-" * 30)
            print("   GESTIÓN DE PLATOS EN ÓRDEN")
            print("-" * 30)
            print("1. Crear Plato_Orden")
            print("2. Listar Platos_Orden")
            print("3. Buscar Plato_Orden (orden, plato)")
            print("4. Actualizar Plato_Orden")
            print("5. Eliminar Plato_Orden")
            print("0. Volver al menú principal")

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                self.crear_plato_orden()
            elif opcion == "2":
                self.listar_platos_orden()
            elif opcion == "3":
                self.buscar_plato_orden()
            elif opcion == "4":
                self.actualizar_plato_orden()
            elif opcion == "5":
                self.eliminar_plato_orden()
            elif opcion == "0":
                break
            else:
                print("ERROR: Opción inválida. Intente nuevamente.")

    def crear_plato_orden(self) -> None:
        try:
            print("\n--- CREAR PLATO_EN_ORDEN ---")

            """Mostrar órdenes (FK)"""
            ordenes = self.orden_crud.obtener_ordenes()
            if not ordenes:
                print("ERROR: No hay órdenes registradas.")
                return
            print("\n--- ÓRDENES DISPONIBLES ---")
            for i, o in enumerate(ordenes, 1):
                print(f"{i}. ID: {o.id} | Mesa: {o.id_mesa} | Estado: {o.estado}")
            id_orden = UUID(input("Ingrese el ID de la orden: ").strip())

            """Mostrar platos (FK)"""
            platos = self.plato_crud.obtener_platos()
            if not platos:
                print("ERROR: No hay platos registrados.")
                return
            print("\n--- PLATOS DISPONIBLES ---")
            for i, p in enumerate(platos, 1):
                print(f"{i}. ID: {p.id} | {p.nombre} | Precio: {p.precio_unidad}")
            id_plato = UUID(input("Ingrese el ID del plato: ").strip())

            """usuario (FK)"""
            usuarios = self.usuario_crud.obtener_usuarios()
            if not usuarios:
                print("ERROR: No hay usuarios registrados.")
                return
            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return
            id_usuario = self.usuario_actual.id

            cantidad = int(input("Cantidad: ").strip())

            plato_orden = self.plato_orden_crud.crear_plato_orden(
                id_orden=id_orden,
                id_plato=id_plato,
                cantidad=cantidad,
                id_usuario=id_usuario,
            )
            print(
                f"ÉXITO: Plato_Orden creado -> Orden: {plato_orden.id_orden}, Plato: {plato_orden.id_plato}, Cantidad: {plato_orden.cantidad}"
            )

        except Exception as e:
            print(f"ERROR: {e}")

    def listar_platos_orden(self) -> None:
        try:
            items = self.plato_orden_crud.obtener_platos_orden()
            if not items:
                print("INFO: No hay platos en órdenes registrados.")
                return
            print(f"\n--- PLATOS EN ÓRDEN ({len(items)}) ---")
            for i, it in enumerate(items, 1):
                print(
                    f"{i}. Orden ID: {it.id_orden} | Plato ID: {it.id_plato} | Cantidad: {it.cantidad}"
                )
        except Exception as e:
            print(f"ERROR: {e}")

    def buscar_plato_orden(self) -> None:
        try:
            id_orden = UUID(input("Ingrese el ID de la orden: ").strip())
            id_plato = UUID(input("Ingrese el ID del plato: ").strip())
            item = self.plato_orden_crud.obtener_plato_orden(id_orden, id_plato)
            if item:
                print(
                    f"Plato_Orden encontrado -> Orden: {item.id_orden}, Plato: {item.id_plato}, Cantidad: {item.cantidad}"
                )
            else:
                print("ERROR: Plato_Orden no encontrado.")
        except Exception as e:
            print(f"ERROR: {e}")

    def actualizar_plato_orden(self) -> None:
        try:
            id_orden = UUID(input("Ingrese el ID de la orden: ").strip())
            id_plato = UUID(input("Ingrese el ID del plato: ").strip())
            item = self.plato_orden_crud.obtener_plato_orden(id_orden, id_plato)
            if not item:
                print("ERROR: Plato_Orden no encontrado.")
                return

            print(
                f"\nActualizando Plato_Orden -> Orden: {item.id_orden}, Plato: {item.id_plato}"
            )
            nuevo_cantidad = input(f"Cantidad actual ({item.cantidad}): ").strip()

            cambios = {}
            if nuevo_cantidad:
                cambios["cantidad"] = int(nuevo_cantidad)

            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return
            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return
            id_usuario_mod = self.usuario_actual.id

            if cambios:
                actualizado = self.plato_orden_crud.actualizar_plato_orden(
                    id_orden, id_plato, id_usuario_mod,**cambios
                )
                print(
                    f"ÉXITO: Plato_Orden actualizado -> Cantidad: {actualizado.cantidad}"
                )
            else:
                print("INFO: No se realizaron cambios.")
        except Exception as e:
            print(f"ERROR: {e}")

    def eliminar_plato_orden(self) -> None:
        try:
            id_orden = UUID(input("Ingrese el ID de la orden: ").strip())
            id_plato = UUID(input("Ingrese el ID del plato: ").strip())
            confirm = (
                input("¿Seguro que deseas eliminar este registro? (s/n): ")
                .strip()
                .lower()
            )
            if confirm == "s":
                eliminado = self.plato_orden_crud.eliminar_plato_orden(
                    id_orden, id_plato
                )
                if eliminado:
                    print("ÉXITO: Plato_Orden eliminado.")
                else:
                    print("ERROR: Plato_Orden no encontrado.")
            else:
                print("INFO: Operación cancelada.")
        except Exception as e:
            print(f"ERROR: {e}")

    def mostrar_menu_reservas(self) -> None:
        while True:
            print("\n" + "-" * 30)
            print("   GESTIÓN DE RESERVAS")
            print("-" * 30)
            print("1. Crear Reserva")
            print("2. Listar Reservas")
            print("3. Buscar Reserva (cliente, mesa)")
            print("4. Actualizar Reserva")
            print("5. Eliminar Reserva")
            print("0. Volver al menú principal")

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                self.crear_reserva()
            elif opcion == "2":
                self.listar_reservas()
            elif opcion == "3":
                self.buscar_reserva()
            elif opcion == "4":
                self.actualizar_reserva()
            elif opcion == "5":
                self.eliminar_reserva()
            elif opcion == "0":
                break
            else:
                print("ERROR: Opción inválida. Intente nuevamente.")

    def _parse_fecha_hora(self, texto: str) -> datetime:
        """Acepta ISO o 'YYYY-MM-DD HH:MM'"""
        try:
            return datetime.fromisoformat(texto)
        except Exception:
            try:
                return datetime.strptime(texto, "%Y-%m-%d %H:%M")
            except Exception:
                raise ValueError(
                    "Formato de fecha/hora inválido. Use 'YYYY-MM-DD HH:MM'"
                )

    def crear_reserva(self) -> None:
        try:
            print("\n--- CREAR RESERVA ---")

            clientes = self.cliente_crud.obtener_clientes()
            if not clientes:
                print("ERROR: No hay clientes registrados.")
                return
            print("\n--- CLIENTES DISPONIBLES ---")
            for i, c in enumerate(clientes, 1):
                print(f"{i}. ID: {c.id} | {c.nombre} {c.apellido}")
            id_cliente = UUID(input("Ingrese el ID del cliente: ").strip())

            mesas = self.mesa_crud.obtener_mesas()
            if not mesas:
                print("ERROR: No hay mesas registradas.")
                return
            print("\n--- MESAS DISPONIBLES ---")
            for i, m in enumerate(mesas, 1):
                print(f"{i}. ID: {m.id} | Capacidad: {m.capacidad}")
            id_mesa = UUID(input("Ingrese el ID de la mesa: ").strip())

            cantidad_personas = int(input("Cantidad de personas: ").strip())
            fecha_text = input("Fecha y hora (YYYY-MM-DD HH:MM): ").strip()
            fecha_hora = self._parse_fecha_hora(fecha_text)

            estado_input = (
                input("Estado (True para confirmada, False para pendiente): ")
                .strip()
                .lower()
            )
            Estado = estado_input in ("1", "true", "t", "si", "s", "yes")

            usuarios = self.usuario_crud.obtener_usuarios()
            if not usuarios:
                print("ERROR: No hay usuarios registrados.")
                return
            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return
            id_usuario = self.usuario_actual.id

            reserva = self.reserva_crud.crear_reserva(
                id_cliente=id_cliente,
                id_mesa=id_mesa,
                cantidad_personas=cantidad_personas,
                fecha_Hora=fecha_hora,
                Estado=Estado,
                id_usuario=id_usuario,
            )
            print(
                f"ÉXITO: Reserva creada -> Cliente: {reserva.id_cliente}, Mesa: {reserva.id_mesa}, Fecha: {reserva.fecha_Hora}"
            )

        except Exception as e:
            print(f"ERROR: {e}")

    def listar_reservas(self) -> None:
        try:
            reservas = self.reserva_crud.obtener_reservas()
            if not reservas:
                print("INFO: No hay reservas registradas.")
                return
            print(f"\n--- RESERVAS ({len(reservas)}) ---")
            for i, r in enumerate(reservas, 1):
                print(
                    f"{i}. Cliente: {r.id_cliente} | Mesa: {r.id_mesa} | Personas: {r.cantidad_personas} | Fecha: {r.fecha_Hora} | Estado: {r.Estado}"
                )
        except Exception as e:
            print(f"ERROR: {e}")

    def buscar_reserva(self) -> None:
        try:
            id_cliente = UUID(input("Ingrese el ID del cliente: ").strip())
            id_mesa = UUID(input("Ingrese el ID de la mesa: ").strip())
            reserva = self.reserva_crud.obtener_reserva(id_cliente, id_mesa)
            if reserva:
                print(
                    f"Reserva encontrada -> Cliente: {reserva.id_cliente}, Mesa: {reserva.id_mesa}, Fecha: {reserva.fecha_Hora}, Personas: {reserva.cantidad_personas}"
                )
            else:
                print("ERROR: Reserva no encontrada.")
        except Exception as e:
            print(f"ERROR: {e}")

    def actualizar_reserva(self) -> None:
        try:
            id_cliente = UUID(
                input("Ingrese el ID del cliente de la reserva: ").strip()
            )
            id_mesa = UUID(input("Ingrese el ID de la mesa de la reserva: ").strip())
            reserva = self.reserva_crud.obtener_reserva(id_cliente, id_mesa)
            if not reserva:
                print("ERROR: Reserva no encontrada.")
                return

            print(
                f"\nActualizando reserva Cliente: {reserva.id_cliente} | Mesa: {reserva.id_mesa}"
            )
            print("Deje en blanco para mantener el valor actual")

            nuevo_cant = input(
                f"Cantidad de personas actual ({reserva.cantidad_personas}): "
            ).strip()
            nueva_fecha = input(
                f"Fecha/hora actual ({reserva.fecha_Hora}) [YYYY-MM-DD HH:MM]: "
            ).strip()
            nuevo_estado = input(
                f"Estado actual ({reserva.Estado}) [True/False]: "
            ).strip()

            cambios = {}
            if nuevo_cant:
                cambios["cantidad_personas"] = int(nuevo_cant)
            if nueva_fecha:
                cambios["fecha_Hora"] = self._parse_fecha_hora(nueva_fecha)
            if nuevo_estado:
                cambios["Estado"] = nuevo_estado.lower() in (
                    "1",
                    "true",
                    "t",
                    "si",
                    "s",
                    "yes",
                )

            if not self.usuario_actual:
                print("ERROR: No hay usuario autenticado.")
                return
            id_usuario_mod = self.usuario_actual.id

            if cambios:
                reserva_actualizada = self.reserva_crud.actualizar_reserva(
                    id_cliente, id_mesa, id_usuario_mod,**cambios
                )
                print(
                    f"ÉXITO: Reserva actualizada -> Cliente: {reserva_actualizada.id_cliente}, Mesa: {reserva_actualizada.id_mesa}"
                )
            else:
                print("INFO: No se realizaron cambios.")
        except Exception as e:
            print(f"ERROR: {e}")

    def eliminar_reserva(self) -> None:
        try:
            id_cliente = UUID(
                input("Ingrese el ID del cliente de la reserva: ").strip()
            )
            id_mesa = UUID(input("Ingrese el ID de la mesa de la reserva: ").strip())
            confirm = (
                input("¿Seguro que deseas eliminar la reserva? (s/n): ").strip().lower()
            )
            if confirm == "s":
                eliminado = self.reserva_crud.eliminar_reserva(id_cliente, id_mesa)
                if eliminado:
                    print("ÉXITO: Reserva eliminada.")
                else:
                    print("ERROR: Reserva no encontrada.")
            else:
                print("INFO: Operación cancelada.")
        except Exception as e:
            print(f"ERROR: {e}")

    def ejecutar(self) -> None:
        """Ejecutar el sistema principal con autenticacion"""
        try:
            print("Iniciando Sistema de Gestion de Productos...")
            print("Configurando base de datos...")
            create_tables()
            print("Sistema listo para usar.")

            """Autenticacion requerida"""
            if not self.pantalla_login():
                print("Acceso denegado. Hasta luego!")
                return

            """Menu principal autenticado"""
            while True:
                self.menu_principal_autentificado()
                opcion = input("\nSeleccione una opcion: ").strip()
                if opcion == "1":
                    self.mostrar_menu_usuarios()
                elif opcion == "2":
                    self.mostrar_menu_categorias()
                elif opcion == "3":
                    self.mostrar_menu_clientes()
                elif opcion =="4":
                    self.mostrar_menu_empleados()
                elif opcion=="5":
                    self.mostrar_menu_facturas()
                elif opcion =="6":
                    self.mostrar_menu_mesas()
                elif opcion =="7":
                    self.mostrar_menu_ordenes()
                elif opcion == "8":
                    self.mostrar_menu_platos()
                elif opcion == "9":
                    self.mostrar_menu_reservas()
                elif opcion =="10":
                    self.mostrar_menu_perfil()
                elif opcion == "0":
                    print("Cerrando sesion. Hasta luego!")
                    break

        except:
            raise ValueError("error")


def main():
    """Funcion principal"""
    with SistemaPrincipal() as sistema:
        sistema.ejecutar()


if __name__ == "__main__":
    main()
