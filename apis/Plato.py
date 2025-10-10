from typing import List
from uuid import UUID
from crud.Plato_crud import PlatoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import *

router = APIRouter(prefix="/platos", tags=["platos"])

"""Métodos get para Plato"""
@router.get("/", response_model=List[PlatoResponse])
async def obtener_platos(db: Session = Depends(get_db)):
    try:
        plato_crud = PlatoCRUD(db)
        platos = plato_crud.obtener_platos()
        return platos
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener platos: {str(e)}")

@router.get("/{plato_id}", response_model=PlatoResponse)
async def obtener_plato(plato_id: UUID, db: Session = Depends(get_db)):
    try:
        plato_crud = PlatoCRUD(db)
        plato = plato_crud.obtener_plato(plato_id)
        if not plato:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plato no encontrado")
        return plato
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener plato: {str(e)}")

"""Método post para Plato"""
@router.post("/", response_model=PlatoResponse, status_code=status.HTTP_201_CREATED)
async def crear_plato(datos_plato: PlatoCreate, db: Session = Depends(get_db)):
    try:
        plato_crud = PlatoCRUD(db)
        plato = plato_crud.crear_plato(**datos_plato.dict())
        return plato
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear plato: {str(e)}")

"""Método put para Plato"""
@router.put("/{plato_id}", response_model=PlatoResponse)
async def actualizar_plato(plato_id: UUID, datos_plato: PlatoUpdate, db: Session = Depends(get_db)):
    try:
        plato_crud = PlatoCRUD(db)
        plato_existe = plato_crud.obtener_plato(plato_id)
        if not plato_existe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plato no encontrado")
        datos_actualizar = datos_plato.dict(exclude_unset=True)
        plato_actualizado = plato_crud.actualizar_plato(plato_id, **datos_actualizar)
        return plato_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al actualizar plato: {str(e)}")

"""Método delete para Plato"""
@router.delete("/{plato_id}", response_model=RespuestaAPI)
async def eliminar_plato(plato_id: UUID, db: Session = Depends(get_db)):
    try:
        plato_crud = PlatoCRUD(db)
        plato_existe = plato_crud.obtener_plato(plato_id)
        if not plato_existe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plato no encontrado")
        eliminado = plato_crud.eliminar_plato(plato_id)
        if eliminado:
            return RespuestaAPI(mensaje="Plato eliminado exitosamente", exito=True)
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar plato")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al eliminar plato: {str(e)}")