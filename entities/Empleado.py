import uuid
from sqlalchemy import Column, Integer, String, Date, ForeignKey, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from database.config import Base


class Empleado(Base):
    """
    Modelo de la entidad Empleado para la base de datos.
    """

    __tablename__ = "empleado"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nombre = Column(String(20), nullable=False)
    apellido = Column(String(20), nullable=False)
    rol = Column(String(20), nullable=False)
    salario = Column(Integer, nullable=False)
    fecha_registro = Column(Date, nullable=False, default=datetime.now)
    fecha_actualizacion = Column(Date, nullable=True, default=None, onupdate=datetime.now)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("usuario.id"), nullable=False)
    id_usuario_mod = Column(UUID(as_uuid=True), ForeignKey("usuario.id"))

    ordenes = relationship("Orden", back_populates="empleado")

    usuario = relationship(
        "Usuario", back_populates="empleados", foreign_keys=[id_usuario]
    )
    usuario_mod = relationship(
        "Usuario", foreign_keys=[id_usuario_mod], overlaps="usuario,empleados"
    )

    def __repr__(self):
        return f"Empleado(id={self.id}, nombre='{self.nombre}', apellido='{self.apellido}', rol='{self.rol}', salario={self.salario})"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "rol": self.rol,
            "salario": self.salario,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": (
                self.fecha_actualizacion if self.fecha_actualizacion else None
            ),
            "id_usuario": self.id_usuario,
            "id_usuario_mod": self.id_usuario_mod,
        }
