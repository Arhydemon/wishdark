# infrastructure/db/repositories/deal.py

from infrastructure.db.repo_base import get_conn
from domain.models import Deal

class DealRepo:
    async def create(self, *, wish_id: int, wishmaker_id: int) -> Deal:
        sql = """
        INSERT INTO public.deal (
            id_wish, id_wishmaker
        ) VALUES ($1, $2)
        RETURNING *;
        """
        row = await get_conn().fetchrow(sql, wish_id, wishmaker_id)
        return Deal.model_validate(dict(row))

    async def get_by_id(self, deal_id: int) -> Deal | None:
        sql = "SELECT * FROM public.deal WHERE id_deal = $1;"
        row = await get_conn().fetchrow(sql, deal_id)
        return Deal.model_validate(dict(row)) if row else None
