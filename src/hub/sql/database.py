from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql+asyncpg://test_user:password@192.168.0.57:5432/test"
DATABASE_URL_SYNC = "postgresql://test_user:password@192.168.0.57:5432/test"

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
    )
Base = declarative_base()
