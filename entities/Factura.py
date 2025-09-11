from sqlalchemy import column, Integer,Float, String, Date, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class Factuta(Base):
    __tablename__ = 'Factura'
    id = column(Integer, primary_key=True, autoincrement=True)
    total = column(Float, nullable=False)
    metodo_pago = column(String(20), nullable=False)
    numero_orden = column(Integer, ForeignKey('Orden.numero'), nullable=False)
    fecha_registro = column(Date, nullable=False, default = datetime.now)
    fecha_actualizacion = column(Date, default= datetime.now, onupdate=datetime.now)
    id_usuario = column(Integer, ForeignKey('Usuario.id'), nullable=False)
    id_usuario_mod = column(Integer, ForeignKey('Usuario.id'))

    Orden = relationship("Orden", back_populates="Factura")
    Usuario= relationship("Usuario", back_populates="Factura")

    def __repr__(self):
        return f"Factura(id={self.id}, total={self.total}, metodo_pago='{self.metodo_pago}', id_orden={self.numero_orden})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "total": self.total,
            "metodo_pago": self.metodo_pago,
            "numero_orden": self.numero_orden,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion if self.fecha_actualizacion else None,
            "id_usuario": self.id_usuario,
            "id_usuario_mod": self.id_usuario_mod
        }

class FacturaBase(BaseModel):
    total: float = Field(..., gt=0, description="Total de la factura")
    metodo_pago: str = Field(..., max_length=20, description="Método de pago de la factura")
    numero_orden: int = Field(..., gt=0, description="Número de la orden asociada a la factura")
    id_usuario: int = Field(..., gt=0, description="ID del usuario que crea la factura")

    @validator('metodo_pago')
    def validar_metodo_pago(cls, v):
        if not v.strip():
            raise ValueError('El método de pago no puede estar vacío o solo contener espacios')
        return v.strip()
    
    @validator('total')
    def validar_total(cls, v):
        if v <= 0:
            raise ValueError('El total debe ser un número positivo')
        return v
    
class FacturaCreate(FacturaBase):
    pass

class FacturaUpdate(BaseModel):
    total: Optional[float] = Field(None, gt=0, description="Total de la factura")
    metodo_pago: Optional[str] = Field(None, max_length=20, description="Método de pago de la factura")
    id_usuario_mod: int = Field(..., gt=0, description="ID del usuario que modifica la factura")

    @validator('metodo_pago')
    def validar_metodo_pago(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El método de pago no puede estar vacío o solo contener espacios')
        return v.strip() if v is not None else v
    
    @validator('total')
    def validar_total(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El total debe ser un número positivo')
        return v
    
class FacturaResponse(FacturaBase):
    id: int
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None
    id_usuario_mod: Optional[int] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()   
            }

class FacturaConRelaciones(FacturaResponse):
    usuario: Optional ['UsuarioResponse']
    orden: Optional ['OrdenResponse']

    class config:
        from_attributes= True

class FacturaListResponse (BaseModel):
    Empleados: list [FacturaResponse]
    total:int

