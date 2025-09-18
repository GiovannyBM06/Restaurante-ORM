from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from database.config import Base

class Reserva(Base):
    __tablename__ = 'reserva'
    CC_cliente = Column(Integer, ForeignKey('cliente.cc'), primary_key=True, nullable=False)
    Numero_mesa = Column(Integer, ForeignKey('mesa.numero'), primary_key=True, nullable=False)
    cantidad_personas = Column(Integer, nullable=False)
    fecha_Hora = Column(DateTime, nullable=False)
    Estado = Column(Boolean, nullable=False)
    fecha_registro = Column(Date, nullable=False, default=datetime.now)
    fecha_actualizacion = Column(Date, default= datetime.now, onupdate=datetime.now)
    id_usuario = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    id_usuario_mod = Column(Integer, ForeignKey('usuario.id'))

    cliente = relationship("Cliente", back_populates="reservas")
    mesa = relationship("Mesa", back_populates="reservas")

    usuario = relationship("Usuario", back_populates="reservas", foreign_keys=[id_usuario])
    usuario_mod = relationship("Usuario", foreign_keys=[id_usuario_mod], overlaps="usuario,reservas")

    def __repr__(self):
        return f"Reserva(cantidad_personas={self.cantidad_personas}, fecha_Hora='{self.fecha_Hora}', CC_cliente={self.CC_cliente}, Numero_mesa={self.Numero_mesa})"
    def to_dict(self):
        return {
            "CC_cliente": self.CC_cliente,
            "Numero_mesa": self.Numero_mesa,
            "cantidad_personas": self.cantidad_personas,
            "fecha_Hora": self.fecha_Hora,
            "Estado": self.Estado,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion if self.fecha_actualizacion else None,
            "id_usuario": self.id_usuario,
            "id_usuario_mod": self.id_usuario_mod
        }