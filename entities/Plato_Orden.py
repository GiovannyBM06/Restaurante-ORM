from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class Plato_Orden(Base):
    __tablename__ = 'Plato_Orden'

    numero_orden = Column(Integer, ForeignKey('Orden.numero'),primary_key=True, nullable=False)
    id_plato = Column(Integer, ForeignKey('Plato.id'),primary_key=True, nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha_registro = Column(Date, nullable=False, default=datetime.now)
    fecha_actualizacion = Column(Date, default= datetime.now, onupdate=datetime.now)
    id_usuario = Column(Integer, ForeignKey('Usuario.id'), nullable=False)
    id_usuario_mod = Column(Integer, ForeignKey('Usuario.id'))

    Orden = relationship("Orden", back_populates="Plato_Orden")
    Plato = relationship("Plato", back_populates="Plato_Orden")
    Usuario = relationship("Usuario", back_populates="Plato_Orden")

    def __repr__(self):
        return f"Plato_Orden(num_orden={self.numero_orden}, id_plato={self.id_plato}, cantidad={self.cantidad})"
    
    def to_dict(self): 
        return {
            "numero_orden": self.numero_orden,
            "id_plato": self.id_plato,
            "cantidad": self.cantidad,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion if self.fecha_actualizacion else None,
            "id_usuario": self.id_usuario,
            "id_usuario_mod": self.id_usuario_mod   
        }


class PlatoOrdenBase(BaseModel):
    numero_orden: int = Field(..., gt=0, description="Número de la orden")
    id_plato: int = Field(..., gt=0, description="ID del plato")
    cantidad: int = Field(..., gt=0, description="Cantidad de platos")
    id_usuario: int = Field(..., gt=0, description="ID del usuario que crea el registro")

    @validator('cantidad', 'numero_orden', 'id_plato', 'id_usuario')
    def validar_positivos(cls, v):
        if v is not None and v <= 0:
            raise ValueError("El valor debe ser mayor que 0")
        return v

class PlatoOrdenCreate(PlatoOrdenBase):
    pass

class PlatoOrdenUpdate(PlatoOrdenBase):
    id_usuario_mod: int = Field(..., gt=0, description="ID del usuario que modifica el registro")

    @validator('id_usuario_mod')
    def validar_id_usuario_mod(cls, v):
        if v is not None and v <= 0:
            raise ValueError("El id_usuario_mod debe ser mayor que 0")
        return v

class PlatoOrdenResponse(PlatoOrdenBase):
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None
    id_usuario_mod: Optional[int] = None
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
'''
class PlatoOrdenConRelaciones(PlatoOrdenResponse):
    from typing import Any
    Orden: Optional['OrdenResponse'] = None
    Plato: Optional['PlatoResponse'] = None
    Usuario: Optional['UsuarioResponse'] = None
    class Config:
        from_attributes = True
'''
class PlatoOrdenListResponse(BaseModel):
    Plato_Ordenes: List[PlatoOrdenResponse]

    class Config:
        from_attributes = True