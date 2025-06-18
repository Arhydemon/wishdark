# infrastructure/db/repositories/deal.py

from infrastructure.db.repo_base import get_conn
from domain.models import Deal

class DealRepo:

    async def create(self, *, wish_id: int, wishmaker_id: int) -> Deal:
        sql = """
        INSERT INTO public.deal (id_wish, id_wishmaker)
        VALUES ($1, $2)
        RETURNING *;
        """
        row = await get_conn().fetchrow(sql, wish_id, wishmaker_id)
        data = dict(row)
        # переименовываем автогенерируемое поле
        data["id"] = data.pop("id_deal")
        return Deal.model_validate(data)

    async def get_by_id(self, deal_id: int) -> Deal | None:
        sql = "SELECT * FROM public.deal WHERE id_deal = $1;"
        row = await get_conn().fetchrow(sql, deal_id)
        if not row:
            return None
        data = dict(row)
        data["id"] = data.pop("id_deal")
        return Deal.model_validate(data)

    async def list_by_user(self, user_id: int) -> list[Deal]:
        sql = """
        SELECT * FROM public.deal
        WHERE id_wishmaker = $1
        ORDER BY start_date DESC;
        """
        rows = await get_conn().fetch(sql, user_id)
        result = []
        for row in rows:
            d = dict(row)
            d["id"] = d.pop("id_deal")
            result.append(Deal.model_validate(d))
        return result

    async def update_status(self, deal_id: int, status: str) -> None:
        sql = "UPDATE public.deal SET status = $1 WHERE id_deal = $2;"
        await get_conn().execute(sql, status, deal_id)
