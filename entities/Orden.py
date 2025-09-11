from sqlalchemy import column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class Orden(Base):
    __tablename__ = 'Orden'
    numero = column(Integer, primary_key=True, autoincrement=True)
    estado = column(String, nullable=False, default='Pendiente')
    numero_mesa = column(Integer, ForeignKey('Mesa.numero'), nullable=False)
    id_empleado = column(Integer, ForeignKey('Empleado.id'), nullable=False)
    fecha_registro = column(Date, nullable=False, default = datetime.now)
    fecha_actualizacion = column(Date, default= datetime.now, onupdate=datetime.now)
    id_usuario = column(Integer, ForeignKey('Usuario.id'), nullable=False)
    id_usuario_mod = column(Integer, ForeignKey('Usuario.id'))

    Mesa = relationship("Mesa", back_populates= "Orden")
    Empleado= relationship("Empleado", back_populates= "Orden")
    Factura = relationship("Factura", back_populates= "Orden")
    Plato_Orden = relationship("Plato_Orden", back_populates= "Orden")
    Usuario = relationship("Usuario", back_populates="Orden")

    def __repr__(self):
        return f"Orden(numero={self.numero}, estado='{self.estado}')"
    
    def to_dict(self):
        return {
            "numero": self.numero,
            "estado": self.estado,
            "numero_mesa": self.numero_mesa,
            "id_empleado": self.id_empleado,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion if self.fecha_actualizacion else None,
            "id_usuario": self.id_usuario,
            "id_usuario_mod": self.id_usuario_mod
        }

class OrdenBase(BaseModel):
    estado: str = Field(..., description="Estado de la orden")
    numero_mesa: int = Field(..., gt=0, description="Número de la mesa")
    id_empleado: int = Field(..., gt=0, description="ID del empleado")
    id_usuario: int = Field(..., gt=0, description="ID del usuario que crea la orden")

    @validator('estado')
    def validar_estado(cls, v):
        estados_validos = ['Pendiente', 'En Proceso', 'Completada', 'Cancelada']
        if v not in estados_validos:
            raise ValueError(f"El estado debe ser uno de: {', '.join(estados_validos)}")
        return v

    @validator('numero_mesa', 'id_empleado', 'id_usuario')
    def validar_ids(cls, v):
        if v is not None and v <= 0:
            raise ValueError("El valor debe ser mayor que 0")
        return v

class OrdenCreate(OrdenBase):
    pass

class OrdenUpdate(OrdenBase):
    id_usuario_mod: int = Field(..., gt=0, description="ID del usuario que modifica la orden")

    @validator('id_usuario_mod')
    def validar_id_usuario_mod(cls, v):
        if v is not None and v <= 0:
            raise ValueError("El id_usuario_mod debe ser mayor que 0")
        return v

class OrdenResponse(OrdenBase):
    numero: int
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None
    id_usuario_mod: Optional[int] = None
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
'''
class OrdenConRelaciones(OrdenResponse):
    usuario: Optional ['UsuarioResponse']
    mesa: Optional ['MesaResponse']
    empleado: Optional ['EmpledoResponse']
    class Config:
        from_attributes = True
'''
class OrdenListResponse(BaseModel):
    Ordenes: List[OrdenResponse]

    class Config:
        from_attributes = True
        