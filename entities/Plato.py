from sqlalchemy import column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class Plato(Base):
    __tablename__ = 'Plato'

    id = column(Integer, primary_key=True, autoincrement=True)
    nombre = column(String(20), nullable=False)
    precio_unidad = column(Integer, nullable=False)
    descripcion = column(String(100), nullable=True)
    id_categoria = column(Integer, ForeignKey('Categoria.id'), nullable=False)
    fecha_registro = column(Date, nullable=False, default= datetime.now)
    fecha_actualizacion = column(Date, default= datetime.now, onupdate=datetime.now)
    id_usuario = column(Integer, ForeignKey('Usuario.id'), nullable=False)
    id_usuario_mod = column(Integer, ForeignKey('Usuario.id'))

    Categoria = relationship("Categoria", back_populates="platos")
    Plato_Orden = relationship("Plato_Orden", back_populates="Plato")
    Usuario = relationship("Usuario", back_populates="Plato")

    def __repr__(self):
        return f"Plato(id={self.id}, nombre='{self.nombre}', precio={self.precio_unidad}, descripcion='{self.descripcion}', id_categoria={self.id_categoria})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio_unidad,
            "descripcion": self.descripcion,
            "id_categoria": self.id_categoria,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion if self.fecha_actualizacion else None,
            "id_usuario": self.id_usuario,
            "id_usuario_mod": self.id_usuario_mod   
        }


class PlatoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=20, description="Nombre del plato")
    precio_unidad: int = Field(..., gt=0, description="Precio unitario del plato")
    descripcion: Optional[str] = Field(None, max_length=100, description="Descripción del plato")
    id_categoria: int = Field(..., gt=0, description="ID de la categoría")
    id_usuario: int = Field(..., gt=0, description="ID del usuario que crea el plato")

    @validator('nombre')
    def validar_nombre(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("El nombre no puede estar vacío")
        return v

    @validator('precio_unidad', 'id_categoria', 'id_usuario')
    def validar_positivos(cls, v):
        if v is not None and v <= 0:
            raise ValueError("El valor debe ser mayor que 0")
        return v

class PlatoCreate(PlatoBase):
    pass

class PlatoUpdate(PlatoBase):
    id_usuario_mod: int = Field(..., gt=0, description="ID del usuario que modifica el plato")

    @validator('id_usuario_mod')
    def validar_id_usuario_mod(cls, v):
        if v is not None and v <= 0:
            raise ValueError("El id_usuario_mod debe ser mayor que 0")
        return v

class PlatoResponse(PlatoBase):
    id: int
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None
    id_usuario_mod: Optional[int] = None
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
'''
class PlatoConRelaciones(PlatoResponse):

    Categoria: Optional['CategoriaResponse'] = None
    Plato_Orden: Optional['PlatoOrdenResponse'] = None
    Usuario: Optional["UsuarioResponse"] = None
    class Config:
        from_attributes = True
'''
class PlatoListResponse(BaseModel):
    Platos: List[PlatoResponse]

    class Config:
        from_attributes = True