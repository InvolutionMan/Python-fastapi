import sqlmodel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

ASYNC_DATABASE_URL=f"mysql+aiomysql://root:12345678@localhost:3306/news_app"

async_engine=create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
)

AsyncSessionLocal= async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise






