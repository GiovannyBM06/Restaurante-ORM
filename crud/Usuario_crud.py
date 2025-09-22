from sqlalchemy.orm import Session;
from entities.Usuario import Usuario
from typing import Optional, List
from uuid import UUID
import re
class UsuarioCRUD:

    def __init__(self, db: Session):
        self.db= db

    def _validar_nombre(self,nombre: str) -> bool:
        """Validar formato de nombre"""
        pattern = r"^[a-zA-Z]{1,20}$"
        return re.match(pattern, nombre) is not None

    def _validar_apellido(self,apellido: str) -> bool:
        """Validar formato de apellido"""
        pattern = r"^[a-zA-Z]{1,20}$"
        return re.match(pattern, apellido) is not None
    
    def _validar_email(self, email: str) -> bool:
        """Validar formato de email"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,40}$"
        return re.match(pattern, email) is not None
    
    def _validar_contraseña(self, contraseña:str) -> bool:
        """Validar formato de contraseña"""
        pattern = r"^[a-zA-Z._-*]{6,20}$"
        return re.match(pattern, contraseña) is not None
    
    def crear_usuario(
        self,
        nombre: str,
        apellido:str,
        email:str,
        contraseña:str,
        es_admin: bool= False,
    )-> Usuario:
        
        if not nombre or len(nombre.strip())==0:
            raise ValueError("El usuario debe tener nombre")
        if len(nombre)> 20:
            raise ValueError("El nombre nop puede tener más de 10 caracteres")
    

    def obtener_usuario(self, usuario_id: UUID)-> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    def obtener_usuario_con_email(self, email:str)-> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.email== email.lower().strip()).first()
    
    def obtener_usuario_con_nombre(self,nombre:str)-> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.nombre== nombre.lower().strip().all())
    
    def autenticar_usuario(self, email:str, contraseña:str)-> Optional[Usuario]:
        usuario = self.obtener_usuario_con_email
        if not usuario:
            return None
        
        if Usuario.contraseña == contraseña:
            return usuario
        return None
    
    def cambiar_contraseña(self, usuario_id: UUID, contraseña_actual: str, contraseña_nueva: str) -> bool:
        """
        Cambia la contraseña de un usuario si la contraseña actual es correcta.
        """
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")

        if usuario.contraseña != contraseña_actual:
            raise ValueError("La contraseña actual es incorrecta")

        if not self._validar_contraseña(contraseña_nueva):
            raise ValueError("La nueva contraseña no cumple con los requisitos de formato")

        usuario.contraseña = contraseña_nueva
        self.db.commit()
        return True
    
    def obtener_usuarios(self, skip:int = 0)-> List[Usuario]:
        return self.db.query(Usuario).offset(skip).all()
    
    def actualizar_usuario(self,usuario_id:UUID, **kwargs)-> Optional[Usuario]:
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return None
        
        if "email" in kwargs:
            email = kwargs["email"]
            if not self._validar_email(email):
                raise ValueError("Email inválido")
            if(
                self.obtener_usuario_con_email(email)
                and self.obtener_usuario_con_email(email).id != usuario_id
            ):
                raise ValueError("El Email ya se encuantra registrado")
            kwargs["email"] = email.lower().strip()
        
        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not self._validar_nombre(nombre):
                raise ValueError("Nombre inválido")

        if "apellido" in kwargs:
            apellido = kwargs["apellido"]
            if not self._validar_apellido(apellido):
                raise ValueError("apellido inválido") 

        if "contraseña" in kwargs:
            contraseña = kwargs["cotraseña"]
            if not self._validar_contraseña(contraseña):
                raise ValueError ("Contraseña inválida")
        
        for key, value in kwargs.items():
            if hasattr(usuario, key):
                setattr(usuario, key, value)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario
    