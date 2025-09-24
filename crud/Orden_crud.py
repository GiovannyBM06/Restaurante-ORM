from sqlalchemy.orm import Session
from entities.Orden import Orden
from typing import Optional, List
from uuid import UUID
import re


class OrdenCRUD:
    """
    Operaciones CRUD para la entidad Orden.
    """

    def __init__(self, db: Session):
        """Inicializa con una sesión de base de datos."""
        self.db = db

    def _validar_estado(self, estado: str) -> bool:
        """Valida el estado de la orden (debe ser uno de los permitidos)."""
        return estado in ["Pendiente", "En Proceso", "Completada", "Cancelada"]

    def crear_orden(
        self, estado: str, id_mesa: UUID, id_empleado: UUID, id_usuario: UUID
    ) -> Orden:
        """Crea una nueva orden después de validar sus campos."""
        if not self._validar_estado(estado):
            raise ValueError("Estado inválido")
        orden = Orden(
            estado=estado,
            id_mesa=id_mesa,
            id_empleado=id_empleado,
            id_usuario=id_usuario,
        )
        self.db.add(orden)
        self.db.commit()
        self.db.refresh(orden)
        return orden

    def obtener_orden(self, orden_id: UUID) -> Optional[Orden]:
        """Obtiene una orden por su UUID."""
        return self.db.query(Orden).filter(Orden.id == orden_id).first()

    def obtener_ordenes(self, skip: int = 0) -> List[Orden]:
        """Obtiene una lista de órdenes, con salto opcional para paginación."""
        return self.db.query(Orden).offset(skip).all()

    def actualizar_orden(self, orden_id: UUID, id_usuario_mod: UUID, **kwargs) -> Optional[Orden]:
        """Actualiza los campos de una orden, actualizando id_usuario_mod y fecha_actualizacion solo si hay cambios."""
        from datetime import datetime
        orden = self.obtener_orden(orden_id)
        if not orden:
            return None
        cambios = False
        if "estado" in kwargs and not self._validar_estado(kwargs["estado"]):
            raise ValueError("Estado inválido")
        for key, value in kwargs.items():
            if hasattr(orden, key):
                if getattr(orden, key) != value:
                    setattr(orden, key, value)
                    cambios = True
        if cambios:
            if id_usuario_mod:
                orden.id_usuario_mod = id_usuario_mod
            if hasattr(orden, "fecha_actualizacion"):
                orden.fecha_actualizacion = datetime.now()
            self.db.commit()
            self.db.refresh(orden)
        return orden

    def eliminar_orden(self, orden_id: UUID) -> bool:
        """Elimina una orden por su UUID."""
        orden = self.obtener_orden(orden_id)
        if not orden:
            return False
        self.db.delete(orden)
        self.db.commit()
        return True
