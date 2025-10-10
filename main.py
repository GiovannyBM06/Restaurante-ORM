import uvicorn
from apis import (
    Categoria,
    Cliente,
    Empleado,
    Factura,
    Mesa,
    Orden,
    Plato_Orden,
    Plato,
    Reserva,
    Usuario,
)
from database.config import create_tables
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Sistema de Gestión de Restaurante",
    description="API REST para gestión de usuarios y demás entidades presente en el Restaurante",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
""" Importacion de los routers"""
app.include_router(Usuario.router)
app.include_router(Categoria.router)
app.include_router(Cliente.router)
app.include_router(Empleado.router)
app.include_router(Factura.router)
app.include_router(Mesa.router)
app.include_router(Orden.router)
app.include_router(Plato_Orden.router)
app.include_router(Plato.router)
app.include_router(Reserva.router)


@app.on_event("startup")
async def startup_event():
    print("Iniciando Sistema de Gestión de Restaurante...")
    print("Configurando base de datos...")
    create_tables()
    print("Sistema listo para usar.")
    print("Documentación disponible en: http://localhost:4000/docs")


@app.get("/", tags=["raíz"])
async def root():
    return {
        "mensaje": "Bienvenido al Sistema de Gestión del Restaurante",
        "version": "1.0.0",
        "documentacion": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "autenticacion": "/auth",
            "usuarios": "/usuarios",
            "categorias": "/categorias",
            "productos": "/productos",
        },
    }


def main():
    """Función principal para ejecutar el servidor"""
    print("Iniciando servidor FastAPI...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=4000,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
