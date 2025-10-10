from typing import List
from uuid import UUID
from crud.Reserva_crud import ReservaCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import *

router = APIRouter(prefix="/reservas", tags=["reservas"])


@router.get("/", response_model=List[ReservaResponse])
async def obtener_reservas(db: Session = Depends(get_db)):
    reserva_crud = ReservaCRUD(db)
    return reserva_crud.obtener_reservas()


@router.get("/{id_cliente}/{id_mesa}", response_model=ReservaResponse)
async def obtener_reserva(
    id_cliente: UUID, id_mesa: UUID, db: Session = Depends(get_db)
):
    reserva_crud = ReservaCRUD(db)
    reserva = reserva_crud.obtener_reserva(id_cliente, id_mesa)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva


@router.post("/", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
async def crear_reserva(datos_reserva: ReservaCreate, db: Session = Depends(get_db)):
    reserva_crud = ReservaCRUD(db)
    return reserva_crud.crear_reserva(**datos_reserva.dict())


@router.put("/{id_cliente}/{id_mesa}", response_model=ReservaResponse)
async def actualizar_reserva(
    id_cliente: UUID,
    id_mesa: UUID,
    datos_reserva: ReservaUpdate,
    db: Session = Depends(get_db),
):
    reserva_crud = ReservaCRUD(db)
    reserva_actualizada = reserva_crud.actualizar_reserva(
        id_cliente,
        id_mesa,
        id_usuario_mod=datos_reserva.id_usuario_mod,
        **datos_reserva.dict(exclude_unset=True)
    )
    if not reserva_actualizada:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva_actualizada


@router.delete("/{id_cliente}/{id_mesa}", response_model=RespuestaAPI)
async def eliminar_reserva(
    id_cliente: UUID, id_mesa: UUID, db: Session = Depends(get_db)
):
    reserva_crud = ReservaCRUD(db)
    eliminado = reserva_crud.eliminar_reserva(id_cliente, id_mesa)
    if eliminado:
        return RespuestaAPI(mensaje="Reserva eliminada exitosamente", exito=True)
    raise HTTPException(status_code=404, detail="Reserva no encontrada")
