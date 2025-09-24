from sqlalchemy.orm import Session
from entities.Empleado import Empleado
from typing import Optional, List
from uuid import UUID
import re
class EmpleadoCRUD:
    """
    Operaciones CRUD para la entidad Empleado.
    """

    def __init__(self, db: Session):
        """Inicializa con una sesión de base de datos."""
        self.db = db

    def _validar_nombre(self, nombre: str) -> bool:
        """Valida el nombre del empleado (1-20 caracteres alfabéticos)."""
        pattern = r"^[a-zA-Z]{1,20}$"
        return re.match(pattern, nombre) is not None

    def _validar_apellido(self, apellido: str) -> bool:
        """Valida el apellido del empleado (1-20 caracteres alfabéticos)."""
        pattern = r"^[a-zA-Z]{1,20}$"
        return re.match(pattern, apellido) is not None

    def _validar_rol(self, rol: str) -> bool:
        """Valida el rol del empleado (1-20 caracteres)."""
        return 1 <= len(rol.strip()) <= 20

    def _validar_salario(self, salario: float) -> bool:
        """Valida el salario del empleado (debe ser un número positivo)."""
        return isinstance(salario, float) and salario > 0

    def crear_empleado(
        self, nombre: str, apellido: str, rol: str, salario: int, id_usuario: UUID
    ) -> Empleado:
        """Crea un nuevo empleado después de validar sus campos."""
        if not self._validar_nombre(nombre):
            raise ValueError("Nombre inválido")
        if not self._validar_apellido(apellido):
            raise ValueError("Apellido inválido")
        if not self._validar_rol(rol):
            raise ValueError("Rol inválido")
        if not self._validar_salario(salario):
            raise ValueError("Salario inválido")
        empleado = Empleado(
            nombre=nombre.strip(),
            apellido=apellido.strip(),
            rol=rol.strip(),
            salario=salario,
            id_usuario=id_usuario,
        )
        self.db.add(empleado)
        self.db.commit()
        self.db.refresh(empleado)
        return empleado

    def obtener_empleado(self, empleado_id: UUID) -> Optional[Empleado]:
        """Obtiene un empleado por su UUID."""
        return self.db.query(Empleado).filter(Empleado.id == empleado_id).first()

    def obtener_empleados(self, skip: int = 0) -> List[Empleado]:
        """Obtiene una lista de empleados, con salto opcional para paginación."""
        return self.db.query(Empleado).offset(skip).all()

    def actualizar_empleado(self, empleado_id: UUID, id_usuario_mod: UUID, **kwargs) -> Optional[Empleado]:
        """Actualiza los campos de un empleado, actualizando id_usuario_mod y fecha_actualizacion solo si hay cambios."""
        from datetime import datetime

        empleado = self.obtener_empleado(empleado_id)
        if not empleado:
            return None
        cambios = False
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
                if getattr(empleado, key) != value:
                    setattr(empleado, key, value)
                    cambios = True
        if cambios:
            if id_usuario_mod:
                empleado.id_usuario_mod = id_usuario_mod
            if hasattr(empleado, "fecha_actualizacion"):
                empleado.fecha_actualizacion = datetime.now()
            self.db.commit()
            self.db.refresh(empleado)
        return empleado

    def eliminar_empleado(self, empleado_id: UUID) -> bool:
        """Elimina un empleado por su UUID."""
        empleado = self.obtener_empleado(empleado_id)
        if not empleado:
            return False
        self.db.delete(empleado)
        self.db.commit()
        return True
