from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from database.config import Base

class Empleado(Base):
    __tablename__ = 'empleado'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(20), nullable=False)
    apellido = Column(String(20), nullable=False)
    rol = Column(String(20), nullable=False)
    salario = Column(Integer, nullable=False)
    fecha_registro = Column(Date, nullable=False, default = datetime.now)
    fecha_actualizacion = Column(Date, default= datetime.now, onupdate=datetime.now) 
    id_usuario = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    id_usuario_mod = Column(Integer, ForeignKey('usuario.id'))

    ordenes = relationship("Orden", back_populates="empleado")

    usuario = relationship("Usuario", back_populates="empleados", foreign_keys=[id_usuario])
    usuario_mod = relationship("Usuario", foreign_keys=[id_usuario_mod], overlaps="usuario,empleados")

    def __repr__(self):
        return f"Empleado(id={self.id}, nombre='{self.nombre}', apellido='{self.apellido}', rol='{self.rol}', salario={self.salario})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "rol": self.rol,
            "salario": self.salario,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion if self.fecha_actualizacion else None,
            "id_usuario": self.id_usuario,
            "id_usuario_mod": self.id_usuario_mod
        }
