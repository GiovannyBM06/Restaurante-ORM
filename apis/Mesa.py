from typing import List
from uuid import UUID
from crud.Mesa_crud import MesaCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import *

router = APIRouter(prefix="/mesas", tags=["mesas"])

"""Métodos get para Factura"""
@router.get("/", response_model=List[MesaResponse])
async def obtener_mesas(db: Session = Depends(get_db)):
    try:
        mesa_crud = MesaCRUD(db)
        mesas = mesa_crud.obtener_mesas()
        return mesas
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener mesas: {str(e)}")

@router.get("/{mesa_id}", response_model=MesaResponse)
async def obtener_mesa(mesa_id: UUID, db: Session = Depends(get_db)):
    try:
        mesa_crud = MesaCRUD(db)
        mesa = mesa_crud.obtener_mesa(mesa_id)
        if not mesa:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mesa no encontrada")
        return mesa
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener mesa: {str(e)}")

"""Método post para Factura"""
@router.post("/", response_model=MesaResponse, status_code=status.HTTP_201_CREATED)
async def crear_mesa(datos_mesa: MesaCreate, db: Session = Depends(get_db)):
    try:
        mesa_crud = MesaCRUD(db)
        mesa = mesa_crud.crear_mesa(**datos_mesa.dict())
        return mesa
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear mesa: {str(e)}")

"""Método put para Factura"""
@router.put("/{mesa_id}", response_model=MesaResponse)
async def actualizar_mesa(mesa_id: UUID, datos_mesa: MesaUpdate, db: Session = Depends(get_db)):
    try:
        mesa_crud = MesaCRUD(db)
        mesa_existe = mesa_crud.obtener_mesa(mesa_id)
        if not mesa_existe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mesa no encontrada")
        datos_actualizar = datos_mesa.dict(exclude_unset=True)
        mesa_actualizada = mesa_crud.actualizar_mesa(mesa_id, **datos_actualizar)
        return mesa_actualizada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al actualizar mesa: {str(e)}")

"""Método delete para Factura"""
@router.delete("/{mesa_id}", response_model=RespuestaAPI)
async def eliminar_mesa(mesa_id: UUID, db: Session = Depends(get_db)):
    try:
        mesa_crud = MesaCRUD(db)
        mesa_existe = mesa_crud.obtener_mesa(mesa_id)
        if not mesa_existe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mesa no encontrada")
        eliminado = mesa_crud.eliminar_mesa(mesa_id)
        if eliminado:
            return RespuestaAPI(mensaje="Mesa eliminada exitosamente", exito=True)
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar mesa")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al eliminar mesa: {str(e)}")