from sqlalchemy.orm import Session
from entities.Plato import Plato
from typing import Optional, List
from uuid import UUID
import re


class PlatoCRUD:
    """
    Operaciones CRUD para la entidad Plato.
    """

    def __init__(self, db: Session):
        """Inicializa con una sesión de base de datos."""
        self.db = db

    def _validar_nombre(self, nombre: str) -> bool:
        """Valida el nombre del plato (1-20 caracteres alfabéticos)."""
        pattern = r"^[a-zA-Z]{1,20}$"
        return re.match(pattern, nombre) is not None

    def _validar_precio(self, precio: int) -> bool:
        """Valida el precio del plato (debe ser un entero positivo)."""
        return isinstance(precio, int) and precio > 0

    def _validar_descripcion(self, descripcion: str) -> bool:
        """Valida la descripción del plato (opcional, hasta 100 caracteres)."""
        return descripcion is None or (0 < len(descripcion.strip()) <= 100)

    def crear_plato(
        self,
        nombre: str,
        precio_unidad: int,
        descripcion: str,
        id_categoria: UUID,
        id_usuario: UUID,
    ) -> Plato:
        """Crea un nuevo plato después de validar sus campos."""
        if not self._validar_nombre(nombre):
            raise ValueError("Nombre inválido")
        if not self._validar_precio(precio_unidad):
            raise ValueError("Precio inválido")
        if not self._validar_descripcion(descripcion):
            raise ValueError("Descripción inválida")
        plato = Plato(
            nombre=nombre.strip(),
            precio_unidad=precio_unidad,
            descripcion=descripcion,
            id_categoria=id_categoria,
            id_usuario=id_usuario,
        )
        self.db.add(plato)
        self.db.commit()
        self.db.refresh(plato)
        return plato

    def obtener_plato(self, plato_id: UUID) -> Optional[Plato]:
        """Obtiene un plato por su UUID."""
        return self.db.query(Plato).filter(Plato.id == plato_id).first()

    def obtener_platos(self, skip: int = 0) -> List[Plato]:
        """Obtiene una lista de platos, con salto opcional para paginación."""
        return self.db.query(Plato).offset(skip).all()

    def actualizar_plato(
        self, plato_id: UUID, id_usuario_mod: UUID, **kwargs
    ) -> Optional[Plato]:
        """Actualiza los campos de un plato, actualizando id_usuario_mod y fecha_actualizacion solo si hay cambios."""
        from datetime import datetime

        plato = self.obtener_plato(plato_id)
        if not plato:
            return None
        cambios = False
        if "nombre" in kwargs and not self._validar_nombre(kwargs["nombre"]):
            raise ValueError("Nombre inválido")
        if "precio_unidad" in kwargs and not self._validar_precio(
            kwargs["precio_unidad"]
        ):
            raise ValueError("Precio inválido")
        if "descripcion" in kwargs and not self._validar_descripcion(
            kwargs["descripcion"]
        ):
            raise ValueError("Descripción inválida")
        for key, value in kwargs.items():
            if hasattr(plato, key):
                if getattr(plato, key) != value:
                    setattr(plato, key, value)
                    cambios = True
        if cambios:
            if id_usuario_mod:
                plato.id_usuario_mod = id_usuario_mod
            if hasattr(plato, "fecha_actualizacion"):
                plato.fecha_actualizacion = datetime.now()
            self.db.commit()
            self.db.refresh(plato)
        return plato

    def eliminar_plato(self, plato_id: UUID) -> bool:
        """Elimina un plato por su UUID."""
        plato = self.obtener_plato(plato_id)
        if not plato:
            return False
        self.db.delete(plato)
        self.db.commit()
        return True
