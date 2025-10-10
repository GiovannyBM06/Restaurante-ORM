from typing import List
from uuid import UUID
from crud.Categoria_crud import CategoriaCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from schemas import *

router = APIRouter(prefix="/categorias", tags=["categorias"])

"""Rutas para la gestión de categorías."""


@router.get("/", response_model=List[CategoriaResponse])
async def obtener_categorias(db: Session = Depends(get_db)):
    try:
        categoria_crud = CategoriaCRUD(db)
        categorias = categoria_crud.obtener_categorias()
        return categorias
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener categorías: {str(e)}",
        )


@router.get("/{categoria_id}", response_model=CategoriaResponse)
async def obtener_categoria(categoria_id: UUID, db: Session = Depends(get_db)):
    try:
        categoria_crud = CategoriaCRUD(db)
        categoria = categoria_crud.obtener_categoria(categoria_id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
            )
        return categoria
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener categoría: {str(e)}",
        )


@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
async def crear_categoria(
    datos_categoria: CategoriaCreate, db: Session = Depends(get_db)
):
    try:
        categoria_crud = CategoriaCRUD(db)
        categoria = categoria_crud.crear_categoria(**datos_categoria.dict())
        return categoria
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear categoría: {str(e)}",
        )


@router.put("/{categoria_id}", response_model=CategoriaResponse)
async def actualizar_categoria(
    categoria_id: UUID, datos_categoria: CategoriaUpdate, db: Session = Depends(get_db)
):
    try:
        categoria_crud = CategoriaCRUD(db)
        categoria_existe = categoria_crud.obtener_categoria(categoria_id)
        if not categoria_existe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
            )
        datos_actualizar = datos_categoria.dict(exclude_unset=True)
        id_usuario_mod = datos_actualizar.pop("id_usuario_mod", None)
        categoria_actualizada = categoria_crud.actualizar_categoria(
            categoria_id, id_usuario_mod=id_usuario_mod, **datos_actualizar
        )
        return categoria_actualizada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar categoría: {str(e)}",
        )


@router.delete("/{categoria_id}", response_model=RespuestaAPI)
async def eliminar_categoria(categoria_id: UUID, db: Session = Depends(get_db)):
    try:
        categoria_crud = CategoriaCRUD(db)
        categoria_existe = categoria_crud.obtener_categoria(categoria_id)
        if not categoria_existe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
            )
        eliminado = categoria_crud.eliminar_categoria(categoria_id)
        if eliminado:
            return RespuestaAPI(mensaje="Categoría eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar categoría",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar categoría: {str(e)}",
        )
