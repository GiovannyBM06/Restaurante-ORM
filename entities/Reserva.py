from sqlalchemy import column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()
class Reserva(Base):
    __tablename__ = 'Reserva'
    cantidad_personas = column(Integer, nullable=False)
    fecha_hora = column(Date, nullable=False)
    id_cliente = column(Integer, ForeignKey('Cliente.id'), nullable=False)
    id_mesa = column(Integer, ForeignKey('Mesa.numero'), nullable=False)
    id_orden = column(Integer, ForeignKey('Orden.num_orden'), nullable=True)
    fecha_registro = column(Date, nullable=False, default=datetime.now)
    fecha_actualizacion = column(Date, default= datetime.now, onupdate=datetime.now)
    id_usuario = column(Integer, ForeignKey('Usuario.id'), nullable=False)

    Cliente = relationship("Cliente", back_populates="Reserva")
    Mesa = relationship("Mesa", back_populates="Reserva")
    Orden = relationship("Orden", back_populates="Reserva")

    def __repr__(self):
        return f"Reserva(cantidad_personas={self.cantidad_personas}, fecha_hora='{self.fecha_hora}', id_cliente={self.id_cliente}, id_mesa={self.id_mesa}, id_orden={self.id_orden})"
    
    def to_dict(self):
        return {
            "cantidad_personas": self.cantidad_personas,
            "fecha_hora": self.fecha_hora,
            "id_cliente": self.id_cliente,
            "id_mesa": self.id_mesa,
            "id_oreden": self.id_oreden if self.id_oreden else None,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion if self.fecha_actualizacion else None,
            "id_usuario": self.id_usuario
        }