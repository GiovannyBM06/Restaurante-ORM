from sqlalchemy.orm import Session
from entities.Categoria import Categoria
from typing import Optional, List
from uuid import UUID
import re


class CategoriaCRUD:
    """
    Operaciones CRUD para la entidad Categoria.
    """

    def __init__(self, db: Session):
        """Inicializa con una sesión de base de datos."""
        self.db = db

    def _validar_nombre(self, nombre: str) -> bool:
        """Valida el nombre de la categoría (1-20 caracteres alfabéticos)."""
        pattern = r"^[a-zA-Z]{1,20}$"
        return re.match(pattern, nombre) is not None

    def _validar_descripcion(self, descripcion: Optional[str]) -> bool:
        """Valida la descripción (opcional, hasta 150 caracteres)."""
        if descripcion is None:
            return True
        return 0 < len(descripcion.strip()) <= 150

    def crear_categoria(
        self, nombre: str, descripcion: Optional[str], id_usuario: UUID
    ) -> Categoria:
        """Crea una nueva categoría después de validar sus campos."""
        if not self._validar_nombre(nombre):
            raise ValueError("Nombre de categoría inválido")
        if not self._validar_descripcion(descripcion):
            raise ValueError("Descripción inválida (1-200 caracteres)")
        categoria = Categoria(
            nombre=nombre.strip(), descripcion=descripcion, id_usuario=id_usuario
        )
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def obtener_categoria(self, categoria_id: UUID) -> Optional[Categoria]:
        """Obtiene una categoría por su UUID."""
        return self.db.query(Categoria).filter(Categoria.id == categoria_id).first()

    def obtener_categorias(self, skip: int = 0) -> List[Categoria]:
        """Obtiene una lista de categorías, con salto opcional para paginación."""
        return self.db.query(Categoria).offset(skip).all()

    def actualizar_categoria(self, categoria_id: UUID, id_usuario_mod: UUID, **kwargs) -> Optional[Categoria]:
        """Actualiza los campos de una categoría, actualizando id_usuario_mod y fecha_actualizacion solo si hay cambios."""
        from datetime import datetime

        categoria = self.obtener_categoria(categoria_id)
        if not categoria:
            return None
        cambios = False
        if "nombre" in kwargs and not self._validar_nombre(kwargs["nombre"]):
            raise ValueError("Nombre de categoría inválido")
        if "descripcion" in kwargs and not self._validar_descripcion(kwargs["descripcion"]):
            raise ValueError("Descripción inválida (1-200 caracteres)")
        for key, value in kwargs.items():
            if hasattr(categoria, key):
                if getattr(categoria, key) != value:
                    setattr(categoria, key, value)
                    cambios = True
        if cambios:
            if id_usuario_mod:
                categoria.id_usuario_mod = id_usuario_mod
            categoria.fecha_actualizacion = datetime.now()
            self.db.commit()
            self.db.refresh(categoria)
        return categoria

    def eliminar_categoria(self, categoria_id: UUID) -> bool:
        """Elimina una categoría por su UUID."""
        categoria = self.obtener_categoria(categoria_id)
        if not categoria:
            return False
        self.db.delete(categoria)
        self.db.commit()
        return True
