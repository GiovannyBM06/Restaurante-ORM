from sqlalchemy import column, Integer,Float, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class Plato_Ingrediente(Base):
    __tablename__ = 'Plato_Ingrediente'

    id = column(Integer, primary_key=True, autoincrement=True)
    id_comida = column(Integer, ForeignKey('Comida.id'), nullable=False)
    id_ingrediente = column(Integer, ForeignKey('Ingrediente.id'), nullable=False)
    cantidad_porcion = column(Float, nullable=False)
    fecha_registro = column(Date, nullable=False,default= datetime.now)
    fecha_actualizacion = column(Date, default= datetime.now, onupdate=datetime.now)
    id_usuario = column(Integer, ForeignKey('Usuario.id'), nullable=False)

    Plato = relationship("Plato", back_populates="Plato_Ingrediente")
    Ingrediente = relationship("Ingrediente", back_populates="Plato_Ingrediente")   

    def __repr__(self):
        return f"Plato_Ingrediente(id={self.id}, id_comida={self.id_comida}, id_ingrediente={self.id_ingrediente}, cantidad_porcion={self.cantidad_porcion})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "id_comida": self.id_comida,
            "id_ingrediente": self.id_ingrediente,
            "cantidad_porcion": self.cantidad_porcion,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion if self.fecha_actualizacion else None,
            "id_usuario": self.id_usuario
        }