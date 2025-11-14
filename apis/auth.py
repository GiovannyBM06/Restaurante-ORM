from typing import List
from uuid import UUID
from crud.Usuario_crud import UsuarioCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import *
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = "506-456-651-224"
ALGORITHM = "HS256"
TIEMPO_DE_VIDA_TOKEN = 30


@router.post("/login", response_model=LoginResponse)
def login(login: LoginRequest, db: Session = Depends(get_db)):
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario = usuario_crud.obtener_usuario_con_email(login.email)

        if not usuario:
            raise HTTPException(status_code=400, detail="Usuario no encontrado")

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo o contraseña incorrectos"
                )
    
        if usuario.contraseña != login.contraseña:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo o contraseña incorrectos"
            )
    
        token_datos = {
            "sub": usuario.email,
            "exp": datetime.utcnow() + timedelta(minutes=TIEMPO_DE_VIDA_TOKEN)
        }

        token_jwt = jwt.encode(token_datos, SECRET_KEY, algorithm=ALGORITHM)

        return {
            "token": token_jwt,
            "usuario": UsuarioResponse.from_orm(usuario)
        }
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error durante el login: {str(e)}"
        )