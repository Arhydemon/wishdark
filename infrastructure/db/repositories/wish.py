from infrastructure.db.repo_base import get_conn
from domain.models import Wish
from decimal import Decimal

class WishRepo:
    async def create(self, *, id_requester: int, id_category: int,
                     description: str, amount: Decimal,
                     currency: str, deadline):
        sql = """
        INSERT INTO public.wish (
          id_requester, id_category, description,
          amount, currency, deadline
        ) VALUES ($1,$2,$3,$4,$5,$6)
        RETURNING *;
        """
        row = await get_conn().fetchrow(
            sql, id_requester, id_category, description,
            amount, currency, deadline
        )
        return Wish.model_validate(dict(row))
