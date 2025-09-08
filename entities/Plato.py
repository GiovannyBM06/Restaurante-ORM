from sqlalchemy import column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class Plato(Base):
    __tablename__ = 'Plato'

    id = column(Integer, primary_key=True, autoincrement=True)
    nombre = column(String(20), nullable=False)
    precio = column(Integer, nullable=False)
    descripcion = column(String(100), nullable=True)
    id_categoria = column(Integer, ForeignKey('Categoria.id'), nullable=False)
    fecha_registro = column(Date, nullable=False, default= datetime.now)
    fecha_actualizacion = column(Date, default= datetime.now, onupdate=datetime.now)
    id_usuario = column(Integer, ForeignKey('Usuario.id'), nullable=False)

    Categoria = relationship("Categoria", back_populates="platos")
    Plato_Ingrediente = relationship("Plato_Ingrediente", back_populates="Plato")
    Plato_Orden = relationship("Plato_Orden", back_populates="Plato")

    def __repr__(self):
        return f"Plato(id={self.id}, nombre='{self.nombre}', precio={self.precio}, descripcion='{self.descripcion}', id_categoria={self.id_categoria})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "descripcion": self.descripcion,
            "id_categoria": self.id_categoria,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion if self.fecha_actualizacion else None,
            "id_usuario": self.id_usuario
        }