from typing import List
from uuid import UUID
from crud.Plato_Orden_crud import PlatoOrdenCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import PlatoOrdenCreate, PlatoOrdenUpdate, PlatoOrdenResponse, RespuestaAPI

router = APIRouter(prefix="/platos_orden", tags=["Platos en Órdenes"])


@router.get("/", response_model=List[PlatoOrdenResponse])
async def obtener_platos_orden(db: Session = Depends(get_db)):
    try:
        po_crud = PlatoOrdenCRUD(db)
        items = po_crud.obtener_platos_orden()
        return items
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener platos_orden: {str(e)}"
        )


@router.get("/{id_orden}/{id_plato}", response_model=PlatoOrdenResponse)
async def obtener_plato_orden(
    id_orden: UUID, id_plato: UUID, db: Session = Depends(get_db)
):
    try:
        po_crud = PlatoOrdenCRUD(db)
        item = po_crud.obtener_plato_orden(id_orden, id_plato)
        if not item:
            raise HTTPException(status_code=404, detail="Plato_Orden no encontrado")
        return item
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener plato_orden: {str(e)}"
        )


@router.post(
    "/", response_model=PlatoOrdenResponse, status_code=status.HTTP_201_CREATED
)
async def crear_plato_orden(datos: PlatoOrdenCreate, db: Session = Depends(get_db)):
    try:
        po_crud = PlatoOrdenCRUD(db)
        item = po_crud.crear_plato_orden(**datos.dict())
        return item
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al crear plato_orden: {str(e)}"
        )


@router.put("/{id_orden}/{id_plato}", response_model=PlatoOrdenResponse)
async def actualizar_plato_orden(
    id_orden: UUID,
    id_plato: UUID,
    datos: PlatoOrdenUpdate,
    db: Session = Depends(get_db),
):
    try:
        po_crud = PlatoOrdenCRUD(db)
        existe = po_crud.obtener_plato_orden(id_orden, id_plato)
        if not existe:
            raise HTTPException(status_code=404, detail="Plato_Orden no encontrado")

        datos_actualizar = datos.dict(exclude_unset=True)
        id_usuario_mod = datos_actualizar.pop("id_usuario_mod", None)
        actualizado = po_crud.actualizar_plato_orden(
            id_orden, id_plato, id_usuario_mod=id_usuario_mod, **datos_actualizar
        )
        return actualizado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar plato_orden: {str(e)}"
        )


@router.delete("/{id_orden}/{id_plato}", response_model=RespuestaAPI)
async def eliminar_plato_orden(
    id_orden: UUID, id_plato: UUID, db: Session = Depends(get_db)
):
    try:
        po_crud = PlatoOrdenCRUD(db)
        existe = po_crud.obtener_plato_orden(id_orden, id_plato)
        if not existe:
            raise HTTPException(status_code=404, detail="Plato_Orden no encontrado")

        eliminado = po_crud.eliminar_plato_orden(id_orden, id_plato)
        if eliminado:
            return RespuestaAPI(
                mensaje="Plato_Orden eliminado exitosamente", exito=True
            )
        else:
            raise HTTPException(status_code=500, detail="Error al eliminar plato_orden")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar plato_orden: {str(e)}"
        )
