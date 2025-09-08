from sqlalchemy import column, Integer,Float, String, Date, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class Factuta(Base):
    __tablename__ = 'Factura'
    id = column(Integer, primary_key=True, autoincrement=True)
    total = column(Float, nullable=False)
    metodo_pago = column(String(20), nullable=False)
    id_orden = column(Integer, ForeignKey('Orden.num_orden'), nullable=False)
    fecha_registro = column(Date, nullable=False, default = datetime.now)
    fecha_actualizacion = column(Date, default= datetime.now, onupdate=datetime.now)
    id_usuario = column(Integer, ForeignKey('Usuario.id'), nullable=False)

    Orden = relationship("Orden", back_populates="Factura")

    def __repr__(self):
        return f"Factura(id={self.id}, total={self.total}, metodo_pago='{self.metodo_pago}', id_orden={self.id_orden})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "total": self.total,
            "metodo_pago": self.metodo_pago,
            "id_orden": self.id_orden,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion if self.fecha_actualizacion else None,
            "id_usuario": self.id_usuario
        }