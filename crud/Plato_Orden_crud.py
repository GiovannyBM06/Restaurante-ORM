from sqlalchemy.orm import Session
from entities.Plato_Orden import Plato_Orden
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class PlatoOrdenCRUD:
    """
    Operaciones CRUD para la entidad Plato_Orden.
    """

    def __init__(self, db: Session):
        """Inicializa con una sesión de base de datos."""
        self.db = db

    def _validar_cantidad(self, cantidad: int) -> bool:
        """Valida la cantidad (debe ser un entero positivo)."""
        return isinstance(cantidad, int) and cantidad > 0

    def _validar_fecha(self, fecha) -> bool:
        """Valida la fecha (debe ser un objeto datetime)."""
        return isinstance(fecha, datetime)

    def crear_plato_orden(
        self, id_orden: UUID, id_plato: UUID, cantidad: int, id_usuario: UUID
    ) -> Plato_Orden:
        """Crea un nuevo Plato_Orden después de validar sus campos."""
        if not self._validar_cantidad(cantidad):
            raise ValueError("Cantidad inválida")
        plato_orden = Plato_Orden(
            id_orden=id_orden,
            id_plato=id_plato,
            cantidad=cantidad,
            id_usuario=id_usuario,
        )
        self.db.add(plato_orden)
        self.db.commit()
        self.db.refresh(plato_orden)
        return plato_orden

    def obtener_plato_orden(
        self, id_orden: UUID, id_plato: UUID
    ) -> Optional[Plato_Orden]:
        """Obtiene un Plato_Orden por los UUIDs de orden y plato."""
        return (
            self.db.query(Plato_Orden)
            .filter(Plato_Orden.id_orden == id_orden, Plato_Orden.id_plato == id_plato)
            .first()
        )

    def obtener_platos_orden(self, skip: int = 0) -> List[Plato_Orden]:
        """Obtiene una lista de Plato_Orden, con salto opcional para paginación."""
        return self.db.query(Plato_Orden).offset(skip).all()

    def actualizar_plato_orden(
        self, id_orden: UUID, id_plato: UUID, id_usuario_mod: UUID, **kwargs
    ) -> Optional[Plato_Orden]:
        """Actualiza los campos de un Plato_Orden, actualizando id_usuario_mod y fecha_actualizacion solo si hay cambios."""
        from datetime import datetime
        plato_orden = self.obtener_plato_orden(id_orden, id_plato)
        if not plato_orden:
            return None
        cambios = False
        if "cantidad" in kwargs and not self._validar_cantidad(kwargs["cantidad"]):
            raise ValueError("Cantidad inválida")
        for key, value in kwargs.items():
            if hasattr(plato_orden, key):
                if getattr(plato_orden, key) != value:
                    setattr(plato_orden, key, value)
                    cambios = True
        if cambios:
            if id_usuario_mod:
                plato_orden.id_usuario_mod = id_usuario_mod
            if hasattr(plato_orden, "fecha_actualizacion"):
                plato_orden.fecha_actualizacion = datetime.now()
            self.db.commit()
            self.db.refresh(plato_orden)
        return plato_orden

    def eliminar_plato_orden(self, id_orden: UUID, id_plato: UUID) -> bool:
        """Elimina un Plato_Orden por los UUIDs de orden y plato."""
        plato_orden = self.obtener_plato_orden(id_orden, id_plato)
        if not plato_orden:
            return False
        self.db.delete(plato_orden)
        self.db.commit()
        return True
