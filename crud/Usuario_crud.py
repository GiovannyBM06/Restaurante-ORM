from sqlalchemy.orm import Session
from entities.Usuario import Usuario
from typing import Optional, List
from uuid import UUID
import re


class UsuarioCRUD:
    """
    Operaciones CRUD para la entidad Usuario.
    """

    def eliminar_usuario(self, usuario_id: UUID) -> bool:
        """Elimina un usuario por su UUID."""
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return False
        self.db.delete(usuario)
        self.db.commit()
        return True

    def __init__(self, db: Session):
        """Inicializa con una sesión de base de datos."""
        self.db = db

    def _validar_nombre(self, nombre: str) -> bool:
        """Valida el nombre del usuario (1-20 caracteres alfabéticos)."""
        pattern = r"^[a-zA-Z]{1,20}$"
        return re.match(pattern, nombre) is not None

    def _validar_apellido(self, apellido: str) -> bool:
        """Valida el apellido del usuario (1-20 caracteres alfabéticos)."""
        pattern = r"^[a-zA-Z]{1,20}$"
        return re.match(pattern, apellido) is not None

    def _validar_email(self, email: str) -> bool:
        """Valida el correo electrónico del usuario."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,40}$"
        return re.match(pattern, email) is not None

    def _validar_contraseña(self, contraseña: str) -> bool:
        """Valida la contraseña del usuario (6-20 caracteres, permite números)."""
        pattern = r"^[a-zA-Z0-9._*-]{6,20}$"
        return re.match(pattern, contraseña) is not None

    def crear_usuario(
        self,
        nombre: str,
        apellido: str,
        email: str,
        contraseña: str,
    ) -> Usuario:
        """Crea un nuevo usuario después de validar sus campos."""
        if not self._validar_nombre(nombre):
            raise ValueError("Nombre inválido")
        if not self._validar_apellido(apellido):
            raise ValueError("Apellido inválido")
        if not self._validar_email(email):
            raise ValueError("Email inválido")
        if not self._validar_contraseña(contraseña):
            raise ValueError("Contraseña inválida")
        if self.obtener_usuario_con_email(email):
            raise ValueError("El email ya está registrado")
        usuario = Usuario(
            nombre=nombre.strip(),
            apellido=apellido.strip(),
            email=email.lower().strip(),
            contraseña=contraseña,
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def obtener_usuario(self, usuario_id: UUID) -> Optional[Usuario]:
        """Obtiene un usuario por su UUID."""
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def obtener_usuario_con_email(self, email: str) -> Optional[Usuario]:
        """Obtiene un usuario por su correo electrónico."""
        return (
            self.db.query(Usuario)
            .filter(Usuario.email == email.lower().strip())
            .first()
        )

    def obtener_usuarios_con_nombre(self, nombre: str) -> List[Usuario]:
        """Obtiene todos los usuarios con un nombre dado (no sensible a mayúsculas/minúsculas)."""
        return self.db.query(Usuario).filter(Usuario.nombre.ilike(nombre.strip())).all()

    def autenticar_usuario(self, email: str, contraseña: str) -> Optional[Usuario]:
        """Autentica un usuario por correo electrónico y contraseña."""
        usuario = self.obtener_usuario_con_email(email)
        if not usuario:
            return None

        if usuario.contraseña == contraseña:
            return usuario
        return None

    def cambiar_contraseña(
        self, usuario_id: UUID, contraseña_actual: str, contraseña_nueva: str
    ) -> bool:
        """
        Cambia la contraseña de un usuario si la contraseña actual es correcta.
        """
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")

        if usuario.contraseña != contraseña_actual:
            raise ValueError("La contraseña actual es incorrecta")

        if not self._validar_contraseña(contraseña_nueva):
            raise ValueError(
                "La nueva contraseña no cumple con los requisitos de formato"
            )

        usuario.contraseña = contraseña_nueva
        self.db.commit()
        return True

    def obtener_usuarios(self, skip: int = 0) -> List[Usuario]:
        """Obtiene una lista de usuarios, con salto opcional para paginación."""
        return self.db.query(Usuario).offset(skip).all()

    def actualizar_usuario(self, usuario_id: UUID, **kwargs) -> Optional[Usuario]:
        """Actualiza los campos de un usuario después de validar."""
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return None

        if "email" in kwargs:
            email = kwargs["email"]
            if not self._validar_email(email):
                raise ValueError("Email inválido")
            if (
                self.obtener_usuario_con_email(email)
                and self.obtener_usuario_con_email(email).id != usuario_id
            ):
                raise ValueError("El Email ya se encuantra registrado")
            kwargs["email"] = email.lower().strip()

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not self._validar_nombre(nombre):
                raise ValueError("Nombre inválido")

        if "apellido" in kwargs:
            apellido = kwargs["apellido"]
            if not self._validar_apellido(apellido):
                raise ValueError("apellido inválido")

        if "contraseña" in kwargs:
            contraseña = kwargs["contraseña"]
            if not self._validar_contraseña(contraseña):
                raise ValueError("Contraseña inválida")

        for key, value in kwargs.items():
            if hasattr(usuario, key):
                setattr(usuario, key, value)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario
