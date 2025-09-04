from sqlalchemy import column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base 
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()
class Comida(Base):
    __tablename__ = 'Comida'

    id = column( Integer, primary_key=True, autoincrement=True)
    nombre = column (String(20), nullable=False)
    precio = column (Integer, nullable=False)
    fecha_registro = column (Date, nullable=False)
    fecha_actualizacion = column (Date, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "employee",
        "polymorphic_on": "type",
    }


def __repr__(self):
    return f"Comida(id={self.id}, nombre={self.nombre}, precio={self.precio})"

def to_dict(self):
    return {
        "id": self.id,
        "nombre": self.nombre,
        "precio": self.precio,
        "fecha_registro": self.fecha_registro.isoformat() if self.fecha_registro else None,
        "fecha_actualizacion": self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
    }

class ComidaBase (BaseModel):
    nombre: str = Field(min_length=5, max_length=20,description="Nombre de la comida")
    precio:float = Field(gt=0, description="Precio de la comida")



    @validator('nombre')
    def validar_nombre(cls, value):
        if not value.strip():
            raise ValueError("El nombre no puede estar vacío")
        return value.title()

    @validator('precio')
    def validar_precio(cls, value):
        if value <= 0:
            raise ValueError("El precio debe ser mayor que cero")
        return value