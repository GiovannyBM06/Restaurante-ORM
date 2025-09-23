import uuid
from sqlalchemy import Column, Integer, Date, ForeignKey, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from database.config import Base


class Mesa(Base):
    """
    Modelo de la entidad Mesa para la base de datos.
    """

    __tablename__ = "mesa"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    capacidad = Column(Integer, nullable=False)
    fecha_registro = Column(Date, nullable=False, default=datetime.now)
    fecha_actualizacion = Column(Date, default=datetime.now, onupdate=datetime.now)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("usuario.id"), nullable=False)
    id_usuario_mod = Column(UUID(as_uuid=True), ForeignKey("usuario.id"))

    reservas = relationship("Reserva", back_populates="mesa")
    ordenes = relationship("Orden", back_populates="mesa")

    usuario = relationship("Usuario", back_populates="mesas", foreign_keys=[id_usuario])
    usuario_mod = relationship(
        "Usuario", foreign_keys=[id_usuario_mod], overlaps="usuario,mesas"
    )

    def __repr__(self):
        return f"Mesa(id={self.id}, capacidad={self.capacidad})"

    def to_dict(self):
        return {
            "id": self.id,
            "capacidad": self.capacidad,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": (
                self.fecha_actualizacion if self.fecha_actualizacion else None
            ),
            "id_usuario": self.id_usuario,
            "id_usuario_mod": self.id_usuario_mod,
        }
