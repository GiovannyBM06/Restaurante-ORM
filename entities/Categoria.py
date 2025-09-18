from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from database.config import Base

class Categoria(Base):
    __tablename__ = 'categoria'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(20), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_registro = Column(Date, nullable=False, default = datetime.now)
    fecha_actualizacion = Column(Date,default= datetime.now, onupdate=datetime.now)
    id_usuario = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    id_usuario_mod = Column(Integer, ForeignKey('usuario.id'))

    platos = relationship("Plato", back_populates="categoria")

    usuario = relationship("Usuario", back_populates="categorias", foreign_keys=[id_usuario])
    usuario_mod = relationship("Usuario", foreign_keys=[id_usuario_mod], overlaps="usuario,categorias")


    def __repr__(self):
        return f"Categoria(id={self.id}, nombre='{self.nombre}', descripcion='{self.descripcion}')"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion if self.fecha_actualizacion else None,
            "id_usuario": self.id_usuario,
            "id_usuario_mod": self.id_usuario_mod
        }