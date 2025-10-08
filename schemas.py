from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

"""Modelo base para la entidad Usuario"""
class UsuarioBase(BaseModel):
    nombre: str 
    apellido: str 
    email: EmailStr
    contraseña: str

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    contraseña: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    nombre_usuario: str
    contraseña: str

class CambioContraseña(BaseModel):
    contraseña_actual: str
    nueva_contraseña: str

class loginResponse(BaseModel):
    clave: str
    nombre_usuario: UsuarioResponse

"""Modelo base para la entidad Categoria"""

class CategoriaBase(BaseModel):
    nombre: str
    descripcion: str 

class CategoriaCreate(CategoriaBase):
    pass 

class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

class CategoriaResponse(CategoriaBase):
    id: UUID
    fecha_creacion :datetime
    fecha_actulizacion : Optional[datetime] = None

"""Modelo base para la entidad Cliente"""

class ClienteBase (BaseModel):
    nombre:str
    apellido:str
    email: EmailStr
    telefono: str

class ClienteCreate(ClienteBase):
    pass 

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None

class ClienteResponse(BaseModel):
    id:UUID
    fecha_creación: datetime
    fecha_actualización: Optional[datetime] = None
    class Config:
        from_attributes = True
 
"""Modelo base para la entidad Empleado"""
class EmpleadoBase(BaseModel):
    nombre: str
    apellido: str
    rol: str
    salario: int 

class EmpleadoCreate(EmpleadoBase):
    pass

class EmpleadoUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    rol: Optional[str] = None
    salario: Optional[int] = None

class EmpleadoResponse(EmpleadoBase):
    id: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    class Config:
        from_attributes = True

"""Modelo base para la entidad Factura"""
class FacturaBase(BaseModel):
    total: float
    metodo_pago: str

class FacturaCreate(FacturaBase):
    pass

class FacturaUpdate(BaseModel):
    total: Optional[float] = None
    metodo_pago:str

class FacturaResponse(FacturaBase):
    id: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    class Config:
        from_attributes = True

"""Modelo base para la entidad Mesa"""
class MesaBase(BaseModel):
    capacidad: int

class MesaCreate(MesaBase):
    pass

class MesaUpdate(BaseModel):
    capacidad: Optional[int] = None

class MesaResponse(MesaBase):
    id: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    class Config:
        from_attributes = True

"""Modelo base para la entidad Orden"""
class OrdenBase(BaseModel):
    estado: str 

class OrdenCreate(OrdenBase):
    pass

class OrdenUpdate(BaseModel):
    estado: Optional[str] = None

class OrdenResponse(OrdenBase):
    id: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    class Config:
        from_attributes = True

"""Modelo base para la entidad Plato_Orden"""
class PlatoOrdenBase(BaseModel):
    orden_id: UUID
    plato_id: UUID

class PlatoOrdenCreate(PlatoOrdenBase):
    pass

class PlatoOrdenUpdate(BaseModel):
    orden_id: Optional[UUID] = None
    plato_id: Optional[UUID] = None

class PlatoOrdenResponse(PlatoOrdenBase):
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    class Config:
        from_attributes = True

"""Modelo base para la entidad Plato"""
class PlatoBase(BaseModel):
    nombre: str
    precio_unidad: int
    descripcion: str

class PlatoCreate(PlatoBase):
    pass

class PlatoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    descripcion: Optional[str] = None

class PlatoResponse(PlatoBase):
    id: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    class Config:
        from_attributes = True

"""Modelo base para la entidad Reserva"""
class ReservaBase(BaseModel):
    cliente_id: UUID
    mesa_id: UUID
    cantidad_personas: int
    fecha_hora: datetime
    estado: str

class ReservaCreate(ReservaBase):
    pass

class ReservaUpdate(BaseModel):
    cliente_id: Optional[UUID] = None
    mesa_id: Optional[UUID] = None
    cantidad_personas: Optional[int] = None
    fecha_hora: Optional[datetime] = None
    estado: Optional[str] = None

class ReservaResponse(ReservaBase):
    id: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    class Config:
        from_attributes = True

"""Modelos de respuesta para la API"""
class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool = True
    datos: Optional[dict] = None

class RespuestaError(BaseModel):
    mensaje: str
    exito: bool = False
    error: str
    codigo: int
    