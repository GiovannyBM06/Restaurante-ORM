from sqlalchemy.orm import Session
from entities.Plato_Orden import Plato_Orden
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class PlatoOrdenCRUD:
	def __init__(self, db: Session):
		self.db = db

	def _validar_cantidad(self, cantidad: int) -> bool:
		return isinstance(cantidad, int) and cantidad > 0

	def _validar_fecha(self, fecha) -> bool:
		return isinstance(fecha, datetime)

	def crear_plato_orden(self, id_orden: UUID, id_plato: UUID, cantidad: int, id_usuario: UUID) -> Plato_Orden:
		if not self._validar_cantidad(cantidad):
			raise ValueError("Cantidad inválida")
		plato_orden = Plato_Orden(id_orden=id_orden, id_plato=id_plato, cantidad=cantidad, id_usuario=id_usuario)
		self.db.add(plato_orden)
		self.db.commit()
		self.db.refresh(plato_orden)
		return plato_orden

	def obtener_plato_orden(self, id_orden: UUID, id_plato: UUID) -> Optional[Plato_Orden]:
		return self.db.query(Plato_Orden).filter(Plato_Orden.id_orden == id_orden, Plato_Orden.id_plato == id_plato).first()

	def obtener_platos_orden(self, skip: int = 0) -> List[Plato_Orden]:
		return self.db.query(Plato_Orden).offset(skip).all()

	def actualizar_plato_orden(self, id_orden: UUID, id_plato: UUID, **kwargs) -> Optional[Plato_Orden]:
		plato_orden = self.obtener_plato_orden(id_orden, id_plato)
		if not plato_orden:
			return None
		if "cantidad" in kwargs and not self._validar_cantidad(kwargs["cantidad"]):
			raise ValueError("Cantidad inválida")
		for key, value in kwargs.items():
			if hasattr(plato_orden, key):
				setattr(plato_orden, key, value)
		self.db.commit()
		self.db.refresh(plato_orden)
		return plato_orden
"""
	def eliminar_plato_orden(self, id_orden: UUID, id_plato: UUID) -> bool:
		plato_orden = self.obtener_plato_orden(id_orden, id_plato)
		if not plato_orden:
			return False
		self.db.delete(plato_orden)
		self.db.commit()
		return True
"""