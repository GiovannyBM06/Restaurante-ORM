"""
Configuración del entorno de Alembic
"""

import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool


"""
Agregar el directorio raíz al path para importar los modelos.
"""
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


"""
Importar los modelos para que Alembic los detecte.
"""
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


"""
Este es el objeto de configuración de Alembic, que da acceso a los valores del archivo .ini en uso.
"""
config = context.config


"""
Interpretar el archivo de configuración para el logging de Python.
Esta línea configura los loggers.
"""
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


"""
Agregar el objeto MetaData de los modelos para soporte de 'autogenerate'.
"""
target_metadata = Base.metadata


"""
Otros valores de configuración pueden ser adquiridos según las necesidades de env.py.
"""


def get_url():
    """Obtener la URL de la base de datos desde variables de entorno"""
    from database.config import DATABASE_URL

    return DATABASE_URL


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
