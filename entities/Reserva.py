from sqlalchemy import column, Integer, String, Date, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()
class Reserva(Base):
    __tablename__ = 'Reserva'
    CC_cliente = column(Integer, ForeignKey('Cliente.id'), nullable=False)
    Numero_mesa = column(Integer, ForeignKey('Mesa.numero'), nullable=False)
    cantidad_personas = column(Integer, nullable=False)
    fecha_Hora = column(DateTime, nullable=False)
    Estado = column(Boolean, nullable=False)
    fecha_registro = column(Date, nullable=False, default=datetime.now)
    fecha_actualizacion = column(Date, default= datetime.now, onupdate=datetime.now)
    id_usuario = column(Integer, ForeignKey('Usuario.id'), nullable=False)
    id_usuario_mod = column(Integer, ForeignKey('Usuario.id'))

    Cliente = relationship("Cliente", back_populates="Reserva")
    Mesa = relationship("Mesa", back_populates="Reserva")
    Usuario = relationship("Usuario", back_populates="Reserva")

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