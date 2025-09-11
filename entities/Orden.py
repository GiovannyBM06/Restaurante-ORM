from sqlalchemy import column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class Orden(Base):
    __tablename__ = 'Orden'
    numero = column(Integer, primary_key=True, autoincrement=True)
    estado = column(String, nullable=False, default='Pendiente')
    numero_mesa = column(Integer, ForeignKey('Mesa.numero'), nullable=False)
    id_empleado = column(Integer, ForeignKey('Empleado.id'), nullable=False)
    fecha_registro = column(Date, nullable=False, default = datetime.now)
    fecha_actualizacion = column(Date, default= datetime.now, onupdate=datetime.now)
    id_usuario = column(Integer, ForeignKey('Usuario.id'), nullable=False)
    id_usuario_mod = column(Integer, ForeignKey('Usuario.id'))

    Mesa = relationship("Mesa", back_populates= "Orden")
    Empleado= relationship("Empleado", back_populates= "Orden")
    Factura = relationship("Factura", back_populates= "Orden")
    Plato_Orden = relationship("Plato_Orden", back_populates= "Orden")
    Usuario = relationship("Usuario", back_populates="Orden")

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
    