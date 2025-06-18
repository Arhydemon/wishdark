# infrastructure/db/repositories/wish.py

from infrastructure.db.repo_base import get_conn
from domain.models import Wish
from decimal import Decimal
from typing import List, Optional


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
        return Wish.model_validate(dict(row))

    async def get_by_id(self, wish_id: int) -> Optional[Wish]:
        sql = "SELECT * FROM public.wish WHERE id_wish = $1;"
        row = await get_conn().fetchrow(sql, wish_id)
        return Wish.model_validate(dict(row)) if row else None

    async def list_open(
        self,
        limit: int = 5,
        offset: int = 0
    ) -> List[Wish]:
        sql = """
        SELECT * FROM public.wish
        WHERE status = 'open'
        ORDER BY created_at DESC
        LIMIT $1 OFFSET $2;
        """
        rows = await get_conn().fetch(sql, limit, offset)
        return [Wish.model_validate(dict(r)) for r in rows]

    async def update_status(
        self,
        wish_id: int,
        new_status: str
    ) -> None:
        sql = "UPDATE public.wish SET status = $2 WHERE id_wish = $1;"
        await get_conn().execute(sql, wish_id, new_status)
