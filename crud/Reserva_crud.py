from sqlalchemy.orm import Session
from entities.Reserva import Reserva
from typing import Optional, List
from uuid import UUID
from datetime import datetime
import re

class ReservaCRUD:
	def __init__(self, db: Session):
		self.db = db

	def _validar_cantidad_personas(self, cantidad: int) -> bool:
		return isinstance(cantidad, int) and cantidad > 0

	def _validar_fecha_hora(self, fecha_hora) -> bool:
		return isinstance(fecha_hora, datetime)

	def crear_reserva(self, id_cliente: UUID, id_mesa: UUID, cantidad_personas: int, fecha_Hora: datetime, Estado: bool, id_usuario: UUID) -> Reserva:
		if not self._validar_cantidad_personas(cantidad_personas):
			raise ValueError("Cantidad de personas inválida")
		if not self._validar_fecha_hora(fecha_Hora):
			raise ValueError("Fecha y hora inválidas")
		reserva = Reserva(id_cliente=id_cliente, id_mesa=id_mesa, cantidad_personas=cantidad_personas, fecha_Hora=fecha_Hora, Estado=Estado, id_usuario=id_usuario)
		self.db.add(reserva)
		self.db.commit()
		self.db.refresh(reserva)
		return reserva

	def obtener_reserva(self, id_cliente: UUID, id_mesa: UUID) -> Optional[Reserva]:
		return self.db.query(Reserva).filter(Reserva.id_cliente == id_cliente, Reserva.id_mesa == id_mesa).first()

	def obtener_reservas(self, skip: int = 0) -> List[Reserva]:
		return self.db.query(Reserva).offset(skip).all()

	def actualizar_reserva(self, id_cliente: UUID, id_mesa: UUID, **kwargs) -> Optional[Reserva]:
		reserva = self.obtener_reserva(id_cliente, id_mesa)
		if not reserva:
			return None
		if "cantidad_personas" in kwargs and not self._validar_cantidad_personas(kwargs["cantidad_personas"]):
			raise ValueError("Cantidad de personas inválida")
		if "fecha_Hora" in kwargs and not self._validar_fecha_hora(kwargs["fecha_Hora"]):
			raise ValueError("Fecha y hora inválidas")
		for key, value in kwargs.items():
			if hasattr(reserva, key):
				setattr(reserva, key, value)
		self.db.commit()
		self.db.refresh(reserva)
		return reserva
"""
	def eliminar_reserva(self, id_cliente: UUID, id_mesa: UUID) -> bool:
		reserva = self.obtener_reserva(id_cliente, id_mesa)
		if not reserva:
			return False
		self.db.delete(reserva)
		self.db.commit()
		return True
"""