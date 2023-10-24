from asyncio import current_task

from src.config import DB_USER, DB_PASS, DB_HOST, DB_NAME
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session, AsyncSession

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )
        return session

    async def get_scoped_session_dependency(self) -> AsyncSession:
        print("session began")
        session = self.get_scoped_session()
        yield session
        print("session closed")
        await session.close()


db_helper = DatabaseHelper(
    url="postgresql+asyncpg://harold:123@localhost/tennis_stat",
    echo=False
)
