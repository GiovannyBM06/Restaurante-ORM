import uuid
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from database.config import Base


class Categoria(Base):
    """
    Modelo de la entidad Categoria para la base de datos.
    """

    __tablename__ = "categoria"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nombre = Column(String(20), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_registro = Column(Date, nullable=False, default=datetime.now)
    fecha_actualizacion = Column(
        Date, nullable=True, default=None, onupdate=datetime.now
    )
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("usuario.id"), nullable=False)
    id_usuario_mod = Column(UUID(as_uuid=True), ForeignKey("usuario.id"))

    platos = relationship("Plato", back_populates="categoria")

    usuario = relationship(
        "Usuario", back_populates="categorias", foreign_keys=[id_usuario]
    )
    usuario_mod = relationship(
        "Usuario", foreign_keys=[id_usuario_mod], overlaps="usuario,categorias"
    )

    def __repr__(self):
        return f"Categoria(id={self.id}, nombre='{self.nombre}', descripcion='{self.descripcion}')"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": (
                self.fecha_actualizacion if self.fecha_actualizacion else None
            ),
            "id_usuario": self.id_usuario,
            "id_usuario_mod": self.id_usuario_mod,
        }
