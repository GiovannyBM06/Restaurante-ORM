from typing import List
from uuid import UUID
from crud.Plato_Orden_crud import PlatoOrdenCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import *

router = APIRouter(prefix="/plato_orden", tags=["plato_orden"])

"""Métodos get para Plato-Orden"""
@router.get("/", response_model=List[PlatoOrdenResponse])
async def obtener_platos_orden(db: Session = Depends(get_db)):
    try:
        po_crud = PlatoOrdenCRUD(db)
        items = po_crud.obtener_platos_orden()
        return items
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener platos_orden: {str(e)}")

@router.get("/{plato_orden_id}", response_model=PlatoOrdenResponse)
async def obtener_plato_orden(plato_orden_id: UUID, db: Session = Depends(get_db)):
    try:
        po_crud = PlatoOrdenCRUD(db)
        item = po_crud.obtener_plato_orden(plato_orden_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plato_Orden no encontrado")
        return item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener plato_orden: {str(e)}")

"""Método post para Plato-Orden"""
@router.post("/", response_model=PlatoOrdenResponse, status_code=status.HTTP_201_CREATED)
async def crear_plato_orden(datos: PlatoOrdenCreate, db: Session = Depends(get_db)):
    try:
        po_crud = PlatoOrdenCRUD(db)
        item = po_crud.crear_plato_orden(**datos.dict())
        return item
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear plato_orden: {str(e)}")

"""Método put para Plato-Orden"""
@router.put("/{plato_orden_id}", response_model=PlatoOrdenResponse)
async def actualizar_plato_orden(plato_orden_id: UUID, datos: PlatoOrdenUpdate, db: Session = Depends(get_db)):
    try:
        po_crud = PlatoOrdenCRUD(db)
        existe = po_crud.obtener_plato_orden(plato_orden_id)
        if not existe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plato_Orden no encontrado")
        datos_actualizar = datos.dict(exclude_unset=True)
        actualizado = po_crud.actualizar_plato_orden(plato_orden_id, **datos_actualizar)
        return actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al actualizar plato_orden: {str(e)}")

"""Método delete para Plato-Orden"""
@router.delete("/{plato_orden_id}", response_model=RespuestaAPI)
async def eliminar_plato_orden(plato_orden_id: UUID, db: Session = Depends(get_db)):
    try:
        po_crud = PlatoOrdenCRUD(db)
        existe = po_crud.obtener_plato_orden(plato_orden_id)
        if not existe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plato_Orden no encontrado")
        eliminado = po_crud.eliminar_plato_orden(plato_orden_id)
        if eliminado:
            return RespuestaAPI(mensaje="Plato_Orden eliminado exitosamente", exito=True)
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar plato_orden")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al eliminar plato_orden: {str(e)}")