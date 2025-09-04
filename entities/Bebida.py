from sqlalchemy import column,ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base 
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from Comida import Comida, ComidaBase

class Bebida(Comida):
    __tablename__ = 'Bebida'
    id = column(Integer, ForeignKey(Comida.id), primary_key=True)
    tamaño = column(float, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "bebida",}
    
def __repr__(self):
    return f"Bebida(id={self.id}, nombre={self.nombre}, precio={self.precio}, tamaño={self.tamaño})"    

def to_dict(self):   
    base_dict = super().to_dict()
    base_dict.update({
        "tamaño": self.tamaño
    })
    return base_dict

class BebidaBase(ComidaBase):
    tamaño: float = Field(gt=0, description="Tamaño de la bebida en litros")

    @validator('tamaño')
    def validar_tamaño(cls, value):
        if value <= 0:
            raise ValueError("El tamaño debe ser mayor que cero")
        return value
    
    