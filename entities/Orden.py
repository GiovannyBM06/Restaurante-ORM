import uuid
from sqlalchemy import Column, Integer, String, Date, ForeignKey, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from database.config import Base


class Orden(Base):
    __tablename__ = "orden"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    estado = Column(String, nullable=False, default="Pendiente")
    id_mesa = Column(UUID(as_uuid=True), ForeignKey("mesa.id"), nullable=False)
    id_empleado = Column(UUID(as_uuid=True), ForeignKey("empleado.id"), nullable=False)
    fecha_registro = Column(Date, nullable=False, default=datetime.now)
    fecha_actualizacion = Column(Date, default=datetime.now, onupdate=datetime.now)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("usuario.id"), nullable=False)
    id_usuario_mod = Column(UUID(as_uuid=True), ForeignKey("usuario.id"))

    mesa = relationship("Mesa", back_populates="ordenes")
    empleado = relationship("Empleado", back_populates="ordenes")
    facturas = relationship("Factura", back_populates="orden")
    platos_orden = relationship("Plato_Orden", back_populates="orden")

    usuario = relationship(
        "Usuario", back_populates="ordenes", foreign_keys=[id_usuario]
    )
    usuario_mod = relationship(
        "Usuario", foreign_keys=[id_usuario_mod], overlaps="usuario,ordenes"
    )

    def __repr__(self):
        return f"Orden(id={self.id}, estado='{self.estado}')"

    def to_dict(self):
        return {
            "id": self.id,
            "estado": self.estado,
            "numero_mesa": self.id_mesa,
            "id_empleado": self.id_empleado,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": (
                self.fecha_actualizacion if self.fecha_actualizacion else None
            ),
            "id_usuario": self.id_usuario,
            "id_usuario_mod": self.id_usuario_mod,
        }
