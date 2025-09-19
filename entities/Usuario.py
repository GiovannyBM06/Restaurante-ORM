import uuid
from sqlalchemy import Column, Integer, String, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from database.config import Base


class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nombre = Column(String(20), nullable=False)
    apellido = Column(String(20), nullable=False)
    email = Column(String(40), nullable=False, unique=True)
    contraseña = Column(String(20), nullable=False)

    platos = relationship(
        "Plato", back_populates="usuario", foreign_keys="Plato.id_usuario"
    )
    categorias = relationship(
        "Categoria", back_populates="usuario", foreign_keys="Categoria.id_usuario"
    )
    empleados = relationship(
        "Empleado", back_populates="usuario", foreign_keys="Empleado.id_usuario"
    )
    clientes = relationship(
        "Cliente", back_populates="usuario", foreign_keys="Cliente.id_usuario"
    )
    reservas = relationship(
        "Reserva", back_populates="usuario", foreign_keys="Reserva.id_usuario"
    )
    facturas = relationship(
        "Factura", back_populates="usuario", foreign_keys="Factura.id_usuario"
    )
    ordenes = relationship(
        "Orden", back_populates="usuario", foreign_keys="Orden.id_usuario"
    )
    mesas = relationship(
        "Mesa", back_populates="usuario", foreign_keys="Mesa.id_usuario"
    )
    platos_orden = relationship(
        "Plato_Orden", back_populates="usuario", foreign_keys="Plato_Orden.id_usuario"
    )

    def __repr__(self):
        return f"Usuario(nombre='{self.nombre}', apellido='{self.apellido}', email='{self.email}')"

    def to_dict(self):
        return {"nombre": self.nombre, "apellido": self.apellido, "email": self.email}
