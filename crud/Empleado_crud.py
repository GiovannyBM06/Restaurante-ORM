from sqlalchemy.orm import Session
from entities.Empleado import Empleado
from typing import Optional, List
from uuid import UUID
import re

class EmpleadoCRUD:
	def __init__(self, db: Session):
		self.db = db

	def _validar_nombre(self, nombre: str) -> bool:
		pattern = r"^[a-zA-Z]{1,20}$"
		return re.match(pattern, nombre) is not None

	def _validar_apellido(self, apellido: str) -> bool:
		pattern = r"^[a-zA-Z]{1,20}$"
		return re.match(pattern, apellido) is not None

	def _validar_rol(self, rol: str) -> bool:
		return 1 <= len(rol.strip()) <= 20

	def _validar_salario(self, salario: float) -> bool:
		return isinstance(salario, float) and salario > 0

	def crear_empleado(self, nombre: str, apellido: str, rol: str, salario: int, id_usuario: UUID) -> Empleado:
		if not self._validar_nombre(nombre):
			raise ValueError("Nombre inválido")
		if not self._validar_apellido(apellido):
			raise ValueError("Apellido inválido")
		if not self._validar_rol(rol):
			raise ValueError("Rol inválido")
		if not self._validar_salario(salario):
			raise ValueError("Salario inválido")
		empleado = Empleado(nombre=nombre.strip(), apellido=apellido.strip(), rol=rol.strip(), salario=salario, id_usuario=id_usuario)
		self.db.add(empleado)
		self.db.commit()
		self.db.refresh(empleado)
		return empleado

	def obtener_empleado(self, empleado_id: UUID) -> Optional[Empleado]:
		return self.db.query(Empleado).filter(Empleado.id == empleado_id).first()

	def obtener_empleados(self, skip: int = 0) -> List[Empleado]:
		return self.db.query(Empleado).offset(skip).all()

	def actualizar_empleado(self, empleado_id: UUID, **kwargs) -> Optional[Empleado]:
		empleado = self.obtener_empleado(empleado_id)
		if not empleado:
			return None
		if "nombre" in kwargs and not self._validar_nombre(kwargs["nombre"]):
			raise ValueError("Nombre inválido")
		if "apellido" in kwargs and not self._validar_apellido(kwargs["apellido"]):
			raise ValueError("Apellido inválido")
		if "rol" in kwargs and not self._validar_rol(kwargs["rol"]):
			raise ValueError("Rol inválido")
		if "salario" in kwargs and not self._validar_salario(kwargs["salario"]):
			raise ValueError("Salario inválido")
		for key, value in kwargs.items():
			if hasattr(empleado, key):
				setattr(empleado, key, value)
		self.db.commit()
		self.db.refresh(empleado)
		return empleado
"""
	def eliminar_empleado(self, empleado_id: UUID) -> bool:
		empleado = self.obtener_empleado(empleado_id)
		if not empleado:
			return False
		self.db.delete(empleado)
		self.db.commit()
		return True
"""