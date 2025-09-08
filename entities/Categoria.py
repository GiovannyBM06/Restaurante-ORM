from sqlalchemy import column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class Categoria(Base):
    __tablename__ = 'Categoria'
    id = column(Integer, primary_key=True, autoincrement=True)
    nombre = column(String(20), nullable=False)
    descripcion = column(Text, nullable=True)
    fecha_registro = column(Date, nullable=False, default = datetime.now)
    fecha_actualizacion = column(Date,default= datetime.now, onupdate=datetime.now)
    id_usuario = column(Integer, ForeignKey('Usuario.id'), nullable=False)

    Plato = relationship("Plato", back_populates="Categoria")    

    def __repr__(self):
        return f"Categoria(id={self.id}, nombre='{self.nombre}', descripcion='{self.descripcion}')"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion if self.fecha_actualizacion else None,
            "id_usuario": self.id_usuario
        }