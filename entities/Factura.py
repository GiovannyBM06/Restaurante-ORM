import uuid
from sqlalchemy import Column, Integer, String, Date, ForeignKey, UUID, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from database.config import Base


class Factura(Base):
    __tablename__ = "factura"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    total = Column(Float, nullable=False)
    metodo_pago = Column(String(20), nullable=False)
    id_orden = Column(UUID(as_uuid=True), ForeignKey("orden.id"), nullable=False)
    fecha_registro = Column(Date, nullable=False, default=datetime.now)
    fecha_actualizacion = Column(Date, default=datetime.now, onupdate=datetime.now)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("usuario.id"), nullable=False)
    id_usuario_mod = Column(UUID(as_uuid=True), ForeignKey("usuario.id"))

    orden = relationship("Orden", back_populates="facturas")

    usuario = relationship(
        "Usuario", back_populates="facturas", foreign_keys=[id_usuario]
    )
    usuario_mod = relationship(
        "Usuario", foreign_keys=[id_usuario_mod], overlaps="usuario,facturas"
    )

    def __repr__(self):
        return f"Factura(id={self.id}, total={self.total}, metodo_pago='{self.metodo_pago}', id_orden={self.id_orden})"

    def to_dict(self):
        return {
            "id": self.id,
            "total": self.total,
            "metodo_pago": self.metodo_pago,
            "numero_orden": self.id_orden,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": (
                self.fecha_actualizacion if self.fecha_actualizacion else None
            ),
            "id_usuario": self.id_usuario,
            "id_usuario_mod": self.id_usuario_mod,
        }
