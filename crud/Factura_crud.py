from sqlalchemy.orm import Session
from entities.Factura import Factura
from typing import Optional, List
from uuid import UUID
import re


class FacturaCRUD:
    """
    Operaciones CRUD para la entidad Factura.
    """

    def __init__(self, db: Session):
        """Inicializa con una sesión de base de datos."""
        self.db = db

    def _validar_total(self, total: float) -> bool:
        """Valida el monto total (debe ser un número no negativo)."""
        return isinstance(total, (int, float)) and total >= 0

    def _validar_metodo_pago(self, metodo_pago: str) -> bool:
        """Valida el método de pago (debe ser uno de los permitidos)."""
        return metodo_pago in ["Efectivo", "Tarjeta", "Transferencia"]

    def crear_factura(
        self, total: float, metodo_pago: str, id_orden: UUID, id_usuario: UUID
    ) -> Factura:
        """Crea una nueva factura después de validar sus campos."""
        if not self._validar_total(total):
            raise ValueError("Total inválido")
        if not self._validar_metodo_pago(metodo_pago):
            raise ValueError("Método de pago inválido")
        factura = Factura(
            total=total,
            metodo_pago=metodo_pago.strip(),
            id_orden=id_orden,
            id_usuario=id_usuario,
        )
        self.db.add(factura)
        self.db.commit()
        self.db.refresh(factura)
        return factura

    def obtener_factura(self, factura_id: UUID) -> Optional[Factura]:
        """Obtiene una factura por su UUID."""
        return self.db.query(Factura).filter(Factura.id == factura_id).first()

    def obtener_facturas(self, skip: int = 0) -> List[Factura]:
        """Obtiene una lista de facturas, con salto opcional para paginación."""
        return self.db.query(Factura).offset(skip).all()

    def actualizar_factura(self, factura_id: UUID, id_usuario_mod: UUID, **kwargs) -> Optional[Factura]:
        """Actualiza los campos de una factura, actualizando id_usuario_mod y fecha_actualizacion solo si hay cambios."""
        from datetime import datetime

        factura = self.obtener_factura(factura_id)
        if not factura:
            return None
        cambios = False
        if "total" in kwargs and not self._validar_total(kwargs["total"]):
            raise ValueError("Total inválido")
        if "metodo_pago" in kwargs and not self._validar_metodo_pago(
            kwargs["metodo_pago"]
        ):
            raise ValueError("Método de pago inválido")
        for key, value in kwargs.items():
            if hasattr(factura, key):
                if getattr(factura, key) != value:
                    setattr(factura, key, value)
                    cambios = True
        if cambios:
            if id_usuario_mod:
                factura.id_usuario_mod = id_usuario_mod
            if hasattr(factura, "fecha_actualizacion"):
                factura.fecha_actualizacion = datetime.now()
            self.db.commit()
            self.db.refresh(factura)
        return factura

    def eliminar_factura(self, factura_id: UUID) -> bool:
        """Elimina una factura por su UUID."""
        factura = self.obtener_factura(factura_id)
        if not factura:
            return False
        self.db.delete(factura)
        self.db.commit()
        return True
