from sqlalchemy.orm import Session
from entities.Cliente import Cliente
from typing import Optional, List
from uuid import UUID
import re

class ClienteCRUD:
    """
    Operaciones CRUD para la entidad Cliente.
    """

    def __init__(self, db: Session):
        """Inicializa con una sesión de base de datos."""
        self.db = db

    def _validar_nombre(self, nombre: str) -> bool:
        """Valida el nombre del cliente (3-20 caracteres alfabéticos)."""
        pattern = r"^[a-zA-Z]{3,20}$"
        return re.match(pattern, nombre) is not None

    def _validar_apellido(self, apellido: str) -> bool:
        """Valida el apellido del cliente (3-20 caracteres alfabéticos)."""
        pattern = r"^[a-zA-Z]{3,20}$"
        return re.match(pattern, apellido) is not None

    def _validar_email(self, email: str) -> bool:
        """Valida el correo electrónico del cliente."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,40}$"
        return re.match(pattern, email) is not None

    def _validar_telefono(self, telefono: str) -> bool:
        """Valida el número de teléfono del cliente (7-15 dígitos)."""
        pattern = r"^[0-9]{7,15}$"
        return re.match(pattern, telefono) is not None

    def crear_cliente(
        self, nombre: str, apellido: str, Email: str, telefono: str, id_usuario: UUID
    ) -> Cliente:
        """Crea un nuevo cliente después de validar sus campos."""
        if not self._validar_nombre(nombre):
            raise ValueError("Nombre inválido")
        if not self._validar_apellido(apellido):
            raise ValueError("Apellido inválido")
        if not self._validar_email(Email):
            raise ValueError("Email inválido")
        if not self._validar_telefono(telefono):
            raise ValueError("Teléfono inválido")
        cliente = Cliente(
            nombre=nombre.strip(),
            apellido=apellido.strip(),
            Email=Email.strip(),
            telefono=telefono.strip(),
            id_usuario=id_usuario,
        )
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def obtener_cliente(self, cliente_id: UUID) -> Optional[Cliente]:
        """Obtiene un cliente por su UUID."""
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def obtener_clientes(self, skip: int = 0) -> List[Cliente]:
        """Obtiene una lista de clientes, con salto opcional para paginación."""
        return self.db.query(Cliente).offset(skip).all()

    def actualizar_cliente(self, cliente_id: UUID, id_usuario_mod: UUID, **kwargs) -> Optional[Cliente]:
        """Actualiza los campos de un cliente, actualizando id_usuario_mod y fecha_actualizacion solo si hay cambios."""
        from datetime import datetime

        cliente = self.obtener_cliente(cliente_id)
        if not cliente:
            return None
        cambios = False
        if "nombre" in kwargs and not self._validar_nombre(kwargs["nombre"]):
            raise ValueError("Nombre inválido")
        if "apellido" in kwargs and not self._validar_apellido(kwargs["apellido"]):
            raise ValueError("Apellido inválido")
        if "Email" in kwargs and not self._validar_email(kwargs["Email"]):
            raise ValueError("Email inválido")
        if "telefono" in kwargs and not self._validar_telefono(kwargs["telefono"]):
            raise ValueError("Teléfono inválido")
        for key, value in kwargs.items():
            if hasattr(cliente, key):
                if getattr(cliente, key) != value:
                    setattr(cliente, key, value)
                    cambios = True
        if cambios:
            if id_usuario_mod:
                cliente.id_usuario_mod = id_usuario_mod
            if hasattr(cliente, "fecha_actualizacion"):
                cliente.fecha_actualizacion = datetime.now()
            self.db.commit()
            self.db.refresh(cliente)
        return cliente

    def eliminar_cliente(self, cliente_id: UUID) -> bool:
        """Elimina un cliente por su UUID."""
        cliente = self.obtener_cliente(cliente_id)
        if not cliente:
            return False
        self.db.delete(cliente)
        self.db.commit()
        return True
