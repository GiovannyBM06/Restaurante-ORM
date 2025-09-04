from sqlalchemy import column,ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base 
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from Comida import Comida, ComidaBase

class Postre(Comida):    
    __tablename__ = 'Postre'
    id = column(Integer, ForeignKey(Comida.id), primary_key=True)
    sabor = column(String(50), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "postre",}  
    
def __repr__(self):
    return f"Postre(id={self.id}, nombre={self.nombre}, precio={self.precio}, sabor={self.sabor})"      

def to_dict(self):
    base_dict = super().to_dict()
    base_dict.update({
        "sabor": self.sabor
    })
    return base_dict

class PostreBase(ComidaBase):        
    sabor: str = Field(min_length=5, max_length=50, description="Sabor del postre")

    @validator('sabor')
    def validar_sabor(cls, value):
        if not value.strip():
            raise ValueError("El sabor no puede estar vacío")
        return value.title()