from sqlalchemy import column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class Orden(Base):
    __tablename__ = 'Orden'
    num_orden = column(Integer, primary_key=True, autoincrement=True)
    estado = column(Boolean, nullable=False)
    fecha_registro = column(Date, nullable=False, default = datetime.now)
    fecha_actualizacion = column(Date, default= datetime.now, onupdate=datetime.now)
    id_usuario = column(Integer, ForeignKey('Usuario.id'), nullable=False)

    Reserva = relationship("Reserva", back_populates= "Orden")
    Empleado= relationship("Empleado", back_populates= "Orden")
    Factura = relationship("Factura", back_populates= "Orden")
    Plato_Orden = relationship("Plato_Orden", back_populates= "Orden")

    def __repr__(self):
        return f"Orden(num_orden={self.num_orden}, estado={self.estado})"
    
    def to_dict(self):
        return {
            "num_orden": self.num_orden,
            "estado": self.estado,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion if self.fecha_actualizacion else None,
            "id_usuario": self.id_usuario
        }
    