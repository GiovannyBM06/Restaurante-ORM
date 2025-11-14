from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

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

    class Config:
        from_attributes = True

class CambioContraseña(BaseModel):
    contraseña_actual: str
    nueva_contraseña: str

class UsuarioLogin(BaseModel):
    email: str
    contraseña: str
    


"""Modelo base para la entidad Categoria"""


from datetime import date
from uuid import UUID
from pydantic import BaseModel
from typing import Optional


class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class CategoriaCreate(CategoriaBase):
    id_usuario: UUID


class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    id_usuario_mod: Optional[UUID] = None


class CategoriaResponse(CategoriaBase):
    id: UUID
    fecha_registro: date
    fecha_actualizacion: Optional[date] = None
    id_usuario: UUID
    id_usuario_mod: Optional[UUID] = None


"""Modelo base para la entidad Cliente"""


class ClienteBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr = Field(..., alias="Email")
    telefono: str

    class Config:
        populate_by_name = True


class ClienteCreate(ClienteBase):
    id_usuario: UUID


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = Field(None, alias="Email")
    telefono: Optional[str] = None
    id_usuario_mod: Optional[UUID] = None

    class Config:
        populate_by_name = True


class ClienteResponse(ClienteBase):
    id: UUID
    fecha_registro: date
    fecha_actualizacion: Optional[date] = None
    id_usuario: UUID
    id_usuario_mod: Optional[UUID] = None

    class Config:
        from_attributes = True
        populate_by_name = True


"""Modelo base para la entidad Empleado"""


class EmpleadoBase(BaseModel):
    nombre: str
    apellido: str
    rol: str
    salario: int


class EmpleadoCreate(EmpleadoBase):
    id_usuario: UUID


class EmpleadoUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    rol: Optional[str] = None
    salario: Optional[int] = None
    id_usuario_mod: Optional[UUID] = None


class EmpleadoResponse(EmpleadoBase):
    id: UUID
    fecha_registro: date
    fecha_actualizacion: Optional[date] = None
    id_usuario: UUID
    id_usuario_mod: Optional[UUID] = None

    class Config:
        from_attributes = True


"""Modelo base para la entidad Factura"""


class FacturaBase(BaseModel):
    total: float
    metodo_pago: str
    id_orden: UUID


class FacturaCreate(FacturaBase):
    id_usuario: UUID


class FacturaUpdate(BaseModel):
    total: Optional[float] = None
    metodo_pago: Optional[str] = None
    id_usuario_mod: UUID


class FacturaResponse(FacturaBase):
    id: UUID
    fecha_registro: date
    fecha_actualizacion: Optional[date] = None
    id_usuario: UUID
    id_usuario_mod: Optional[UUID] = None

    class Config:
        from_attributes = True


"""Modelo base para la entidad Mesa"""


class MesaBase(BaseModel):
    capacidad: int


class MesaCreate(MesaBase):
    id_usuario: UUID


class MesaUpdate(BaseModel):
    capacidad: Optional[int] = None
    id_usuario_mod: Optional[UUID] = None


class MesaResponse(MesaBase):
    id: UUID
    fecha_registro: date
    fecha_actualizacion: Optional[date] = None
    id_usuario: UUID
    id_usuario_mod: Optional[UUID] = None

    class Config:
        from_attributes = True


"""Modelo base para la entidad Orden"""


class OrdenBase(BaseModel):
    estado: str
    id_mesa: UUID
    id_empleado: UUID


class OrdenCreate(OrdenBase):
    id_usuario: UUID


class OrdenUpdate(BaseModel):
    estado: Optional[str] = None
    id_mesa: Optional[UUID] = None
    id_empleado: Optional[UUID] = None
    id_usuario_mod: Optional[UUID] = None


class OrdenResponse(OrdenBase):
    id: UUID
    fecha_registro: date
    fecha_actualizacion: Optional[date] = None
    id_usuario: UUID
    id_usuario_mod: Optional[UUID] = None

    class Config:
        from_attributes = True


"""Modelo base para la entidad Plato_Orden"""


class PlatoOrdenBase(BaseModel):
    id_orden: UUID
    id_plato: UUID
    cantidad: int


class PlatoOrdenCreate(PlatoOrdenBase):
    id_usuario: UUID


class PlatoOrdenUpdate(BaseModel):
    cantidad: Optional[int] = None
    id_usuario_mod: Optional[UUID] = None


class PlatoOrdenResponse(PlatoOrdenBase):
    fecha_registro: date
    fecha_actualizacion: Optional[date] = None
    id_usuario: UUID
    id_usuario_mod: Optional[UUID] = None

    class Config:
        from_attributes = True


"""Modelo base para la entidad Plato"""


class PlatoBase(BaseModel):
    nombre: str
    precio_unidad: int
    descripcion: Optional[str] = None
    id_categoria: UUID


class PlatoCreate(PlatoBase):
    id_usuario: UUID


class PlatoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio_unidad: Optional[int] = None
    descripcion: Optional[str] = None
    id_categoria: Optional[UUID] = None
    id_usuario_mod: Optional[UUID] = None


class PlatoResponse(PlatoBase):
    id: UUID
    fecha_registro: date
    fecha_actualizacion: Optional[date] = None
    id_usuario: UUID
    id_usuario_mod: Optional[UUID] = None

    class Config:
        from_attributes = True


"""Modelo base para la entidad Reserva"""


class ReservaBase(BaseModel):
    id_cliente: UUID
    id_mesa: UUID
    cantidad_personas: int
    fecha_Hora: datetime
    Estado: bool


class ReservaCreate(ReservaBase):
    id_usuario: UUID


class ReservaUpdate(BaseModel):
    cantidad_personas: Optional[int] = None
    fecha_Hora: Optional[datetime] = None
    Estado: Optional[bool] = None
    id_usuario_mod: Optional[UUID] = None


class ReservaResponse(ReservaBase):
    fecha_registro: date
    fecha_actualizacion: Optional[date] = None
    id_usuario: UUID
    id_usuario_mod: Optional[UUID] = None

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

class LoginRequest(BaseModel):
    email: str
    contraseña: str

class LoginResponse(BaseModel):
    token: str
    usuario: UsuarioResponse