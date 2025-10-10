from typing import List
from uuid import UUID
from crud.Factura_crud import FacturaCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import *

router = APIRouter(prefix="/facturas", tags=["facturas"])


@router.get("/", response_model=list[FacturaResponse])
async def obtener_facturas(db: Session = Depends(get_db)):
    try:
        factura_crud = FacturaCRUD(db)
        facturas = factura_crud.obtener_facturas()
        return facturas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener facturas: {str(e)}",
        )


@router.get("/{factura_id}", response_model=FacturaResponse)
async def obtener_factura(factura_id: UUID, db: Session = Depends(get_db)):
    try:
        factura_crud = FacturaCRUD(db)
        factura = factura_crud.obtener_factura(factura_id)
        if not factura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
            )
        return factura
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener factura: {str(e)}",
        )


@router.post("/", response_model=FacturaResponse, status_code=status.HTTP_201_CREATED)
async def crear_factura(datos_factura: FacturaCreate, db: Session = Depends(get_db)):
    try:
        factura_crud = FacturaCRUD(db)
        factura = factura_crud.crear_factura(**datos_factura.dict())
        return factura
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear factura: {str(e)}",
        )


@router.put("/{factura_id}", response_model=FacturaResponse)
async def actualizar_factura(
    factura_id: UUID, datos_factura: FacturaUpdate, db: Session = Depends(get_db)
):
    try:
        factura_crud = FacturaCRUD(db)
        factura_existe = factura_crud.obtener_factura(factura_id)
        if not factura_existe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
            )
        datos_actualizar = datos_factura.dict(exclude_unset=True)
        id_usuario_mod = datos_actualizar.pop("id_usuario_mod", None)
        factura_actualizada = factura_crud.actualizar_factura(
            factura_id, id_usuario_mod=id_usuario_mod, **datos_actualizar
        )
        return factura_actualizada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar factura: {str(e)}",
        )


@router.delete("/{factura_id}", response_model=RespuestaAPI)
async def eliminar_factura(factura_id: UUID, db: Session = Depends(get_db)):
    try:
        factura_crud = FacturaCRUD(db)
        factura_existe = factura_crud.obtener_factura(factura_id)
        if not factura_existe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
            )
        eliminado = factura_crud.eliminar_factura(factura_id)
        if eliminado:
            return RespuestaAPI(mensaje="Factura eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar factura",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar factura: {str(e)}",
        )
