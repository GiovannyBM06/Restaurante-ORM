from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from database.config import Base

class Orden(Base):
    __tablename__ = 'orden'
    numero = Column(Integer, primary_key=True, autoincrement=True)
    estado = Column(String, nullable=False, default='Pendiente')
    numero_mesa = Column(Integer, ForeignKey('mesa.numero'), nullable=False)
    id_empleado = Column(Integer, ForeignKey('empleado.id'), nullable=False)
    fecha_registro = Column(Date, nullable=False, default = datetime.now)
    fecha_actualizacion = Column(Date, default= datetime.now, onupdate=datetime.now)
    id_usuario = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    id_usuario_mod = Column(Integer, ForeignKey('usuario.id'))

    mesa = relationship("Mesa", back_populates="ordenes")
    empleado = relationship("Empleado", back_populates="ordenes")
    facturas = relationship("Factura", back_populates="orden")
    platos_orden = relationship("Plato_Orden", back_populates="orden")

    usuario = relationship("Usuario", back_populates="ordenes", foreign_keys=[id_usuario])
    usuario_mod = relationship("Usuario", foreign_keys=[id_usuario_mod], overlaps="usuario,ordenes")

    def __repr__(self):
        return f"Orden(numero={self.numero}, estado='{self.estado}')"
    
    def to_dict(self):
        return {
            "numero": self.numero,
            "estado": self.estado,
            "numero_mesa": self.numero_mesa,
            "id_empleado": self.id_empleado,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion if self.fecha_actualizacion else None,
            "id_usuario": self.id_usuario,
            "id_usuario_mod": self.id_usuario_mod
        }
    