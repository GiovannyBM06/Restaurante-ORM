from sqlalchemy.orm import Session
from entities.Cliente import Cliente
from typing import Optional, List
from uuid import UUID
import re
from datetime import datetime


class ClienteCRUD:
    def __init__(self, db: Session):
        self.db = db

    def _validar_nombre(self, nombre: str) -> bool:
        return bool(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", nombre))

    def _validar_apellido(self, apellido: str) -> bool:
        return bool(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", apellido))

    def _validar_email(self, email: str) -> bool:
        return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))

    def _validar_telefono(self, telefono: str) -> bool:
        return bool(re.match(r"^\+?\d{7,15}$", telefono))

    def crear_cliente(
        self, nombre: str, apellido: str, Email: str, telefono: str, id_usuario: UUID
    ) -> Cliente:
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
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def obtener_clientes(self, skip: int = 0) -> List[Cliente]:
        return self.db.query(Cliente).offset(skip).all()

    def actualizar_cliente(
        self, cliente_id: UUID, id_usuario_mod: UUID, **kwargs
    ) -> Optional[Cliente]:
        cliente = self.obtener_cliente(cliente_id)
        if not cliente:
            return None
        cambios = False
        if "Email" in kwargs and not self._validar_email(kwargs["Email"]):
            raise ValueError("Email inválido")
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
        cliente = self.obtener_cliente(cliente_id)
        if not cliente:
            return False
        self.db.delete(cliente)
        self.db.commit()
        return True
