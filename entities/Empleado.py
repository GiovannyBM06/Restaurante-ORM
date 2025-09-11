from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class Empleado(Base):
    __tablename__ = 'Empleado'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(20), nullable=False)
    apellido = Column(String(20), nullable=False)
    rol = Column(String(20), nullable=False)
    salario = Column(Integer, nullable=False)
    fecha_registro = Column(Date, nullable=False, default = datetime.now)
    fecha_actualizacion = Column(Date, default= datetime.now, onupdate=datetime.now) 
    id_usuario = Column(Integer, ForeignKey('Usuario.id'), nullable=False)
    id_usuario_mod = Column(Integer, ForeignKey('Usuario.id'))

    Orden = relationship("Orden", back_populates="Empleado")
    Usuario = relationship("Usuario", back_populates="Empleado")

    def __repr__(self):
        return f"Empleado(id={self.id}, nombre='{self.nombre}', apellido='{self.apellido}', rol='{self.rol}', salario={self.salario})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "rol": self.rol,
            "salario": self.salario,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion if self.fecha_actualizacion else None,
            "id_usuario": self.id_usuario,
            "id_usuario_mod": self.id_usuario_mod
        }

class EmpleadoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=20, description="Nombre del empleado")
    apellido: str = Field(..., min_length=1, max_length=20, description="Apellido del empleado")
    rol: str = Field(..., min_length=1, max_length=20, description="Rol del empleado")
    salario: int = Field(..., gt=0, description="Salario del empleado")
    id_usuario: int = Field(..., gt=0, description="ID del usuario que crea el empleado")

    @validator('nombre', 'apellido', 'rol')
    def validar_texto(cls, v, field):
        if not v or len(v.strip()) == 0:
            raise ValueError(f"El campo {field.name} no puede estar vacío")
        return v.strip()
    
    @validator('salario')
    def validar_salario(cls, v):
        if v <= 0:
            raise ValueError('El salario debe ser un número positivo')
        return v
    
class EmpleadoCreate(EmpleadoBase):
    pass

class EmpleadoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=20, description="Nombre del empleado")
    apellido: Optional[str] = Field(None, max_length=20, description="Apellido del empleado")
    rol: Optional[str] = Field(None, max_length=20, description="Rol del empleado")
    salario: Optional[int] = Field(None, gt=0, description="Salario del empleado")
    id_usuario_mod: int = Field(..., gt=0, description="ID del usuario que modifica el empleado")

    @validator('nombre', 'apellido', 'rol')
    def validar_texto(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El campo no puede estar vacío o solo contener espacios')
        return v.strip() if v is not None else v
    
    @validator('salario')
    def validar_salario(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El salario debe ser un número positivo')
        return v

class EmpleadoResponse(EmpleadoBase):
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
class EmpleadoConRelaciones(EmpleadoResponse):
    Usuario: Optional['UsuarioResponse'] = None

    class Config:
        from_attributes = True
'''       
class EmpleadoListResponse(BaseModel):
    Empleados: List[EmpleadoResponse]

    class Config:
        from_attributes = True        