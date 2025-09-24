from sqlalchemy.orm import Session
from entities.Mesa import Mesa
from typing import Optional, List
from uuid import UUID


class MesaCRUD:
    """
    Operaciones CRUD para la entidad Mesa.
    """

    def __init__(self, db: Session):
        """Inicializa con una sesión de base de datos."""
        self.db = db

    def _validar_capacidad(self, capacidad: int) -> bool:
        """Valida la capacidad de la mesa (debe ser un entero positivo)."""
        return isinstance(capacidad, int) and capacidad > 0

    def crear_mesa(self, capacidad: int, id_usuario: UUID) -> Mesa:
        """Crea una nueva mesa después de validar su capacidad."""
        if not self._validar_capacidad(capacidad):
            raise ValueError("Capacidad inválida")
        mesa = Mesa(capacidad=capacidad, id_usuario=id_usuario)
        self.db.add(mesa)
        self.db.commit()
        self.db.refresh(mesa)
        return mesa

    def obtener_mesa(self, mesa_id: UUID) -> Optional[Mesa]:
        """Obtiene una mesa por su UUID."""
        return self.db.query(Mesa).filter(Mesa.id == mesa_id).first()

    def obtener_mesas(self, skip: int = 0) -> List[Mesa]:
        """Obtiene una lista de mesas, con salto opcional para paginación."""
        return self.db.query(Mesa).offset(skip).all()

    def actualizar_mesa(self, mesa_id: UUID, id_usuario_mod: UUID, **kwargs) -> Optional[Mesa]:
        """Actualiza los campos de una mesa, actualizando id_usuario_mod y fecha_actualizacion solo si hay cambios."""
        from datetime import datetime
        mesa = self.obtener_mesa(mesa_id)
        if not mesa:
            return None
        cambios = False
        if "capacidad" in kwargs and not self._validar_capacidad(kwargs["capacidad"]):
            raise ValueError("Capacidad inválida")
        for key, value in kwargs.items():
            if hasattr(mesa, key):
                if getattr(mesa, key) != value:
                    setattr(mesa, key, value)
                    cambios = True
        if cambios:
            if id_usuario_mod:
                mesa.id_usuario_mod = id_usuario_mod
            if hasattr(mesa, "fecha_actualizacion"):
                mesa.fecha_actualizacion = datetime.now()
            self.db.commit()
            self.db.refresh(mesa)
        return mesa

    def eliminar_mesa(self, mesa_id: UUID) -> bool:
        """Elimina una mesa por su UUID."""
        mesa = self.obtener_mesa(mesa_id)
        if not mesa:
            return False
        self.db.delete(mesa)
        self.db.commit()
        return True
