from datetime import datetime
from sqlalchemy.orm import Session
from entities.Reserva import Reserva
from typing import Optional, List
from uuid import UUID


class ReservaCRUD:
    """
    Operaciones CRUD para la entidad Reserva.
    """

    def __init__(self, db: Session):
        """Inicializa con una sesión de base de datos."""
        self.db = db

    def _validar_cantidad_personas(self, cantidad: int) -> bool:
        """Valida la cantidad de personas (debe ser un entero positivo)."""
        return isinstance(cantidad, int) and cantidad > 0

    def _validar_fecha_hora(self, fecha_hora) -> bool:
        """Valida la fecha y hora de la reserva (debe ser un objeto datetime)."""
        return isinstance(fecha_hora, datetime)

    def crear_reserva(
        self,
        id_cliente: UUID,
        id_mesa: UUID,
        cantidad_personas: int,
        fecha_Hora: datetime,
        Estado: bool,
        id_usuario: UUID,
    ) -> Reserva:
        """Crea una nueva reserva después de validar sus campos."""
        if not self._validar_cantidad_personas(cantidad_personas):
            raise ValueError("Cantidad de personas inválida")
        if not self._validar_fecha_hora(fecha_Hora):
            raise ValueError("Fecha y hora inválidas")
        reserva = Reserva(
            id_cliente=id_cliente,
            id_mesa=id_mesa,
            cantidad_personas=cantidad_personas,
            fecha_Hora=fecha_Hora,
            Estado=Estado,
            id_usuario=id_usuario,
        )
        self.db.add(reserva)
        self.db.commit()
        self.db.refresh(reserva)
        return reserva

    def obtener_reserva(self, id_cliente: UUID, id_mesa: UUID) -> Optional[Reserva]:
        """Obtiene una reserva por los UUIDs de cliente y mesa."""
        return (
            self.db.query(Reserva)
            .filter(Reserva.id_cliente == id_cliente, Reserva.id_mesa == id_mesa)
            .first()
        )

    def obtener_reservas(self, skip: int = 0) -> List[Reserva]:
        """Obtiene una lista de reservas, con salto opcional para paginación."""
        return self.db.query(Reserva).offset(skip).all()

    def actualizar_reserva(
        self, id_cliente: UUID, id_mesa: UUID, id_usuario_mod: UUID, **kwargs
    ) -> Optional[Reserva]:
        """Actualiza los campos de una reserva, actualizando id_usuario_mod y fecha_actualizacion solo si hay cambios."""
        from datetime import datetime

        reserva = self.obtener_reserva(id_cliente, id_mesa)
        if not reserva:
            return None
        cambios = False
        if "cantidad_personas" in kwargs and not self._validar_cantidad_personas(
            kwargs["cantidad_personas"]
        ):
            raise ValueError("Cantidad de personas inválida")
        if "fecha_Hora" in kwargs and not self._validar_fecha_hora(
            kwargs["fecha_Hora"]
        ):
            raise ValueError("Fecha y hora inválidas")
        for key, value in kwargs.items():
            if hasattr(reserva, key):
                if getattr(reserva, key) != value:
                    setattr(reserva, key, value)
                    cambios = True
        if cambios:
            if id_usuario_mod:
                reserva.id_usuario_mod = id_usuario_mod
            if hasattr(reserva, "fecha_actualizacion"):
                reserva.fecha_actualizacion = datetime.now()
            self.db.commit()
            self.db.refresh(reserva)
        return reserva

    def eliminar_reserva(self, id_cliente: UUID, id_mesa: UUID) -> bool:
        """Elimina una reserva por los UUIDs de cliente y mesa."""
        reserva = self.obtener_reserva(id_cliente, id_mesa)
        if not reserva:
            return False
        self.db.delete(reserva)
        self.db.commit()
        return True
