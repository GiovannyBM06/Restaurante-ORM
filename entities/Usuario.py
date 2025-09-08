from sqlalchemy import column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
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


    def __repr__(self):
        return f"Usuario(nombre='{self.nombre}', apellido='{self.apellido}', email='{self.email}')"
    
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email
        }
