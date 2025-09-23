import uuid
from sqlalchemy import Column, Date, ForeignKey, UUID, Boolean, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from database.config import Base


class Reserva(Base):
    __tablename__ = "reserva"
    id_cliente = Column(
        UUID(as_uuid=True), ForeignKey("cliente.id"), primary_key=True, nullable=False
    )
    id_mesa = Column(
        UUID(as_uuid=True), ForeignKey("mesa.id"), primary_key=True, nullable=False
    )

    cantidad_personas = Column(Integer, nullable=False)
    fecha_Hora = Column(DateTime, nullable=False)
    Estado = Column(Boolean, nullable=False)
    fecha_registro = Column(Date, nullable=False, default=datetime.now)
    fecha_actualizacion = Column(Date, default=datetime.now, onupdate=datetime.now)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("usuario.id"), nullable=False)
    id_usuario_mod = Column(UUID(as_uuid=True), ForeignKey("usuario.id"))

    cliente = relationship("Cliente", back_populates="reservas")
    mesa = relationship("Mesa", back_populates="reservas")

    usuario = relationship(
        "Usuario", back_populates="reservas", foreign_keys=[id_usuario]
    )
    usuario_mod = relationship(
        "Usuario", foreign_keys=[id_usuario_mod], overlaps="usuario,reservas"
    )

    def __repr__(self):
        return f"Reserva(cantidad_personas={self.cantidad_personas}, fecha_Hora='{self.fecha_Hora}', id_cliente={self.id_cliente}, id_mesa={self.id_mesa})"

    def to_dict(self):
        return {
            "id_cliente": self.id_cliente,
            "id_mesa": self.id_mesa,
            "cantidad_personas": self.cantidad_personas,
            "fecha_Hora": self.fecha_Hora,
            "Estado": self.Estado,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": (
                self.fecha_actualizacion if self.fecha_actualizacion else None
            ),
            "id_usuario": self.id_usuario,
            "id_usuario_mod": self.id_usuario_mod,
        }
