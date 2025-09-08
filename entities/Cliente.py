from sqlalchemy import column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'Cliente'
    cc = column(Integer, primary_key=True)
    nombre = column(String(20), nullable=False)
    apellido = column(String(20), nullable=False)
    Email = column(String(50), nullable=False, unique=True)
    telefono = column(String(15), nullable=False)
    fecha_registro = column(Date, nullable=False, default=datetime.now)
    fecha_actualizacion = column(Date,default=datetime.now, onupdate=datetime.now)
    id_usuario = column(Integer, ForeignKey('Usuario.id'), nullable=False)

    Reserva = relationship("Reserva", back_populates="Cliente")

    def __repr__(self):
        return f"Cliente(cc={self.cc}, nombre='{self.nombre}', apellido='{self.apellido}', Email='{self.Email}', telefono='{self.telefono}')"
    
    def to_dict(self):
        return {
            "cc": self.cc,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "Email": self.Email,
            "telefono": self.telefono,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion if self.fecha_actualizacion else None,
            "id_usuario": self.id_usuario
        }