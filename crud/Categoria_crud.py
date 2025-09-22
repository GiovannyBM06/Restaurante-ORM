from sqlalchemy.orm import Session
from entities.Categoria import Categoria
from typing import Optional, List
from uuid import UUID
import re

class CategoriaCRUD:
	def __init__(self, db: Session):
		self.db = db

	def _validar_nombre(self, nombre: str) -> bool:
		pattern = r"^[a-zA-Z]{1,20}$"
		return re.match(pattern, nombre) is not None

	def _validar_descripcion(self, descripcion: Optional[str]) -> bool:
		if descripcion is None:
			return True
		return 0 < len(descripcion.strip()) <= 150

	def crear_categoria(self, nombre: str, descripcion: Optional[str], id_usuario: UUID) -> Categoria:
		if not self._validar_nombre(nombre):
			raise ValueError("Nombre de categoría inválido")
		if not self._validar_descripcion(descripcion):
			raise ValueError("Descripción inválida (1-200 caracteres)")
		categoria = Categoria(nombre=nombre.strip(), descripcion=descripcion, id_usuario=id_usuario)
		self.db.add(categoria)
		self.db.commit()
		self.db.refresh(categoria)
		return categoria

	def obtener_categoria(self, categoria_id: UUID) -> Optional[Categoria]:
		return self.db.query(Categoria).filter(Categoria.id == categoria_id).first()

	def obtener_categorias(self, skip: int = 0) -> List[Categoria]:
		return self.db.query(Categoria).offset(skip).all()

	def actualizar_categoria(self, categoria_id: UUID, **kwargs) -> Optional[Categoria]:
		categoria = self.obtener_categoria(categoria_id)
		if not categoria:
			return None
		if "nombre" in kwargs and not self._validar_nombre(kwargs["nombre"]):
			raise ValueError("Nombre de categoría inválido")
		if "descripcion" in kwargs and not self._validar_descripcion(kwargs["descripcion"]):
			raise ValueError("Descripción inválida (1-200 caracteres)")
		for key, value in kwargs.items():
			if hasattr(categoria, key):
				setattr(categoria, key, value)
		self.db.commit()
		self.db.refresh(categoria)
		return categoria
"""
	def eliminar_categoria(self, categoria_id: UUID) -> bool:
		categoria = self.obtener_categoria(categoria_id)
		if not categoria:
			return False
		self.db.delete(categoria)
		self.db.commit()
		return True
"""