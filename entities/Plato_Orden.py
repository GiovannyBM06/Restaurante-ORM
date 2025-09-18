from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from database.config import Base

class Plato_Orden(Base):
    __tablename__ = 'plato_orden'

    numero_orden = Column(Integer, ForeignKey('orden.numero'), primary_key=True, nullable=False)
    id_plato = Column(Integer, ForeignKey('plato.id'), primary_key=True, nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha_registro = Column(Date, nullable=False, default=datetime.now)
    fecha_actualizacion = Column(Date, default= datetime.now, onupdate=datetime.now)
    id_usuario = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    id_usuario_mod = Column(Integer, ForeignKey('usuario.id'))

    orden = relationship("Orden", back_populates="platos_orden")
    plato = relationship("Plato", back_populates="platos_orden")

    usuario = relationship("Usuario", back_populates="platos_orden", foreign_keys=[id_usuario])
    usuario_mod = relationship("Usuario", foreign_keys=[id_usuario_mod], overlaps="usuario,platos_orden")


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