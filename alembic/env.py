import sys
sys.path.append("./app")  # Alembic FastAPI app-ni ko‘rishi uchun

from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context

# Alembic konfiguratsiyasini yuklash
config = context.config

# Log konfiguratsiyasini yuklash
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# SQLAlchemy modellari va metadata
from app.database import Base, sync_engine
from app import models  # Modellarni import qilish

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Offline rejimda migratsiyalarni ishga tushirish."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Online rejimda migratsiyalarni ishga tushirish."""
    connectable = sync_engine  # Asinxron emas, sinxron engine ishlatiladi

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
