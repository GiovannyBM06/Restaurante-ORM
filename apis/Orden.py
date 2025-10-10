from typing import List
from uuid import UUID
from crud.Orden_crud import OrdenCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import *

router = APIRouter(prefix="/ordenes", tags=["ordenes"])


@router.get("/", response_model=list[OrdenResponse])
async def obtener_ordenes(db: Session = Depends(get_db)):
    try:
        orden_crud = OrdenCRUD(db)
        ordenes = orden_crud.obtener_ordenes()
        return ordenes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener ordenes: {str(e)}",
        )


@router.get("/{orden_id}", response_model=OrdenResponse)
async def obtener_orden(orden_id: UUID, db: Session = Depends(get_db)):
    try:
        orden_crud = OrdenCRUD(db)
        orden = orden_crud.obtener_orden(orden_id)
        if not orden:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada"
            )
        return orden
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener orden: {str(e)}",
        )


@router.post("/", response_model=OrdenResponse, status_code=status.HTTP_201_CREATED)
async def crear_orden(datos_orden: OrdenCreate, db: Session = Depends(get_db)):
    try:
        orden_crud = OrdenCRUD(db)
        orden = orden_crud.crear_orden(**datos_orden.dict())
        return orden
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear orden: {str(e)}",
        )


@router.put("/{orden_id}", response_model=OrdenResponse)
async def actualizar_orden(
    orden_id: UUID, datos_orden: OrdenUpdate, db: Session = Depends(get_db)
):
    try:
        orden_crud = OrdenCRUD(db)
        orden_existe = orden_crud.obtener_orden(orden_id)
        if not orden_existe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada"
            )
        datos_actualizar = datos_orden.dict(exclude_unset=True)
        id_usuario_mod = datos_actualizar.pop("id_usuario_mod", None)
        orden_actualizada = orden_crud.actualizar_orden(
            orden_id, id_usuario_mod=id_usuario_mod, **datos_actualizar
        )
        return orden_actualizada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar orden: {str(e)}",
        )


@router.delete("/{orden_id}", response_model=RespuestaAPI)
async def eliminar_orden(orden_id: UUID, db: Session = Depends(get_db)):
    try:
        orden_crud = OrdenCRUD(db)
        orden_existe = orden_crud.obtener_orden(orden_id)
        if not orden_existe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada"
            )
        eliminado = orden_crud.eliminar_orden(orden_id)
        if eliminado:
            return RespuestaAPI(mensaje="Orden eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar orden",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar orden: {str(e)}",
        )
