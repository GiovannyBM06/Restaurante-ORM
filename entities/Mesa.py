from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class Mesa(Base):
    __tablename__ = 'Mesa'
    numero = Column(Integer, primary_key=True, autoincrement=True)
    capacidad = Column(Integer, nullable=False)
    fecha_registro = Column(Date, nullable=False, default = datetime.now)  
    fecha_actualizacion = Column(Date, default= datetime.now, onupdate=datetime.now)
    id_usuario = Column(Integer, ForeignKey('Usuario.id'), nullable=False)
    id_usuario_mod = Column(Integer, ForeignKey('Usuario.id'))

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

class MesaBase(BaseModel):
    capacidad: int = Field(..., gt=0, description="Capacidad máxima de personas que pueden estar en una mesa")
    id_usuario: int = Field(..., gt=0, description="ID del usuario que crea la mesa")

    @validator('capacidad', 'id_usuario')
    def validar_positivos(cls, v):
        if v is not None and v <= 0:
            raise ValueError("El valor debe ser mayor que 0")
        return v
class MesaCreate(MesaBase):
    pass

class MesaUpdate(MesaBase):
    capacidad:Integer = Field(...,gt=0, description="Capacidad maxima de persona que pueden estar en una mesa")
    id_usuario_mod: Integer =Field(...,gt=0, description="ID del usuario que crea la mesa")

    @validator ('capacidad')
    def validar_capacidad(cls, v):
        if v is not None and v <= 0:
            raise ValueError ("La capacidad debe ser mayor que 0")
class MesaResponse(MesaBase):
    id:int
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None
    id_usuario_mod: Optional[int] = None
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
            }
'''
class MesaConRelaciones(MesaResponse):
    Usuario: Optional['UsuarioResponse'] = None
    class Config:
        from_attributes = True
'''
class MesaListResponse(BaseModel):
    Mesas: List[MesaResponse]

    class Config:
        from_attributes = True 