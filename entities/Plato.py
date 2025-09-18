from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from database.config import Base

class Plato(Base):
    __tablename__ = 'plato'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(20), nullable=False)
    precio_unidad = Column(Integer, nullable=False)
    descripcion = Column(String(100), nullable=True)
    id_categoria = Column(Integer, ForeignKey('categoria.id'), nullable=False)
    fecha_registro = Column(Date, nullable=False, default= datetime.now)
    fecha_actualizacion = Column(Date, default= datetime.now, onupdate=datetime.now)
    id_usuario = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    id_usuario_mod = Column(Integer, ForeignKey('usuario.id'))

    def __repr__(self):
        return f"Plato(id={self.id}, nombre='{self.nombre}', precio={self.precio_unidad}, descripcion='{self.descripcion}', id_categoria={self.id_categoria})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio_unidad,
            "descripcion": self.descripcion,
            "id_categoria": self.id_categoria,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion if self.fecha_actualizacion else None,
            "id_usuario": self.id_usuario,
            "id_usuario_mod": self.id_usuario_mod   
        }

    categoria = relationship("Categoria", back_populates="platos")
    platos_orden = relationship("Plato_Orden", back_populates="plato")
    usuario = relationship(
        "Usuario",
        back_populates="platos",
        foreign_keys=[id_usuario],
        overlaps="usuario_mod"
    )
    usuario_mod = relationship(
        "Usuario",
        foreign_keys=[id_usuario_mod],
        overlaps="usuario,platos"
    )