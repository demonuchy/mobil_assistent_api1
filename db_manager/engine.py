
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .config import settings
from .models import Base



asyncEngine=create_async_engine(url=settings.AsyncDataBaseUrl, echo=False)
asyncSession=async_sessionmaker(asyncEngine)

async def create_all_table():
    asyncEngine.echo=True
    async with asyncEngine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
   

async def delete_all_table():
    asyncEngine.echo = True
    async with asyncEngine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
   
