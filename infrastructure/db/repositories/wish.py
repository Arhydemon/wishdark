# infrastructure/db/repositories/wish.py

from infrastructure.db.repo_base import get_conn
from domain.models import Wish
from decimal import Decimal
from typing import List

class WishRepo:
    async def create(
        self,
        *,
        id_requester: int,
        id_category: int,
        description: str,
        amount: Decimal,
        currency: str,
        deadline,
    ) -> Wish:
        sql = """
        INSERT INTO public.wish (
          id_requester, id_category, description,
          amount, currency, deadline
        ) VALUES ($1,$2,$3,$4,$5,$6)
        RETURNING *;
        """
        row = await get_conn().fetchrow(
            sql,
            id_requester,
            id_category,
            description,
            amount,
            currency,
            deadline,
        )
        data = dict(row)
        # Переименовываем автоинкрементное поле
        data["id"] = data.pop("id_wish")
        return Wish.model_validate(data)

    async def get_by_id(self, wish_id: int) -> Wish | None:
        sql = "SELECT * FROM public.wish WHERE id_wish = $1;"
        row = await get_conn().fetchrow(sql, wish_id)
        if not row:
            return None
        data = dict(row)
        data["id"] = data.pop("id_wish")
        return Wish.model_validate(data)

    async def list_open(self, limit: int, offset: int) -> List[Wish]:
        sql = """
        SELECT * FROM public.wish
        WHERE status = 'open'
        ORDER BY created_at DESC
        LIMIT $1 OFFSET $2;
        """
        rows = await get_conn().fetch(sql, limit, offset)
        result = []
        for row in rows:
            data = dict(row)
            data["id"] = data.pop("id_wish")
            result.append(Wish.model_validate(data))
        return result

    async def update_status(self, wish_id: int, status: str) -> None:
        sql = "UPDATE public.wish SET status = $1 WHERE id_wish = $2;"
        await get_conn().execute(sql, status, wish_id)
