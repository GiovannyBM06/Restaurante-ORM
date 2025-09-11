from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'Cliente'
    cc = Column(Integer, primary_key=True)
    nombre = Column(String(20), nullable=False)
    apellido = Column(String(20), nullable=False)
    Email = Column(String(50), nullable=False, unique=True)
    telefono = Column(String(15), nullable=False)
    fecha_registro = Column(Date, nullable=False, default=datetime.now)
    fecha_actualizacion = Column(Date,default=datetime.now, onupdate=datetime.now)
    id_usuario = Column(Integer, ForeignKey('Usuario.id'), nullable=False)
    id_usuario_mod = Column(Integer, ForeignKey('Usuario.id'))

    Reserva = relationship("Reserva", back_populates="Cliente")
    Usuario = relationship("Usuario", back_populates="Cliente")

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
    
class ClienteModel(BaseModel):
    cc: int = Field(..., gt=0, description="Cédula del cliente")
    nombre: str = Field(..., min_length=1, max_length=20, description="Nombre del cliente")
    apellido: str = Field(..., min_length=1, max_length=20, description="Apellido del cliente")
    Email: EmailStr = Field(..., description="Email del cliente")
    telefono: str = Field(..., min_length=7, max_length=15, description="Teléfono del cliente")
    id_usuario: int = Field(..., gt=0, description="ID del usuario que crea el cliente")
    id_usuario_mod: Optional[int] = Field(None, gt=0, description="ID del usuario que modifica el cliente")

    @validator('nombre', 'apellido', 'telefono')
    def validar_textos(cls, v, field):
        if not v or len(v.strip()) == 0:
            raise ValueError(f"El campo {field.name} no puede estar vacío")
        return v
    def validar_cedula (cls,v):
        if v is not None and not v.isdigit():
            raise ValueError("La cedula debe contener solo numeros")
        return v
    @validator( 'nombre', 'apellido')
    def validar_nombre_apellido(cls, v):
        if not v.strip():
            raise ValueError('El nombre y apellido no deben estar vacíos o solo contener espacios')
        return v
    @validator('Email')
    def validate_email(cls, v):
        if not v or '@' not in v:
            raise ValueError('El email no es válido')
        return v
    @validator('telefono')
    def validate_telefono(cls, v):
        if not v.isdigit():
            raise ValueError('El telefono debe contener solo numeros')
        return v

class ClienteCreate(ClienteModel):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=20)
    apellido: Optional[str] = Field(None, min_length=1, max_length=20)
    Email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, min_length=7, max_length=15)
    id_usuario_mod: int = Field(..., gt=0)

    @validator('cc')
    def validar_cedula (cls,v):
        if v is not None and not v.isdigit():
            raise ValueError("La cedula debe contener solo numeros")
        return v
    @validator('nombre', 'apellido')
    def validar_nombre_apellido(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El nombre y apellido no deben estar vacíos o solo contener espacios')
        return v
    @validator('Email')
    def validar_email(cls, v):
        if v is not None and ('@' not in v):
            raise ValueError('El email no es válido')
        return v
    @validator('telefono')
    def validar_telefono(cls, v):
        if v is not None and not v.isdigit():
            raise ValueError('El telefono debe contener solo numeros')
        return v

class ClienteResponse(ClienteModel):
    cc:int
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None
    id_usuario_mod: Optional[int] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
            }
'''      
class ClienteConRelaciones(ClienteResponse):
    Usuario: Optional['UsuarioResponse'] = None

    class Config:
        from_attributes = True
'''
class ClienteListResponse(BaseModel):
    clientes: List[ClienteResponse]
    total: int

    class Config:
        from_attributes = True
