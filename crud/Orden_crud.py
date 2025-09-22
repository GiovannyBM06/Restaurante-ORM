from sqlalchemy.orm import Session
from entities.Orden import Orden
from typing import Optional, List
from uuid import UUID
import re

class OrdenCRUD:
	def __init__(self, db: Session):
		self.db = db

	def _validar_estado(self, estado: str) -> bool:
		return estado in ["Pendiente", "En Proceso", "Completada", "Cancelada"]

	def crear_orden(self, estado: str, id_mesa: UUID, id_empleado: UUID, id_usuario: UUID) -> Orden:
		if not self._validar_estado(estado):
			raise ValueError("Estado inválido")
		orden = Orden(estado=estado, id_mesa=id_mesa, id_empleado=id_empleado, id_usuario=id_usuario)
		self.db.add(orden)
		self.db.commit()
		self.db.refresh(orden)
		return orden

	def obtener_orden(self, orden_id: UUID) -> Optional[Orden]:
		return self.db.query(Orden).filter(Orden.id == orden_id).first()

	def obtener_ordenes(self, skip: int = 0) -> List[Orden]:
		return self.db.query(Orden).offset(skip).all()

	def actualizar_orden(self, orden_id: UUID, **kwargs) -> Optional[Orden]:
		orden = self.obtener_orden(orden_id)
		if not orden:
			return None
		if "estado" in kwargs and not self._validar_estado(kwargs["estado"]):
			raise ValueError("Estado inválido")
		for key, value in kwargs.items():
			if hasattr(orden, key):
				setattr(orden, key, value)
		self.db.commit()
		self.db.refresh(orden)
		return orden
"""
	def eliminar_orden(self, orden_id: UUID) -> bool:
		orden = self.obtener_orden(orden_id)
		if not orden:
			return False
		self.db.delete(orden)
		self.db.commit()
		return True
"""