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

# Clases de validación Pydantic para Usuario
class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=20, description="Nombre del usuario")
    apellido: str = Field(..., min_length=1, max_length=20, description="Apellido del usuario")
    email: EmailStr = Field(..., description="Email del usuario")
    contraseña: str = Field(..., min_length=6, max_length=20, description="Contraseña del usuario")

    @validator('nombre', 'apellido', 'contraseña')
    def validar_campos(cls, v, field):
        if not v or len(v.strip()) == 0:
            raise ValueError(f"El campo {field.name} no puede estar vacío")
        return v

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(UsuarioBase):
    pass

class UsuarioResponse(UsuarioBase):
    class Config:
        from_attributes = True
'''class UsuarioConRelaciones(UsuarioResponse):
    Plato: Optional['PlatoResponse'] = None
    Categoria: Optional['CategoriaResponse'] = None
    Empleado: Optional['EmpleadoResponse'] = None
    Cliente: Optional['ClienteResponse'] = None
    Reserva: Optional['ReservaResponse'] = None
    Factura: Optional['FacturaResponse'] = None
    Orden: Optional['OrdenResponse'] = None
    Mesa: Optional['MesaResponse'] = None
    Plato_Orden: Optional['PlatoOrdenResponse'] = None
    class Config:
        from_attributes = True
'''
class UsuarioListResponse(BaseModel):
    Usuarios: List[UsuarioResponse]

    class Config:
        from_attributes = True
