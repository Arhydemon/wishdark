from infrastructure.db.repo_base import get_conn
from domain.models import DealMessage

class DealMessageRepo:
    async def create(self, *, deal_id: int, sender_id: int, message: str) -> DealMessage:
        sql = """
        INSERT INTO public.deal_message (id_deal, sender_id, message)
        VALUES ($1, $2, $3)
        RETURNING *;
        """
        row = await get_conn().fetchrow(sql, deal_id, sender_id, message)
        data = dict(row)
        data["id"] = data.pop("id_message")
        return DealMessage.model_validate(data)
