from sqlalchemy import column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class Proveedor(Base):
    __tablename__ = 'Proveedor'
    id = column(Integer, primary_key=True, autoincrement=True)
    nombre = column(String(50), nullable=False)
    telefono = column(String(15), nullable=True, unique=True)
    email = column(String(50), nullable=True, unique=True)
    direccion = column(String(100), nullable=True)
    fecha_registro = column(Date, nullable=False, default = datetime.now)
    fecha_actualizacion = column(Date, default= datetime.now, onupdate=datetime.now)
    id_usuario = column(Integer, ForeignKey('Usuario.id'), nullable=False)

    ingredientes = relationship('Ingrediente', back_populates='proveedor')

    def __repr__(self):
        return f"Proveedor(id={self.id}, nombre='{self.nombre}', telefono='{self.telefono}', email='{self.email}', direccion='{self.direccion}')"
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "email": self.email,
            "direccion": self.direccion,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion if self.fecha_actualizacion else None,
            "id_usuario": self.id_usuario
        }