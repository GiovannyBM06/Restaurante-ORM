from sqlalchemy.orm import Session
from entities.Mesa import Mesa
from typing import Optional, List
from uuid import UUID
import re

class MesaCRUD:
	def __init__(self, db: Session):
		self.db = db

	def _validar_capacidad(self, capacidad: int) -> bool:
		return isinstance(capacidad, int) and capacidad > 0

	def crear_mesa(self, capacidad: int, id_usuario: UUID) -> Mesa:
		if not self._validar_capacidad(capacidad):
			raise ValueError("Capacidad inválida")
		mesa = Mesa(capacidad=capacidad, id_usuario=id_usuario)
		self.db.add(mesa)
		self.db.commit()
		self.db.refresh(mesa)
		return mesa

	def obtener_mesa(self, mesa_id: UUID) -> Optional[Mesa]:
		return self.db.query(Mesa).filter(Mesa.id == mesa_id).first()

	def obtener_mesas(self, skip: int = 0) -> List[Mesa]:
		return self.db.query(Mesa).offset(skip).all()

	def actualizar_mesa(self, mesa_id: UUID, **kwargs) -> Optional[Mesa]:
		mesa = self.obtener_mesa(mesa_id)
		if not mesa:
			return None
		if "capacidad" in kwargs and not self._validar_capacidad(kwargs["capacidad"]):
			raise ValueError("Capacidad inválida")
		for key, value in kwargs.items():
			if hasattr(mesa, key):
				setattr(mesa, key, value)
		self.db.commit()
		self.db.refresh(mesa)
		return mesa
"""
	def eliminar_mesa(self, mesa_id: UUID) -> bool:
		mesa = self.obtener_mesa(mesa_id)
		if not mesa:
			return False
		self.db.delete(mesa)
		self.db.commit()
		return True
"""