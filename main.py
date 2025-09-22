from typing import Optional
"""
from entities.Categoria import Categoria
from entities.Cliente import Cliente
from entities.Empleado import Empleado
from entities.Factura import Factura
from entities.Mesa import Mesa
from entities.Orden import Orden
from entities.Plato import Plato
from entities.Plato_Orden import Plato_Orden
from entities.Reserva import Reserva
"""
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

class SistemaPrincipal():
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
        self.usuario_actual: Optional[Usuario]= None

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.db.close()
    
    def pantalla_login(self)-> bool:
        print("\n" + "=" * 50)
        print("        SISTEMA DE GESTION DE PRODUCTOS")
        print("=" * 50)
        print("INICIAR SESION")
        print("=" * 50)

        intentos = 0
        max_intentos = 3

        while intentos<max_intentos:
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
                else:
                    print("ERROR: Credenciales incorrectas")
                    intentos += 1
            except Exception as e:
                    print(f"ERROR: Error durante el login: {e}")
                    intentos += 1

    def menu_principal_autentificado(self)-> None:
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
        print("10. Configuracion del Sistema")
        print("11. Mi Perfil")
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
                cambios["apellido"]= nuevo_apellido
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
            print("7. Crear Usuario Administrador")
            print("0. Volver al menu principal")

            opcion = input("\nSeleccione una opcion: ").strip()

            if opcion == "1":
                self.crear_usuario()
            elif opcion == "2":
                self.listar_usuarios()
            elif opcion == "3":
                self.buscar_usuario_por_email()
            elif opcion == "4":
                self.buscar_usuario_por_nombre_usuario()
            elif opcion == "5":
                self.actualizar_usuario()
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
            contrasena = input("Contraseña: ").strip

            usuario = self.usuario_crud.crear_usuario(
                nombre=nombre,
                apellido=apellido,
                email =email,
                contrasena=contrasena,

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
                print(
                    f"{i}. {usuario.nombre} ({usuario.apellido}) - {usuario.email}"
                )

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
                f"Apellid actual ({usuario.apellido}): "
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
               
    def ejecutar(self) -> None:
        """Ejecutar el sistema principal con autenticacion"""
        try:
            print("Iniciando Sistema de Gestion de Productos...")
            print("Configurando base de datos...")
            create_tables()
            print("Sistema listo para usar.")

            # Autenticacion requerida
            if not self.pantalla_login():
                print("Acceso denegado. Hasta luego!")
                return

            # Menu principal autenticado
            while True:
                self.menu_principal_autentificado()
                opcion = input("\nSeleccione una opcion: ").strip()
                """Aquí se ejcutaran las diferentes acciones para la BD"""
        except:
            raise ValueError("error")