from typing import List
from uuid import UUID
from crud.Cliente_crud import ClienteCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import *

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("/", response_model=List[ClienteResponse])
async def obtener_clientes(db: Session = Depends(get_db)):
    try:
        cliente_crud = ClienteCRUD(db)
        clientes = cliente_crud.obtener_clientes()
        return clientes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener clientes: {str(e)}",
        )


@router.get("/{cliente_id}", response_model=ClienteResponse)
async def obtener_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    try:
        cliente_crud = ClienteCRUD(db)
        cliente = cliente_crud.obtener_cliente(cliente_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
            )
        return cliente
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cliente: {str(e)}",
        )


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def crear_cliente(datos_cliente: ClienteCreate, db: Session = Depends(get_db)):
    try:
        cliente_crud = ClienteCRUD(db)
        cliente = cliente_crud.crear_cliente(
            nombre=datos_cliente.nombre,
            apellido=datos_cliente.apellido,
            Email=datos_cliente.email,
            telefono=datos_cliente.telefono,
            id_usuario=datos_cliente.id_usuario,
        )
        return cliente
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear cliente: {str(e)}",
        )


@router.put("/{cliente_id}", response_model=ClienteResponse)
async def actualizar_cliente(
    cliente_id: UUID, datos_cliente: ClienteUpdate, db: Session = Depends(get_db)
):
    try:
        cliente_crud = ClienteCRUD(db)
        cliente_existe = cliente_crud.obtener_cliente(cliente_id)
        if not cliente_existe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
            )
        datos_actualizar = datos_cliente.dict(exclude_unset=True, by_alias=True)
        id_usuario_mod = datos_actualizar.pop("id_usuario_mod", None)
        cliente_actualizado = cliente_crud.actualizar_cliente(
            cliente_id, id_usuario_mod=id_usuario_mod, **datos_actualizar
        )
        return cliente_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar cliente: {str(e)}",
        )


@router.delete("/{cliente_id}", response_model=RespuestaAPI)
async def eliminar_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    try:
        cliente_crud = ClienteCRUD(db)
        cliente_existe = cliente_crud.obtener_cliente(cliente_id)
        if not cliente_existe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
            )
        eliminado = cliente_crud.eliminar_cliente(cliente_id)
        if eliminado:
            return RespuestaAPI(mensaje="Cliente eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar cliente",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar cliente: {str(e)}",
        )
