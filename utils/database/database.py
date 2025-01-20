import asyncpg

from data.config import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT


class Database:
    def __init__(self):
        self.db = POSTGRES_DB
        self.user = POSTGRES_USER
        self.password = POSTGRES_PASSWORD
        self.host = POSTGRES_HOST
        self.port = POSTGRES_PORT
        self.pool = None  # type: asyncpg.pool

    async def connect(self):
        if self.pool is None:
            try:
                self.pool = await asyncpg.create_pool(
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                    database=self.db,
                    min_size=1,
                    max_size=10,
                    timeout=10
                )
            except Exception as e:
                raise RuntimeError(f"Error connecting to the database: {e}")

    async def disconnect(self):
        if self.pool is not None:
            await self.pool.close()

    async def execute(self, command, *args) -> None:
        await self._query("execute", command, *args)

    async def fetch(self, command, *args) -> list[dict]:
        result = await self._query("fetch", command, *args)
        return [dict(row) for row in result] if result else []

    async def fetchrow(self, command, *args) -> dict | None:
        result = await self._query("fetchrow", command, *args)
        return dict(result) if result else None

    async def fetchval(self, command, *args):
        return await self._query("fetchval", command, *args)

    async def _query(self, query_type, command, *args):
        if self.pool is None:
            raise RuntimeError("Database pool is not initialized. Call `connect()` first.")

        try:
            async with self.pool.acquire() as connection:
                return await getattr(connection, query_type)(command, *args)
        except asyncpg.PostgresError as e:
            raise RuntimeError(f"Database query failed: {e}")

    async def get_user(self, tg_id):
        pass
