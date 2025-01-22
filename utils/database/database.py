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
        query = """
        SELECT 
            tg_id, username, fullname, phone, location_id, chat_lang, registered_at 
        FROM 
            bot_users 
        WHERE 
            tg_id = $1
        """
        return await self.fetchrow(query, str(tg_id))

    async def add_user(self, tg_id, username, fullname, phone, latitude, longitude, address, chat_lang, **kwagrs):
        query_location = """
            INSERT INTO locations (latitude, longitude, address)
            VALUES ($1, $2, $3)
            RETURNING id;
        """
        location_id = await self.fetchval(query_location, latitude, longitude, address)

        query_user = """
            INSERT INTO bot_users (tg_id, username, fullname, phone, location_id, chat_lang, registered_at)
            VALUES ($1, $2, $3, $4, $5, $6, NOW());
        """
        await self.execute(query_user, str(tg_id), username, fullname, phone, location_id, chat_lang)

    async def add_result(self, user, attempts, created_at, completed_at, **kwargs):
        query = """
            INSERT INTO results (user_id, number_of_attempts, created_at, completed_at)
            VALUES ($1, $2, $3, $4);
        """
        await self.execute(query, user['tg_id'], attempts, created_at, completed_at)
