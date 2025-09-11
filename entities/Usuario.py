from sqlalchemy import column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class Usuario(Base):
    __tablename__= 'Usuario'
    nombre = column(String(20), nullable=False)
    apellido = column(String(20), nullable=False)
    email = column(String(40), nullable=False, unique=True)
    contraseña = column(String(20), nullable=False)

    Plato = relationship("Plato", back_populates="Usuario")
    Categoria = relationship("Categoria", back_populates="Usuario")
    Empleado = relationship("Empleado", back_populates="Usuario")
    Cliente = relationship("Cliente", back_populates="Usuario")
    Reserva = relationship("Reserva", back_populates="Usuario")
    Factura = relationship("Factura", back_populates="Usuario")
    Orden = relationship("Orden", back_populates="Usuario")
    Mesa = relationship("Mesa", back_populates="Usuario")
    Plato_Orden = relationship("Plato_Orden", back_populates="Usuario")

    def __repr__(self):
        return f"Usuario(nombre='{self.nombre}', apellido='{self.apellido}', email='{self.email}')"
    
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email
        }
