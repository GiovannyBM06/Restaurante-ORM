from typing import List
from uuid import UUID
from crud.Reserva_crud import ReservaCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import *

router = APIRouter(prefix="/reservas", tags=["reservas"])

"""Métodos get para Reserva"""
@router.get("/", response_model=List[ReservaResponse])
async def obtener_reservas(db: Session = Depends(get_db)):
    try:
        reserva_crud = ReservaCRUD(db)
        reservas = reserva_crud.obtener_reservas()
        return reservas
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener reservas: {str(e)}")

@router.get("/{reserva_id}", response_model=ReservaResponse)
async def obtener_reserva(reserva_id: UUID, db: Session = Depends(get_db)):
    try:
        reserva_crud = ReservaCRUD(db)
        reserva = reserva_crud.obtener_reserva(reserva_id)
        if not reserva:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
        return reserva
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener reserva: {str(e)}")

"""Método post para Reserva"""
@router.post("/", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
async def crear_reserva(datos_reserva: ReservaCreate, db: Session = Depends(get_db)):
    try:
        reserva_crud = ReservaCRUD(db)
        reserva = reserva_crud.crear_reserva(**datos_reserva.dict())
        return reserva
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear reserva: {str(e)}")

"""Método put para Reserva"""
@router.put("/{reserva_id}", response_model=ReservaResponse)
async def actualizar_reserva(reserva_id: UUID, datos_reserva: ReservaUpdate, db: Session = Depends(get_db)):
    try:
        reserva_crud = ReservaCRUD(db)
        reserva_existe = reserva_crud.obtener_reserva(reserva_id)
        if not reserva_existe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
        datos_actualizar = datos_reserva.dict(exclude_unset=True)
        reserva_actualizada = reserva_crud.actualizar_reserva(reserva_id, **datos_actualizar)
        return reserva_actualizada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al actualizar reserva: {str(e)}")

"""Método delete para Reserva"""
@router.delete("/{reserva_id}", response_model=RespuestaAPI)
async def eliminar_reserva(reserva_id: UUID, db: Session = Depends(get_db)):
    try:
        reserva_crud = ReservaCRUD(db)
        reserva_existe = reserva_crud.obtener_reserva(reserva_id)
        if not reserva_existe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
        eliminado = reserva_crud.eliminar_reserva(reserva_id)
        if eliminado:
            return RespuestaAPI(mensaje="Reserva eliminada exitosamente", exito=True)
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar reserva")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al eliminar reserva: {str(e)}")