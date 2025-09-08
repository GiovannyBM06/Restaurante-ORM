from sqlalchemy import column, Integer, String,float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class Ingrediente(Base):
    __tablename__ = 'Ingrediente'
    id = column(Integer, primary_key=True, autoincrement=True)
    nombre = column(String(25), nullable=False)
    stock = column(float, nullable=False)
    unidad_medida = column(String(10), nullable=False)
    id_proveedor = column(Integer, ForeignKey('Proveedor.id'), nullable=False)
    fecha_registro = column(Date, nullable=False, default = datetime.now)
    fecha_actualizacion = column(Date, default= datetime.now, onupdate=datetime.now)
    id_usuario = column(Integer, ForeignKey('Usuario.id'), nullable=False)

    proveedor = relationship('Proveedor', back_populates='ingrediente')
    Plato_Ingrediente = relationship("Plato_Ingrediente", back_populates="Ingrediente")

    def __repr__(self):
        return f"Ingrediente(id={self.id}, nombre='{self.nombre}', stock={self.stock}, unidad_medida='{self.unidad_medida}', id_proveedor={self.id_proveedor})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "stock": self.stock,
            "unidad_medida": self.unidad_medida,
            "id_proveedor": self.id_proveedor,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion if self.fecha_actualizacion else None,
            "id_usuario": self.id_usuario
        }