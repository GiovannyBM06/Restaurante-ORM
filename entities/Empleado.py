from sqlalchemy import column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class Empleado(Base):
    __tablename__ = 'Empleado'
    id = column(Integer, primary_key=True, autoincrement=True)
    nombre = column(String(20), nullable=False)
    apellido = column(String(20), nullable=False)
    rol = column(String(20), nullable=False)
    salario = column(Integer, nullable=False)
    fecha_registro = column(Date, nullable=False, default = datetime.now)
    fecha_actualizacion = column(Date, default= datetime.now, onupdate=datetime.now) 
    id_usuario = column(Integer, ForeignKey('Usuario.id'), nullable=False)
    id_usuario_mod = column(Integer, ForeignKey('Usuario.id'))

    Orden = relationship("Orden", back_populates="Empleado")
    Usuario = relationship("Usuario", back_populates="Empleado")

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
