from typing import List
from uuid import UUID
from crud.Empleado_crud import EmpleadoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import *

router = APIRouter(prefix="/empleados", tags=["empleados"])


@router.get("/", response_model=list[EmpleadoResponse])
async def obtener_empleados(db: Session = Depends(get_db)):
    try:
        empleado_crud = EmpleadoCRUD(db)
        empleados = empleado_crud.obtener_empleados()
        return empleados
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener empleados: {str(e)}",
        )


@router.get("/{empleado_id}", response_model=EmpleadoResponse)
async def obtener_empleado(empleado_id: UUID, db: Session = Depends(get_db)):
    try:
        empleado_crud = EmpleadoCRUD(db)
        empleado = empleado_crud.obtener_empleado(empleado_id)
        if not empleado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado"
            )
        return empleado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener empleado: {str(e)}",
        )


@router.post("/", response_model=EmpleadoResponse, status_code=status.HTTP_201_CREATED)
async def crear_empleado(datos_empleado: EmpleadoCreate, db: Session = Depends(get_db)):
    try:
        empleado_crud = EmpleadoCRUD(db)
        empleado = empleado_crud.crear_empleado(
            nombre=datos_empleado.nombre,
            apellido=datos_empleado.apellido,
            rol=datos_empleado.rol,
            salario=datos_empleado.salario,
            id_usuario=datos_empleado.id_usuario,
        )
        return empleado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear empleado: {str(e)}",
        )


@router.put("/{empleado_id}", response_model=EmpleadoResponse)
async def actualizar_empleado(
    empleado_id: UUID, datos_empleado: EmpleadoUpdate, db: Session = Depends(get_db)
):
    try:
        empleado_crud = EmpleadoCRUD(db)
        empleado_existe = empleado_crud.obtener_empleado(empleado_id)
        if not empleado_existe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado"
            )
        datos_actualizar = datos_empleado.dict(exclude_unset=True)
        id_usuario_mod = datos_actualizar.pop("id_usuario_mod", None)
        empleado_actualizado = empleado_crud.actualizar_empleado(
            empleado_id, id_usuario_mod=id_usuario_mod, **datos_actualizar
        )
        return empleado_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar empleado: {str(e)}",
        )


@router.delete("/{empleado_id}", response_model=RespuestaAPI)
async def eliminar_empleado(empleado_id: UUID, db: Session = Depends(get_db)):
    try:
        empleado_crud = EmpleadoCRUD(db)
        empleado_existe = empleado_crud.obtener_empleado(empleado_id)
        if not empleado_existe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado"
            )
        eliminado = empleado_crud.eliminar_empleado(empleado_id)
        if eliminado:
            return RespuestaAPI(mensaje="Empleado eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar empleado",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar empleado: {str(e)}",
        )
