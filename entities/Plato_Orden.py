import uuid
from sqlalchemy import Column, Integer, Date, ForeignKey, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from database.config import Base


class Plato_Orden(Base):
    """
    Modelo de la entidad Plato_Orden para la base de datos.
    """

    __tablename__ = "plato_orden"

    id_orden = Column(
        UUID(as_uuid=True), ForeignKey("orden.id"), primary_key=True, nullable=False
    )
    id_plato = Column(
        UUID(as_uuid=True), ForeignKey("plato.id"), primary_key=True, nullable=False
    )
    cantidad = Column(Integer, nullable=False)
    fecha_registro = Column(Date, nullable=False, default=datetime.now)
    fecha_actualizacion = Column(Date, nullable=True, default=None, onupdate=datetime.now)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("usuario.id"), nullable=False)
    id_usuario_mod = Column(UUID(as_uuid=True), ForeignKey("usuario.id"))

    orden = relationship("Orden", back_populates="platos_orden")
    plato = relationship("Plato", back_populates="platos_orden")

    usuario = relationship(
        "Usuario", back_populates="platos_orden", foreign_keys=[id_usuario]
    )
    usuario_mod = relationship(
        "Usuario", foreign_keys=[id_usuario_mod], overlaps="usuario,platos_orden"
    )

    def __repr__(self):
        return f"Plato_Orden(id_orden={self.id_orden}, id_plato={self.id_plato}, cantidad={self.cantidad})"

    def to_dict(self):
        return {
            "id_orden": self.id_orden,
            "id_plato": self.id_plato,
            "cantidad": self.cantidad,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": (
                self.fecha_actualizacion if self.fecha_actualizacion else None
            ),
            "id_usuario": self.id_usuario,
            "id_usuario_mod": self.id_usuario_mod,
        }
