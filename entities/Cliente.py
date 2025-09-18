from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from database.config import Base

class Cliente(Base):
    __tablename__ = 'cliente'
    cc = Column(Integer, primary_key=True)
    nombre = Column(String(20), nullable=False)
    apellido = Column(String(20), nullable=False)
    Email = Column(String(50), nullable=False, unique=True)
    telefono = Column(String(15), nullable=False)
    fecha_registro = Column(Date, nullable=False, default=datetime.now)
    fecha_actualizacion = Column(Date,default=datetime.now, onupdate=datetime.now)
    id_usuario = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    id_usuario_mod = Column(Integer, ForeignKey('usuario.id'))

    reservas = relationship("Reserva", back_populates="cliente")

    usuario = relationship("Usuario", back_populates="clientes", foreign_keys=[id_usuario])
    usuario_mod = relationship("Usuario", foreign_keys=[id_usuario_mod], overlaps="usuario,clientes")
    
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
            "id_usuario": self.id_usuario,
            "id_usuario_mod": self.id_usuario_mod
        }