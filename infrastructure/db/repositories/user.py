# infrastructure/db/repositories/user.py

from infrastructure.db.repo_base import get_conn
from domain.models import User

class UserRepo:
    async def upsert(self, *, telegram_id: int, username: str) -> User:
        sql = """
        INSERT INTO public."user" (telegram_id, username)
        VALUES ($1, $2)
        ON CONFLICT (telegram_id) DO UPDATE
          SET username = EXCLUDED.username
        RETURNING *;
        """
        row = await get_conn().fetchrow(sql, telegram_id, username)
        data = dict(row)
        # переименовываем id_user -> id
        data["id"] = data.pop("id_user")
        return User.model_validate(data)

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        sql = 'SELECT * FROM public."user" WHERE telegram_id = $1;'
        row = await get_conn().fetchrow(sql, telegram_id)
        if not row:
            return None
        data = dict(row)
        data["id"] = data.pop("id_user")
        return User.model_validate(data)
