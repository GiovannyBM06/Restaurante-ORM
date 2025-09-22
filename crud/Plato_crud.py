from sqlalchemy.orm import Session
from entities.Plato import Plato
from typing import Optional, List
from uuid import UUID
import re

class PlatoCRUD:
	def __init__(self, db: Session):
		self.db = db

	def _validar_nombre(self, nombre: str) -> bool:
		pattern = r"^[a-zA-Z]{1,20}$"
		return re.match(pattern, nombre) is not None

	def _validar_precio(self, precio: int) -> bool:
		return isinstance(precio, int) and precio > 0

	def _validar_descripcion(self, descripcion: str) -> bool:
		return descripcion is None or (0 < len(descripcion.strip()) <= 100)

	def crear_plato(self, nombre: str, precio_unidad: int, descripcion: str, id_categoria: UUID, id_usuario: UUID) -> Plato:
		if not self._validar_nombre(nombre):
			raise ValueError("Nombre inválido")
		if not self._validar_precio(precio_unidad):
			raise ValueError("Precio inválido")
		if not self._validar_descripcion(descripcion):
			raise ValueError("Descripción inválida")
		plato = Plato(nombre=nombre.strip(), precio_unidad=precio_unidad, descripcion=descripcion, id_categoria=id_categoria, id_usuario=id_usuario)
		self.db.add(plato)
		self.db.commit()
		self.db.refresh(plato)
		return plato

	def obtener_plato(self, plato_id: UUID) -> Optional[Plato]:
		return self.db.query(Plato).filter(Plato.id == plato_id).first()

	def obtener_platos(self, skip: int = 0) -> List[Plato]:
		return self.db.query(Plato).offset(skip).all()

	def actualizar_plato(self, plato_id: UUID, **kwargs) -> Optional[Plato]:
		plato = self.obtener_plato(plato_id)
		if not plato:
			return None
		if "nombre" in kwargs and not self._validar_nombre(kwargs["nombre"]):
			raise ValueError("Nombre inválido")
		if "precio_unidad" in kwargs and not self._validar_precio(kwargs["precio_unidad"]):
			raise ValueError("Precio inválido")
		if "descripcion" in kwargs and not self._validar_descripcion(kwargs["descripcion"]):
			raise ValueError("Descripción inválida")
		for key, value in kwargs.items():
			if hasattr(plato, key):
				setattr(plato, key, value)
		self.db.commit()
		self.db.refresh(plato)
		return plato
"""
	def eliminar_plato(self, plato_id: UUID) -> bool:
		plato = self.obtener_plato(plato_id)
		if not plato:
			return False
		self.db.delete(plato)
		self.db.commit()
		return True
"""