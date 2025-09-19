from sqlalchemy import column, Integer, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class Plato_Orden(Base):
    __tablename__ = 'Plato_Orden'

    numero_orden = column(Integer, ForeignKey('Orden.numero'), nullable=False)
    id_plato = column(Integer, ForeignKey('Plato.id'), nullable=False)
    cantidad = column(Integer, nullable=False)
    fecha_registro = column(Date, nullable=False, default=datetime.now)
    fecha_actualizacion = column(Date, default= datetime.now, onupdate=datetime.now)
    id_usuario = column(Integer, ForeignKey('Usuario.id'), nullable=False)
    id_usuario_mod = column(Integer, ForeignKey('Usuario.id'))

    Orden = relationship("Orden", back_populates="Plato_Orden")
    Plato = relationship("Plato", back_populates="Plato_Orden")
    Usuario = relationship("Usuario", back_populates="Plato_Orden")

    def __repr__(self):
        return f"Plato_Orden(num_orden={self.numero_orden}, id_plato={self.id_plato}, cantidad={self.cantidad})"
    
    def to_dict(self): 
        return {
            "numero_orden": self.numero_orden,
            "id_plato": self.id_plato,
            "cantidad": self.cantidad,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion if self.fecha_actualizacion else None,
            "id_usuario": self.id_usuario,
            "id_usuario_mod": self.id_usuario_mod   
        }