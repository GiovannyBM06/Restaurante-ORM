"""
Script para probar la conexión asíncrona con Neon PostgreSQL
Basado en el ejemplo de Neon
"""

import asyncio
import os
import re

from dotenv import load_dotenv
from database.config import Base
from entities.Categoria import Categoria
from entities.Cliente import Cliente
from entities.Empleado import Empleado
from entities.Factura import Factura  
from entities.Mesa import Mesa
from entities.Orden import Orden    
from entities.Plato import Plato
from entities.Plato_Orden import Plato_Orden
from entities.Usuario import Usuario
from entities.Reserva import Reserva
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

load_dotenv()


async def async_main() -> None:
    """Función principal asíncrona para probar la conexión"""
    try:
        # Crear el motor asíncrono
        engine = create_async_engine(
            re.sub(r"^postgresql:", "postgresql+asyncpg:", os.getenv("DATABASE_URL")),
            echo=True,
        )

        # Probar conexión básica
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("✅ Conexión exitosa con Neon PostgreSQL!")
            print(f"Resultado de prueba: {result.fetchall()}")

        # Crear tablas
        print("\n📋 Creando tablas...")
        async with engine.begin() as conn:
            # Importar todas las entidades para crear las tablas
            from database.config import Base
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Tablas creadas exitosamente!")

        # Probar inserción de datos
        print("\n📝 Probando inserción de datos...")
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )

        async with async_session() as session:
            try:
                # Crear un usuario de prueba
                usuario_test = Usuario(
                    nombre="Usuario Test Async",
                    apellido="Admin",
                    email="admin@gmail.com",
                    contraseña="admin123",
                )
                session.add(usuario_test)
                await session.commit()
                print(f"✅ Usuario creado: {usuario_test}")

                # Crear una categoría de prueba
                categoria_test = Categoria(
                    nombre="Test Category Async",
                    descripcion="Categoría de prueba asíncrona para Neon",
                    id_usuario=usuario_test.id
                )
                session.add(categoria_test)
                await session.commit()
                print(f"✅ Categoría creada: {categoria_test}")

                # Crear un cliente de prueba
                cliente_test = Cliente(
                    nombre="Cliente Test Async",
                    apellido="Prueba",
                    Email="cliente-async@neon.com",
                    telefono="3101234567",
                    id_usuario=usuario_test.id
                )
                session.add(cliente_test)
                await session.commit()
                print(f"✅ Cliente creado: {cliente_test}")

                # Crear un empleado de prueba
                empleado_test = Empleado(
                    nombre="Empleado Test Async",
                    apellido="Prueba",
                    rol="Mesero",
                    salario=1200,
                    id_usuario=usuario_test.id
                )
                session.add(empleado_test)
                await session.commit()
                print(f"✅ Empleado creado: {empleado_test}")


                # Crear una mesa de prueba
                mesa_test = Mesa(
                    capacidad=4,
                    id_usuario=usuario_test.id
                )
                session.add(mesa_test)
                await session.commit()
                print(f"✅ Mesa creada: {mesa_test}")

                # Crear una orden de prueba
                orden_test = Orden(
                    numero_mesa=mesa_test.numero,
                    id_empleado=empleado_test.id,
                    estado="Pendiente",
                    id_usuario=usuario_test.id
                )
                session.add(orden_test)
                await session.commit()
                print(f"✅ Orden creada: {orden_test}")

                # Crear un plato de prueba
                plato_test = Plato(
                    nombre="Plato Test Async",
                    precio_unidad=25,
                    descripcion="Plato de prueba asíncrono para Neon",
                    id_categoria=categoria_test.id,
                    id_usuario=usuario_test.id
                )
                session.add(plato_test)
                await session.commit()
                print(f"✅ Plato creado: {plato_test}")

                # Crear una reserva de prueba
                reserva_test = Reserva(
                    CC_cliente=cliente_test.cc,
                    Numero_mesa=mesa_test.numero,
                    cantidad_personas=2,
                    fecha_Hora=datetime(2025, 9, 11, 19, 0, 0),
                    Estado=True,
                    id_usuario=usuario_test.id
                )
                session.add(reserva_test)
                await session.commit()
                print(f"✅ Reserva creada: {reserva_test}")

                # Crear una factura de prueba
                factura_test = Factura(
                    total=100.00,
                    metodo_pago="Efectivo",
                    numero_orden=orden_test.numero,
                    id_usuario=usuario_test.id
                )
                session.add(factura_test)
                await session.commit()
                print(f"✅ Factura creada: {factura_test}")

                # Crear un Plato_Orden de prueba
                plato_orden_test = Plato_Orden(
                    numero_orden=orden_test.numero,
                    id_plato=plato_test.id,
                    cantidad=2,
                    id_usuario=usuario_test.id
                )
                session.add(plato_orden_test)
                await session.commit()
                print(f"✅ Plato_Orden creado: {plato_orden_test}")

                print("\n🎉 ¡Todas las pruebas asíncronas pasaron exitosamente!")
                print("Tu ORM asíncrono está listo para usar con Neon PostgreSQL")

            except Exception as e:
                print(f"❌ Error en las pruebas: {e}")
                await session.rollback()

        await engine.dispose()

    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("\n🔧 Verifica que:")
        print("1. Hayas creado el archivo .env con la URL de Neon")
        print("2. La URL de conexión sea correcta")
        print("3. Hayas instalado las dependencias: pip install -r requirements.txt")


if __name__ == "__main__":
    asyncio.run(async_main())
