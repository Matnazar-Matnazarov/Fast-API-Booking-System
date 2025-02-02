from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://root:password@localhost:5432/booking_system"
)

# Asinxron engine (FastAPI uchun ishlatiladi)
async_engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as session:
        yield session


# Alembic uchun sinxron engine (faqat migratsiyalar uchun)
sync_engine = create_engine(DATABASE_URL.replace("asyncpg", "psycopg2"))
