from sqlalchemy import column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class Mesa(Base):
    __tablename__ = 'Mesa'
    numero = column(Integer, primary_key=True, autoincrement=True)
    capacidad = column(Integer, nullable=False)
    fecha_registro = column(Date, nullable=False, default = datetime.now)  
    fecha_actualizacion = column(Date, default= datetime.now, onupdate=datetime.now)
    id_usuario = column(Integer, ForeignKey('Usuario.id'), nullable=False)
    id_usuario_mod = column(Integer, ForeignKey('Usuario.id'))

    Reserva = relationship("Reserva", back_populates= "Mesa")
    id_usuario = relationship("Usuario", back_populates="Mesa")

    def __repr__(self):
        return f"Mesa(numero={self.numero}, capacidad={self.capacidad}, estado='{self.estado}')"
    
    def to_dict(self):  
        return {
            "numero": self.numero,
            "capacidad": self.capacidad,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion if self.fecha_actualizacion else None,
            "id_usuario": self.id_usuario,
            "id_usuario_mod": self.id_usuario_mod  
        }