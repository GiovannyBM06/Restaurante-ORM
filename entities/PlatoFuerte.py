from sqlalchemy import column,ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base 
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from Comida import Comida, ComidaBase

class PlatoFuerte(Comida):    
    __tablename__ = 'PlatoFuerte'
    id = column(Integer, ForeignKey(Comida.id), primary_key=True)
    ingredientes = column(String(100), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "plato_fuerte",}
    
def __repr__(self):
    return f"PlatoFuerte(id={self.id}, nombre={self.nombre}, precio={self.precio}, ingredientes={self.ingredientes})"

def to_dict(self):
    base_dict = super().to_dict()
    base_dict.update({
        "ingredientes": self.ingredientes
    })
    return base_dict    

class PlatoFuerteBase(ComidaBase):
    ingredientes: str = Field(min_length=5, max_length=100, description="Ingredientes del plato fuerte")

    @validator('ingredientes')
    def validar_ingredientes(cls, value):
        if not value.strip():
            raise ValueError("No puede haber un plato fuerte sin ingredientes")
        return value.title()