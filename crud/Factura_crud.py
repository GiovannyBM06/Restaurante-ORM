from sqlalchemy.orm import Session
from entities.Factura import Factura
from typing import Optional, List
from uuid import UUID
import re

class FacturaCRUD:
	def __init__(self, db: Session):
		self.db = db

	def _validar_total(self, total: float) -> bool:
		return isinstance(total, (int, float)) and total >= 0

	def _validar_metodo_pago(self, metodo_pago: str) -> bool:
		return metodo_pago in ["Efectivo", "Tarjeta", "Transferencia"]

	def crear_factura(self, total: float, metodo_pago: str, id_orden: UUID, id_usuario: UUID) -> Factura:
		if not self._validar_total(total):
			raise ValueError("Total inválido")
		if not self._validar_metodo_pago(metodo_pago):
			raise ValueError("Método de pago inválido")
		factura = Factura(total=total, metodo_pago=metodo_pago.strip(), id_orden=id_orden, id_usuario=id_usuario)
		self.db.add(factura)
		self.db.commit()
		self.db.refresh(factura)
		return factura

	def obtener_factura(self, factura_id: UUID) -> Optional[Factura]:
		return self.db.query(Factura).filter(Factura.id == factura_id).first()

	def obtener_facturas(self, skip: int = 0) -> List[Factura]:
		return self.db.query(Factura).offset(skip).all()

	def actualizar_factura(self, factura_id: UUID, **kwargs) -> Optional[Factura]:
		factura = self.obtener_factura(factura_id)
		if not factura:
			return None
		if "total" in kwargs and not self._validar_total(kwargs["total"]):
			raise ValueError("Total inválido")
		if "metodo_pago" in kwargs and not self._validar_metodo_pago(kwargs["metodo_pago"]):
			raise ValueError("Método de pago inválido")
		for key, value in kwargs.items():
			if hasattr(factura, key):
				setattr(factura, key, value)
		self.db.commit()
		self.db.refresh(factura)
		return factura
"""
	def eliminar_factura(self, factura_id: UUID) -> bool:
		factura = self.obtener_factura(factura_id)
		if not factura:
			return False
		self.db.delete(factura)
		self.db.commit()
		return True
"""