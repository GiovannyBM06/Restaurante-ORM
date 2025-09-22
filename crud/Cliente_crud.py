from sqlalchemy.orm import Session
from entities.Cliente import Cliente
from typing import Optional, List
from uuid import UUID
import re

class ClienteCRUD:
	def __init__(self, db: Session):
		self.db = db

	def _validar_nombre(self, nombre: str) -> bool:
		pattern = r"^[a-zA-Z]{3,20}$"
		return re.match(pattern, nombre) is not None

	def _validar_apellido(self, apellido: str) -> bool:
		pattern = r"^[a-zA-Z]{3,20}$"
		return re.match(pattern, apellido) is not None

	def _validar_email(self, email: str) -> bool:
		pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,40}$"
		return re.match(pattern, email) is not None

	def _validar_telefono(self, telefono: str) -> bool:
		pattern = r"^[0-9]{7,15}$"
		return re.match(pattern, telefono) is not None

	def crear_cliente(self, nombre: str, apellido: str, Email: str, telefono: str, id_usuario: UUID) -> Cliente:
		if not self._validar_nombre(nombre):
			raise ValueError("Nombre inválido")
		if not self._validar_apellido(apellido):
			raise ValueError("Apellido inválido")
		if not self._validar_email(Email):
			raise ValueError("Email inválido")
		if not self._validar_telefono(telefono):
			raise ValueError("Teléfono inválido")
		cliente = Cliente(nombre=nombre.strip(), apellido=apellido.strip(), Email=Email.strip(), telefono=telefono.strip(), id_usuario=id_usuario)
		self.db.add(cliente)
		self.db.commit()
		self.db.refresh(cliente)
		return cliente

	def obtener_cliente(self, cliente_id: UUID) -> Optional[Cliente]:
		return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

	def obtener_clientes(self, skip: int = 0) -> List[Cliente]:
		return self.db.query(Cliente).offset(skip).all()

	def actualizar_cliente(self, cliente_id: UUID, **kwargs) -> Optional[Cliente]:
		cliente = self.obtener_cliente(cliente_id)
		if not cliente:
			return None
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
				setattr(cliente, key, value)
		self.db.commit()
		self.db.refresh(cliente)
		return cliente
"""
	def eliminar_cliente(self, cliente_id: UUID) -> bool:
		cliente = self.obtener_cliente(cliente_id)
		if not cliente:
			return False
		self.db.delete(cliente)
		self.db.commit()
		return True
"""