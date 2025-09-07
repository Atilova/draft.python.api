from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class UnitOfWork:
    __slots__ = (
        ""
    )
    
    def __init__(
        self,
        *,
        
    ):
        ...
    
    async def __aenter__(self):
        ...
        
    async def __aexit__(self):
        ...
        
    